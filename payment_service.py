import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional
from models import Payment, User, Consultation, PricingPlan

class PaymentService:
    def __init__(self):
        # Initialize Stripe (you'll need to set STRIPE_SECRET_KEY in environment)
        stripe_key = os.getenv('STRIPE_SECRET_KEY')
        if stripe_key and stripe_key != 'sk_test_your_secret_key_here':
            try:
                import stripe
                stripe.api_key = stripe_key
                self.enabled = True
            except ImportError:
                self.enabled = False
        else:
            self.enabled = False
        
        self.currency = 'usd'
        
        # Default pricing plans
        self.default_plans = {
            'single_consultation': {
                'name': 'Single Consultation',
                'price': 9.99,
                'consultations_limit': 1,
                'duration_days': 1
            },
            'monthly_premium': {
                'name': 'Monthly Premium',
                'price': 29.99,
                'consultations_limit': 10,
                'duration_days': 30
            },
            'yearly_premium': {
                'name': 'Yearly Premium',
                'price': 299.99,
                'consultations_limit': 120,
                'duration_days': 365
            }
        }
    
    def create_payment_intent(self, amount: float, payment_type: str, user_id: int, consultation_id: Optional[int] = None) -> Dict:
        """
        Create a Stripe payment intent
        """
        if not self.enabled:
            return {
                'error': 'Payment processing is not available. Please set up your Stripe API keys.',
                'success': False
            }
        
        try:
            import stripe
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=self.currency,
                metadata={
                    'user_id': user_id,
                    'payment_type': payment_type,
                    'consultation_id': consultation_id or '',
                    'transaction_id': str(uuid.uuid4())
                }
            )
            
            # Save payment record
            payment = Payment(
                user_id=user_id,
                amount=amount,
                currency=self.currency.upper(),
                payment_type=payment_type,
                transaction_id=intent.metadata['transaction_id'],
                consultation_id=consultation_id,
                status='pending'
            )
            
            return {
                'client_secret': intent.client_secret,
                'payment_id': payment.id,
                'transaction_id': payment.transaction_id,
                'amount': amount,
                'currency': self.currency
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def process_payment_success(self, payment_intent_id: str) -> Dict:
        """
        Process successful payment
        """
        if not self.enabled:
            return {'error': 'Payment processing is not available', 'success': False}
        
        try:
            import stripe
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # Find payment record
            payment = Payment.query.filter_by(transaction_id=intent.metadata['transaction_id']).first()
            if not payment:
                return {'error': 'Payment record not found', 'success': False}
            
            # Update payment status
            payment.status = 'completed'
            payment.completed_at = datetime.utcnow()
            
            # Update user based on payment type
            user = User.query.get(payment.user_id)
            if payment.payment_type == 'consultation':
                # Mark consultation as paid
                if payment.consultation_id:
                    consultation = Consultation.query.get(payment.consultation_id)
                    if consultation:
                        consultation.payment_status = 'paid'
            elif payment.payment_type == 'subscription':
                # Update user subscription
                plan_name = intent.metadata.get('plan_name', 'monthly_premium')
                plan = self.default_plans.get(plan_name, self.default_plans['monthly_premium'])
                
                user.subscription_status = 'premium'
                user.subscription_expires = datetime.utcnow() + timedelta(days=plan['duration_days'])
            
            return {
                'success': True,
                'payment_id': payment.id,
                'user_id': payment.user_id,
                'amount': payment.amount
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def get_pricing_plans(self) -> Dict:
        """
        Get available pricing plans
        """
        return self.default_plans
    
    def calculate_consultation_cost(self, user: User) -> Dict:
        """
        Calculate cost for consultation based on user's current status
        """
        if user.can_use_free_consultation():
            return {
                'cost': 0.0,
                'currency': 'USD',
                'payment_required': False,
                'message': 'Free consultation available'
            }
        elif user.has_active_subscription():
            return {
                'cost': 0.0,
                'currency': 'USD',
                'payment_required': False,
                'message': 'Covered by active subscription'
            }
        else:
            return {
                'cost': 9.99,
                'currency': 'USD',
                'payment_required': True,
                'message': 'Payment required for consultation'
            }
    
    def create_subscription_payment(self, user_id: int, plan_name: str) -> Dict:
        """
        Create payment for subscription
        """
        if not self.enabled:
            return {'error': 'Payment processing is not available. Please set up your Stripe API keys.', 'success': False}
        
        plan = self.default_plans.get(plan_name)
        if not plan:
            return {'error': 'Invalid plan', 'success': False}
        
        return self.create_payment_intent(
            amount=plan['price'],
            payment_type='subscription',
            user_id=user_id,
            consultation_id=None
        )
    
    def refund_payment(self, payment_id: int) -> Dict:
        """
        Process payment refund
        """
        if not self.enabled:
            return {'error': 'Payment processing is not available', 'success': False}
        
        try:
            import stripe
            payment = Payment.query.get(payment_id)
            if not payment:
                return {'error': 'Payment not found', 'success': False}
            
            # Create Stripe refund
            refund = stripe.Refund.create(
                payment_intent=payment.transaction_id,
                reason='requested_by_customer'
            )
            
            # Update payment status
            payment.status = 'refunded'
            
            return {
                'success': True,
                'refund_id': refund.id,
                'amount': payment.amount
            }
            
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def get_user_payment_history(self, user_id: int) -> list:
        """
        Get payment history for user
        """
        payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
        return [
            {
                'id': p.id,
                'amount': p.amount,
                'currency': p.currency,
                'type': p.payment_type,
                'status': p.status,
                'date': p.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'transaction_id': p.transaction_id
            }
            for p in payments
        ]
