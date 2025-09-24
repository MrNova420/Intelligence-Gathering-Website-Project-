import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

interface SubscriptionPlan {
  id: string
  name: string
  price: number
  period: string
  features: string[]
  limits: {
    queriesPerDay: number
    scannersPerQuery: number
    dataRetentionDays: number
    exportFormats: string[]
    apiAccess: boolean
  }
  popular?: boolean
  current?: boolean
}

interface UserSubscription {
  plan: string
  status: 'active' | 'cancelled' | 'expired' | 'trial'
  currentPeriodEnd: string
  usage: {
    queriesUsedToday: number
    queriesRemainingToday: number
    totalQueriesThisMonth: number
  }
}

export default function SubscriptionPage() {
  const router = useRouter()
  const [currentSubscription, setCurrentSubscription] = useState<UserSubscription | null>(null)
  const [loading, setLoading] = useState(true)
  
  const subscriptionPlans: SubscriptionPlan[] = [
    {
      id: 'free',
      name: 'Free',
      price: 0,
      period: 'forever',
      features: [
        'Up to 5 queries per day',
        'Preview reports only',
        'Basic 10 scanner tools',
        'JSON and HTML export',
        '7-day data retention',
        'Community support'
      ],
      limits: {
        queriesPerDay: 5,
        scannersPerQuery: 10,
        dataRetentionDays: 7,
        exportFormats: ['JSON', 'HTML'],
        apiAccess: false
      },
      current: true
    },
    {
      id: 'professional',
      name: 'Professional',
      price: 29,
      period: 'month',
      popular: true,
      features: [
        'Up to 100 queries per day',
        'Full detailed reports',
        '50+ advanced scanner tools',
        'PDF, JSON, HTML, CSV export',
        '90-day data retention',
        'API access included',
        'Advanced filtering',
        'Priority support',
        'Bulk operations'
      ],
      limits: {
        queriesPerDay: 100,
        scannersPerQuery: 50,
        dataRetentionDays: 90,
        exportFormats: ['PDF', 'JSON', 'HTML', 'CSV'],
        apiAccess: true
      }
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      price: 99,
      period: 'month',
      features: [
        'Up to 1,000 queries per day',
        'Complete intelligence reports',
        '100+ scanner tools',
        'All export formats',
        '365-day data retention',
        'Full API access',
        'Custom integrations',
        'White-label reports',
        'Dedicated support',
        'Advanced analytics',
        'Compliance features',
        'Priority processing'
      ],
      limits: {
        queriesPerDay: 1000,
        scannersPerQuery: 100,
        dataRetentionDays: 365,
        exportFormats: ['PDF', 'JSON', 'HTML', 'CSV', 'XML'],
        apiAccess: true
      }
    }
  ]

  useEffect(() => {
    // Simulate loading current subscription
    setTimeout(() => {
      setCurrentSubscription({
        plan: 'free',
        status: 'active',
        currentPeriodEnd: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
        usage: {
          queriesUsedToday: 2,
          queriesRemainingToday: 3,
          totalQueriesThisMonth: 45
        }
      })
      setLoading(false)
    }, 1000)
  }, [])

  const handleUpgrade = (planId: string) => {
    // In real implementation, this would integrate with Stripe or similar
    console.log(`Upgrading to ${planId}`)
    
    // Simulate payment process
    const confirmUpgrade = window.confirm(`Upgrade to ${planId.charAt(0).toUpperCase() + planId.slice(1)} plan?`)
    if (confirmUpgrade) {
      alert('Redirecting to secure payment page...')
      // router.push(`/checkout?plan=${planId}`)
    }
  }

  const handleManageSubscription = () => {
    // In real implementation, this would redirect to billing portal
    alert('Redirecting to billing portal...')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading subscription information...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">Choose Your Intelligence Plan</h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Unlock the full power of our intelligence gathering platform with advanced features,
            higher limits, and priority support.
          </p>
        </div>

        {/* Current Subscription Status */}
        {currentSubscription && (
          <div className="max-w-4xl mx-auto mb-12">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
              <h2 className="text-2xl font-semibold text-white mb-4">Current Subscription</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary-400 mb-2">
                    {currentSubscription.plan.charAt(0).toUpperCase() + currentSubscription.plan.slice(1)}
                  </div>
                  <div className="text-gray-400">Current Plan</div>
                  <div className={`inline-block px-3 py-1 rounded-full text-sm mt-2 ${
                    currentSubscription.status === 'active' ? 'bg-green-600 text-green-100' :
                    currentSubscription.status === 'trial' ? 'bg-yellow-600 text-yellow-100' :
                    'bg-red-600 text-red-100'
                  }`}>
                    {currentSubscription.status.charAt(0).toUpperCase() + currentSubscription.status.slice(1)}
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-white mb-2">
                    {currentSubscription.usage.queriesRemainingToday}
                  </div>
                  <div className="text-gray-400">Queries Remaining Today</div>
                  <div className="text-sm text-gray-500 mt-1">
                    Used: {currentSubscription.usage.queriesUsedToday}
                  </div>
                </div>
                
                <div className="text-center">
                  <div className="text-3xl font-bold text-white mb-2">
                    {currentSubscription.usage.totalQueriesThisMonth}
                  </div>
                  <div className="text-gray-400">Total This Month</div>
                  <div className="text-sm text-gray-500 mt-1">
                    Ends: {new Date(currentSubscription.currentPeriodEnd).toLocaleDateString()}
                  </div>
                </div>
              </div>
              
              {currentSubscription.plan !== 'free' && (
                <div className="text-center mt-6">
                  <button 
                    onClick={handleManageSubscription}
                    className="btn-secondary"
                  >
                    Manage Subscription
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Pricing Plans */}
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {subscriptionPlans.map((plan) => (
              <div 
                key={plan.id}
                className={`relative bg-white/10 backdrop-blur-sm rounded-lg p-8 border transition-all duration-300 hover:scale-105 ${
                  plan.popular ? 'border-primary-500 ring-2 ring-primary-500' : 'border-gray-600'
                } ${plan.current ? 'ring-2 ring-green-500' : ''}`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-primary-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                      MOST POPULAR
                    </span>
                  </div>
                )}
                
                {plan.current && (
                  <div className="absolute -top-4 right-4">
                    <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                      CURRENT
                    </span>
                  </div>
                )}

                {/* Plan Header */}
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-white mb-4">{plan.name}</h3>
                  <div className="text-4xl font-bold text-white mb-2">
                    ${plan.price}
                    {plan.price > 0 && <span className="text-lg text-gray-400">/{plan.period}</span>}
                  </div>
                  {plan.price === 0 && (
                    <div className="text-gray-400">No credit card required</div>
                  )}
                </div>

                {/* Plan Limits */}
                <div className="bg-gray-800/50 rounded-lg p-4 mb-6">
                  <h4 className="font-semibold text-white mb-3">Plan Limits</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Daily Queries:</span>
                      <span className="text-white font-medium">{plan.limits.queriesPerDay}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Scanners per Query:</span>
                      <span className="text-white font-medium">{plan.limits.scannersPerQuery}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Data Retention:</span>
                      <span className="text-white font-medium">{plan.limits.dataRetentionDays} days</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">API Access:</span>
                      <span className={`font-medium ${plan.limits.apiAccess ? 'text-green-400' : 'text-red-400'}`}>
                        {plan.limits.apiAccess ? 'Yes' : 'No'}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Features List */}
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <svg className="w-5 h-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
                      </svg>
                      <span className="text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* Action Button */}
                <div className="text-center">
                  {plan.current ? (
                    <button className="w-full py-3 px-6 bg-green-600 text-white rounded-lg font-semibold cursor-default">
                      Current Plan
                    </button>
                  ) : (
                    <button 
                      onClick={() => handleUpgrade(plan.id)}
                      className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                        plan.popular 
                          ? 'btn-primary' 
                          : 'bg-gray-700 text-white hover:bg-gray-600'
                      }`}
                    >
                      {plan.price === 0 ? 'Get Started Free' : `Upgrade to ${plan.name}`}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* FAQ Section */}
        <div className="max-w-4xl mx-auto mt-16">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Frequently Asked Questions</h2>
          
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-white mb-2">What happens when I exceed my daily query limit?</h3>
              <p className="text-gray-300">
                Once you reach your daily limit, you'll need to wait until the next day or upgrade to a higher plan. 
                Enterprise users get priority processing and can request temporary limit increases.
              </p>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-white mb-2">Can I cancel my subscription anytime?</h3>
              <p className="text-gray-300">
                Yes, you can cancel your subscription at any time. You'll continue to have access to your paid features 
                until the end of your current billing period.
              </p>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-white mb-2">Is my data secure and private?</h3>
              <p className="text-gray-300">
                Absolutely. We use enterprise-grade encryption and follow strict data protection policies. 
                Your queries and results are never shared with third parties and are automatically deleted 
                according to your plan's retention policy.
              </p>
            </div>
            
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
              <h3 className="text-lg font-semibold text-white mb-2">Do you offer custom enterprise solutions?</h3>
              <p className="text-gray-300">
                Yes! For organizations with specific requirements, we offer custom enterprise solutions with 
                dedicated infrastructure, custom integrations, and tailored pricing. Contact our sales team for more information.
              </p>
            </div>
          </div>
        </div>

        {/* Contact Section */}
        <div className="text-center mt-16">
          <h3 className="text-2xl font-bold text-white mb-4">Need a Custom Solution?</h3>
          <p className="text-gray-300 mb-6">
            Contact our sales team to discuss enterprise requirements and custom pricing.
          </p>
          <button className="btn-secondary">
            Contact Sales
          </button>
        </div>
      </div>
    </div>
  )
}