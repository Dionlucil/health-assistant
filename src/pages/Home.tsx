import React from 'react'
import { Link } from 'react-router-dom'
import { Activity, Brain, FileText, Users, Shield, Clock } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

export function Home() {
  const { user } = useAuth()

  return (
    <div>
      {/* Hero Section */}
      <section className="hero-gradient min-h-[75vh] flex items-center">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div className="animate-fade-in-up">
              <h1 className="text-4xl lg:text-6xl font-bold mb-6">
                Your Personal Health <span className="text-gradient">Assistant</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Get quick insights about your symptoms with our AI-powered health assessment tool. 
                Always remember to consult with healthcare professionals for proper medical advice.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 mb-8">
                {user ? (
                  <>
                    <Link to="/symptoms" className="btn-primary text-lg px-8 py-3">
                      <Activity className="w-5 h-5 mr-2" />
                      Start Assessment
                    </Link>
                    <Link to="/dashboard" className="btn-secondary text-lg px-8 py-3">
                      <Activity className="w-5 h-5 mr-2" />
                      Dashboard
                    </Link>
                  </>
                ) : (
                  <>
                    <Link to="/register" className="btn-primary text-lg px-8 py-3">
                      <Users className="w-5 h-5 mr-2" />
                      Get Started
                    </Link>
                    <Link to="/login" className="btn-secondary text-lg px-8 py-3">
                      <Users className="w-5 h-5 mr-2" />
                      Login
                    </Link>
                  </>
                )}
              </div>
              
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-start">
                  <Shield className="w-5 h-5 text-blue-600 mr-2 mt-0.5" />
                  <div>
                    <strong className="text-blue-900">Remember:</strong>
                    <span className="text-blue-800"> This tool provides health information only. 
                    For medical emergencies, call emergency services immediately.</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="text-center">
              <div className="text-primary-600 animate-float">
                <Activity className="w-48 h-48 mx-auto opacity-80" />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">How It Works</h2>
            <p className="text-xl text-gray-600">Simple steps to get personalized health insights</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card p-8 text-center hover:shadow-lg transition-all duration-300">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">1. Select Symptoms</h3>
              <p className="text-gray-600">
                Choose from our comprehensive list of symptoms and describe your condition accurately.
              </p>
            </div>
            
            <div className="card p-8 text-center hover:shadow-lg transition-all duration-300">
              <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-success-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">2. AI Analysis</h3>
              <p className="text-gray-600">
                Our AI analyzes your symptoms against medical databases to provide insights.
              </p>
            </div>
            
            <div className="card p-8 text-center hover:shadow-lg transition-all duration-300">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Activity className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-4">3. Get Recommendations</h3>
              <p className="text-gray-600">
                Receive personalized health recommendations and guidance on next steps.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      {user && (
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
              <div className="animate-fade-in-up">
                <Users className="w-12 h-12 text-primary-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Trusted</h3>
                <p className="text-gray-600">By healthcare professionals</p>
              </div>
              <div className="animate-fade-in-up">
                <Shield className="w-12 h-12 text-success-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Secure</h3>
                <p className="text-gray-600">Your data is protected</p>
              </div>
              <div className="animate-fade-in-up">
                <Clock className="w-12 h-12 text-blue-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-900 mb-2">24/7</h3>
                <p className="text-gray-600">Available anytime</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      {!user && (
        <section className="py-16 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
            <p className="text-xl mb-8 opacity-90">Join thousands of users who trust our health assessment tool</p>
            <Link to="/register" className="bg-white text-primary-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors">
              <Users className="w-5 h-5 mr-2 inline" />
              Create Your Account
            </Link>
          </div>
        </section>
      )}
    </div>
  )
}