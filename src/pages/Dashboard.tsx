import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Activity, MessageCircle, History, CreditCard, Crown, Gift, User as UserIcon } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { supabase } from '../lib/supabase'
import type { Consultation } from '../types'

export function Dashboard() {
  const { user } = useAuth()
  const [consultations, setConsultations] = useState<Consultation[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchConsultations()
    }
  }, [user])

  const fetchConsultations = async () => {
    try {
      const { data, error } = await supabase
        .from('consultations')
        .select('*')
        .eq('user_id', user?.id)
        .order('created_at', { ascending: false })
        .limit(5)

      if (error) throw error
      setConsultations(data || [])
    } catch (error) {
      console.error('Error fetching consultations:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!user) return null

  const canUseFreeConsultation = user.free_consultations_used < 1
  const hasActiveSubscription = user.subscription_status === 'premium' && 
    user.subscription_expires && new Date(user.subscription_expires) > new Date()

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 text-white p-6 rounded-xl mb-8">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">Welcome back, {user.first_name}!</h1>
            <p className="opacity-90">Ready to check your health today? Let's get started with a quick assessment.</p>
          </div>
          <div className="mt-4 md:mt-0">
            <Link to="/symptoms" className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-6 rounded-lg transition-colors">
              <Activity className="w-5 h-5 mr-2 inline" />
              Start Assessment
            </Link>
          </div>
        </div>
      </div>

      {/* Payment Status Alert */}
      {!canUseFreeConsultation && !hasActiveSubscription && (
        <div className="bg-warning-50 border border-warning-200 text-warning-800 p-4 rounded-lg mb-6">
          <div className="flex items-center">
            <CreditCard className="w-5 h-5 mr-3" />
            <div>
              <strong>Payment Required</strong>
              <p className="text-sm mt-1">You've used your free consultation. To continue using our AI doctor service, please choose a plan.</p>
            </div>
          </div>
          <div className="mt-3 flex gap-2">
            <Link to="/pricing" className="btn-warning text-sm">View Plans</Link>
            <Link to="/ai-doctor" className="bg-warning-200 text-warning-800 hover:bg-warning-300 font-medium py-1 px-3 rounded text-sm transition-colors">
              Try AI Doctor
            </Link>
          </div>
        </div>
      )}

      {hasActiveSubscription && (
        <div className="bg-success-50 border border-success-200 text-success-800 p-4 rounded-lg mb-6">
          <div className="flex items-center">
            <Crown className="w-5 h-5 mr-3" />
            <div>
              <strong>Premium Active</strong>
              <p className="text-sm mt-1">
                You have unlimited access to AI consultations until {new Date(user.subscription_expires!).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="card p-6 mb-6">
            <h2 className="text-xl font-bold mb-6 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Quick Actions
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Link to="/symptoms" className="card p-6 text-center hover:shadow-lg transition-all duration-300 group">
                <Activity className="w-12 h-12 text-primary-600 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold mb-2">Symptom Checker</h3>
                <p className="text-gray-600 text-sm mb-4">Get instant insights about your symptoms</p>
                <span className="btn-primary inline-block">Start Now</span>
              </Link>
              
              <Link to="/ai-doctor" className="card p-6 text-center hover:shadow-lg transition-all duration-300 group">
                <MessageCircle className="w-12 h-12 text-success-600 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold mb-2">AI Doctor Chat</h3>
                <p className="text-gray-600 text-sm mb-4">Chat with Dr. Sarah Chen for personalized advice</p>
                <span className="btn-success inline-block">Start Chat</span>
              </Link>
              
              <Link to="/history" className="card p-6 text-center hover:shadow-lg transition-all duration-300 group">
                <History className="w-12 h-12 text-blue-600 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold mb-2">View History</h3>
                <p className="text-gray-600 text-sm mb-4">Review your past consultations</p>
                <span className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors inline-block">View All</span>
              </Link>
              
              <Link to="/pricing" className="card p-6 text-center hover:shadow-lg transition-all duration-300 group">
                <CreditCard className="w-12 h-12 text-warning-600 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="font-bold mb-2">Pricing Plans</h3>
                <p className="text-gray-600 text-sm mb-4">Upgrade to premium for unlimited access</p>
                <span className="btn-warning inline-block">View Plans</span>
              </Link>
            </div>
          </div>

          {/* Recent Consultations */}
          <div className="card p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold flex items-center">
                <History className="w-5 h-5 mr-2 text-primary-600" />
                Recent Consultations
              </h2>
              {consultations.length > 0 && (
                <Link to="/history" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                  View All
                </Link>
              )}
            </div>

            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
              </div>
            ) : consultations.length > 0 ? (
              <div className="space-y-4">
                {consultations.map((consultation) => (
                  <div key={consultation.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-2">
                          <span className="text-sm text-gray-500">
                            {new Date(consultation.created_at).toLocaleDateString()}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            consultation.severity === 'severe' ? 'bg-danger-100 text-danger-800' :
                            consultation.severity === 'moderate' ? 'bg-warning-100 text-warning-800' :
                            'bg-success-100 text-success-800'
                          }`}>
                            {consultation.severity}
                          </span>
                          {consultation.payment_status === 'paid' && (
                            <span className="bg-success-100 text-success-800 px-2 py-1 rounded-full text-xs font-medium">
                              Paid
                            </span>
                          )}
                          {consultation.payment_status === 'free' && (
                            <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                              Free
                            </span>
                          )}
                        </div>
                        <div className="text-sm text-gray-600">
                          {consultation.symptoms.slice(0, 3).join(', ').replace(/_/g, ' ')}
                          {consultation.symptoms.length > 3 && ` and ${consultation.symptoms.length - 3} more`}
                        </div>
                      </div>
                      <Link
                        to={`/results/${consultation.id}`}
                        className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                      >
                        View Results
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <History className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-gray-600 font-medium mb-2">No consultations yet</h3>
                <p className="text-gray-500 text-sm mb-4">Start your first health assessment to see results here</p>
                <Link to="/symptoms" className="btn-primary">
                  Start Assessment
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Subscription Status */}
          <div className="card p-6 text-center">
            <h3 className="text-lg font-bold mb-4 flex items-center justify-center">
              <Crown className="w-5 h-5 mr-2 text-warning-600" />
              Your Plan
            </h3>
            
            {hasActiveSubscription ? (
              <div className="space-y-3">
                <div className="text-3xl font-bold text-success-600 flex items-center justify-center">
                  <Crown className="w-8 h-8 mr-2" />
                  Premium
                </div>
                <div className="text-gray-600">Active until {new Date(user.subscription_expires!).toLocaleDateString()}</div>
                <div className="text-success-600 font-medium">
                  <Activity className="w-4 h-4 mr-1 inline" />
                  Unlimited consultations
                </div>
              </div>
            ) : canUseFreeConsultation ? (
              <div className="space-y-3">
                <div className="text-3xl font-bold text-primary-600 flex items-center justify-center">
                  <Gift className="w-8 h-8 mr-2" />
                  Free Trial
                </div>
                <div className="text-gray-600">1 free consultation remaining</div>
                <Link to="/pricing" className="btn-warning text-sm">
                  Upgrade to Premium
                </Link>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="text-3xl font-bold text-gray-600 flex items-center justify-center">
                  <UserIcon className="w-8 h-8 mr-2" />
                  Basic
                </div>
                <div className="text-gray-600">Free trial used</div>
                <Link to="/pricing" className="btn-warning text-sm">
                  Choose a Plan
                </Link>
              </div>
            )}
          </div>

          {/* Health Stats */}
          <div className="card p-6 text-center">
            <h3 className="text-lg font-bold mb-4 flex items-center justify-center">
              <Activity className="w-5 h-5 mr-2 text-primary-600" />
              Your Health Stats
            </h3>
            
            <div className="space-y-4">
              <div>
                <div className="text-3xl font-bold text-primary-600">{consultations.length}</div>
                <div className="text-gray-600">Total Assessments</div>
              </div>
              
              <div>
                <div className="text-3xl font-bold text-success-600">
                  {consultations.filter(c => new Date(c.created_at).getMonth() === new Date().getMonth()).length}
                </div>
                <div className="text-gray-600">This Month</div>
              </div>
              
              <div>
                <div className="text-3xl font-bold text-blue-600">
                  {canUseFreeConsultation ? 1 : 0}
                </div>
                <div className="text-gray-600">Free Consultations Left</div>
              </div>
            </div>
          </div>

          {/* Health Tips */}
          <div className="card p-6">
            <h3 className="text-lg font-bold mb-4 flex items-center">
              <Activity className="w-5 h-5 mr-2 text-warning-600" />
              Daily Health Tips
            </h3>
            
            <div className="space-y-4">
              <div className="flex items-start">
                <div className="w-2 h-2 bg-success-600 rounded-full mt-2 mr-3"></div>
                <div>
                  <strong className="text-sm">Stay Hydrated</strong>
                  <p className="text-gray-600 text-sm">Drink at least 8 glasses of water daily</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="w-2 h-2 bg-success-600 rounded-full mt-2 mr-3"></div>
                <div>
                  <strong className="text-sm">Regular Exercise</strong>
                  <p className="text-gray-600 text-sm">Aim for 30 minutes of activity daily</p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="w-2 h-2 bg-success-600 rounded-full mt-2 mr-3"></div>
                <div>
                  <strong className="text-sm">Quality Sleep</strong>
                  <p className="text-gray-600 text-sm">Get 7-9 hours of sleep each night</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Emergency Notice */}
      <div className="bg-danger-50 border border-danger-200 text-danger-800 p-4 rounded-lg mt-8">
        <div className="flex items-center">
          <Activity className="w-6 h-6 mr-3" />
          <div>
            <h3 className="font-bold mb-1">Medical Emergency</h3>
            <p className="text-sm">
              If you're experiencing a medical emergency, please call emergency services immediately. 
              This platform is not a substitute for emergency medical care.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}