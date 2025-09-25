/**
 * Professional Pricing Page
 * Optimized for conversion with industry-leading design patterns
 */

import React, { useState } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { motion } from 'framer-motion';
import {
  CheckCircleIcon,
  XMarkIcon,
  StarIcon,
  ShieldCheckIcon,
  BoltIcon,
  CreditCardIcon,
  UserGroupIcon,
  BuildingOfficeIcon,
  GlobeAltIcon,
  PhoneIcon,
  EnvelopeIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

interface PricingPlan {
  id: string;
  name: string;
  description: string;
  price: {
    monthly: number;
    yearly: number;
  };
  popular?: boolean;
  features: string[];
  limits: {
    searches: string;
    reports: string;
    support: string;
  };
  cta: string;
  ctaLink: string;
}

const PricingPage: NextPage = () => {
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly');
  const [showFAQ, setShowFAQ] = useState<number | null>(null);

  const plans: PricingPlan[] = [
    {
      id: 'basic',
      name: 'Basic',
      description: 'Perfect for occasional searches',
      price: { monthly: 9.99, yearly: 99 },
      features: [
        'Basic people search',
        'Contact information',
        'Social media profiles',
        'Address history (limited)',
        'Email support',
        'Mobile app access'
      ],
      limits: {
        searches: '10 per month',
        reports: 'Basic reports only',
        support: 'Email support'
      },
      cta: 'Get Started',
      ctaLink: '/signup?plan=basic'
    },
    {
      id: 'professional',
      name: 'Professional',
      description: 'Most popular for investigators',
      price: { monthly: 29.99, yearly: 299 },
      popular: true,
      features: [
        'Unlimited people searches',
        'Comprehensive background checks',
        'Criminal records access',
        'Property records',
        'Court documents',
        'Relatives & associates',
        'Phone & email validation',
        'Advanced social media intel',
        'Professional reports (PDF/Excel)',
        'Priority support',
        'API access (limited)',
        'Mobile app with offline sync'
      ],
      limits: {
        searches: 'Unlimited',
        reports: 'Professional reports',
        support: 'Priority phone & email'
      },
      cta: 'Start Free Trial',
      ctaLink: '/signup?plan=professional'
    },
    {
      id: 'enterprise',
      name: 'Enterprise',
      description: 'For teams and businesses',
      price: { monthly: 99.99, yearly: 999 },
      features: [
        'Everything in Professional',
        'Unlimited team members',
        'White-label reports',
        'Custom branding',
        'Full API access',
        'Bulk processing',
        'Advanced analytics dashboard',
        'Custom integrations',
        'Dedicated account manager',
        '24/7 phone support',
        'SLA guarantees',
        'Custom data sources',
        'Compliance reporting',
        'SSO integration'
      ],
      limits: {
        searches: 'Unlimited',
        reports: 'White-label reports',
        support: '24/7 dedicated support'
      },
      cta: 'Contact Sales',
      ctaLink: '/contact?plan=enterprise'
    }
  ];

  const faqs = [
    {
      question: 'How accurate is the information?',
      answer: 'Our platform maintains a 99.2% accuracy rate by aggregating data from thousands of public sources, official records, and verified databases. All information is cross-verified and updated in real-time.'
    },
    {
      question: 'Is this legal and compliant?',
      answer: 'Yes, we only access publicly available information and comply with all privacy laws including GDPR, CCPA, and FCRA. Our platform is designed for legitimate purposes such as background checks, investigations, and reconnecting with people.'
    },
    {
      question: 'Can I cancel anytime?',
      answer: 'Absolutely. You can cancel your subscription at any time from your account dashboard. There are no cancellation fees or long-term commitments required.'
    },
    {
      question: 'What payment methods do you accept?',
      answer: 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and for enterprise clients, we also accept wire transfers and purchase orders.'
    },
    {
      question: 'Do you offer refunds?',
      answer: 'Yes, we offer a 30-day money-back guarantee for all subscription plans. If you\'re not satisfied with our service, contact us within 30 days for a full refund.'
    },
    {
      question: 'How is my data protected?',
      answer: 'We use enterprise-grade security including AES-256 encryption, secure data centers, and strict access controls. Your searches and personal information are never shared with third parties.'
    }
  ];

  const getSavingsPercent = (monthly: number, yearly: number) => {
    const monthlyCost = monthly * 12;
    const savings = ((monthlyCost - yearly) / monthlyCost) * 100;
    return Math.round(savings);
  };

  return (
    <>
      <Head>
        <title>Pricing - Professional Intelligence Gathering Plans</title>
        <meta name="description" content="Choose the perfect plan for your intelligence gathering needs. From basic searches to enterprise solutions." />
      </Head>

      {/* Navigation */}
      <nav className="bg-white shadow-lg border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Intelligence Pro
            </Link>
            
            <div className="flex items-center space-x-4">
              <Link href="/search" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                Search
              </Link>
              <Link href="/login" className="text-blue-600 hover:text-blue-800 px-3 py-2 rounded-md text-sm font-medium">
                Sign In
              </Link>
              <Link href="/signup" className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg text-sm font-medium">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="bg-gray-50 min-h-screen">
        {/* Header Section */}
        <section className="bg-gradient-to-br from-blue-600 to-purple-700 py-20">
          <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h1 className="text-5xl font-bold text-white mb-6">
              Professional Plans for Every Need
            </h1>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of professionals who trust Intelligence Pro for their investigation needs
            </p>
            
            {/* Billing Toggle */}
            <div className="inline-flex items-center bg-white bg-opacity-20 rounded-xl p-1 backdrop-blur-sm">
              <button
                onClick={() => setBillingPeriod('monthly')}
                className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                  billingPeriod === 'monthly'
                    ? 'bg-white text-blue-700 shadow-lg'
                    : 'text-white hover:bg-white hover:bg-opacity-10'
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setBillingPeriod('yearly')}
                className={`px-6 py-3 rounded-lg font-semibold transition-all relative ${
                  billingPeriod === 'yearly'
                    ? 'bg-white text-blue-700 shadow-lg'
                    : 'text-white hover:bg-white hover:bg-opacity-10'
                }`}
              >
                Yearly
                <span className="absolute -top-2 -right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">
                  Save 17%
                </span>
              </button>
            </div>
          </div>
        </section>

        {/* Pricing Cards */}
        <section className="py-20 -mt-10">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {plans.map((plan, index) => (
                <motion.div
                  key={plan.id}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className={`bg-white rounded-2xl shadow-xl border-2 relative overflow-hidden ${
                    plan.popular ? 'border-blue-500 scale-105' : 'border-gray-200'
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute top-0 left-0 right-0 bg-gradient-to-r from-blue-500 to-purple-600 text-white text-center py-2 font-semibold text-sm">
                      Most Popular
                    </div>
                  )}
                  
                  <div className={`p-8 ${plan.popular ? 'pt-12' : ''}`}>
                    {/* Plan Header */}
                    <div className="text-center mb-8">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                      <p className="text-gray-600 mb-6">{plan.description}</p>
                      
                      <div className="mb-4">
                        <span className="text-5xl font-bold text-gray-900">
                          ${billingPeriod === 'monthly' ? plan.price.monthly : Math.round(plan.price.yearly / 12)}
                        </span>
                        <span className="text-gray-600 ml-2">
                          {billingPeriod === 'monthly' ? '/month' : '/month'}
                        </span>
                      </div>
                      
                      {billingPeriod === 'yearly' && (
                        <div className="text-center">
                          <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                            Save {getSavingsPercent(plan.price.monthly, plan.price.yearly)}% annually
                          </span>
                          <p className="text-sm text-gray-500 mt-2">
                            Billed ${plan.price.yearly} yearly
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Features List */}
                    <div className="mb-8">
                      <ul className="space-y-3">
                        {plan.features.map((feature, idx) => (
                          <li key={idx} className="flex items-start">
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                            <span className="text-gray-700 text-sm">{feature}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Limits */}
                    <div className="mb-8 p-4 bg-gray-50 rounded-lg">
                      <h4 className="font-semibold text-gray-900 mb-3">Plan Limits</h4>
                      <div className="space-y-2 text-sm text-gray-600">
                        <div className="flex justify-between">
                          <span>Searches:</span>
                          <span className="font-medium">{plan.limits.searches}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Reports:</span>
                          <span className="font-medium">{plan.limits.reports}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Support:</span>
                          <span className="font-medium">{plan.limits.support}</span>
                        </div>
                      </div>
                    </div>

                    {/* CTA Button */}
                    <Link
                      href={plan.ctaLink}
                      className={`block w-full text-center py-4 rounded-xl font-semibold text-lg transition-all ${
                        plan.popular
                          ? 'bg-blue-600 text-white hover:bg-blue-700 shadow-lg hover:shadow-xl'
                          : plan.id === 'enterprise'
                          ? 'bg-purple-600 text-white hover:bg-purple-700'
                          : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                      }`}
                    >
                      {plan.cta}
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Feature Comparison */}
        <section className="py-20 bg-white">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Compare All Features
              </h2>
              <p className="text-xl text-gray-600">
                See exactly what's included in each plan
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full bg-white rounded-2xl shadow-lg overflow-hidden">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left font-semibold text-gray-900">Features</th>
                    <th className="px-6 py-4 text-center font-semibold text-gray-900">Basic</th>
                    <th className="px-6 py-4 text-center font-semibold text-gray-900 bg-blue-50">
                      Professional
                      <span className="block text-xs text-blue-600 font-normal">Most Popular</span>
                    </th>
                    <th className="px-6 py-4 text-center font-semibold text-gray-900">Enterprise</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {[
                    { feature: 'People Search', basic: '10/month', pro: 'Unlimited', enterprise: 'Unlimited' },
                    { feature: 'Background Checks', basic: false, pro: true, enterprise: true },
                    { feature: 'Criminal Records', basic: false, pro: true, enterprise: true },
                    { feature: 'Professional Reports', basic: false, pro: true, enterprise: true },
                    { feature: 'API Access', basic: false, pro: 'Limited', enterprise: 'Full' },
                    { feature: 'White-label Reports', basic: false, pro: false, enterprise: true },
                    { feature: 'Team Members', basic: '1', pro: '5', enterprise: 'Unlimited' },
                    { feature: 'Priority Support', basic: false, pro: true, enterprise: true },
                    { feature: '24/7 Phone Support', basic: false, pro: false, enterprise: true },
                    { feature: 'Custom Integrations', basic: false, pro: false, enterprise: true }
                  ].map((row, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-6 py-4 font-medium text-gray-900">{row.feature}</td>
                      <td className="px-6 py-4 text-center">
                        {typeof row.basic === 'boolean' ? (
                          row.basic ? (
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mx-auto" />
                          ) : (
                            <XMarkIcon className="h-5 w-5 text-gray-300 mx-auto" />
                          )
                        ) : (
                          <span className="text-gray-700">{row.basic}</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-center bg-blue-50">
                        {typeof row.pro === 'boolean' ? (
                          row.pro ? (
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mx-auto" />
                          ) : (
                            <XMarkIcon className="h-5 w-5 text-gray-300 mx-auto" />
                          )
                        ) : (
                          <span className="text-gray-700 font-medium">{row.pro}</span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-center">
                        {typeof row.enterprise === 'boolean' ? (
                          row.enterprise ? (
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mx-auto" />
                          ) : (
                            <XMarkIcon className="h-5 w-5 text-gray-300 mx-auto" />
                          )
                        ) : (
                          <span className="text-gray-700">{row.enterprise}</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* Trust Indicators */}
        <section className="py-16 bg-gray-50">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Trusted by Industry Professionals
              </h2>
              <p className="text-xl text-gray-600">
                Join thousands who rely on Intelligence Pro daily
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="text-center">
                <div className="bg-white rounded-xl p-6 shadow-lg">
                  <UserGroupIcon className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                  <div className="text-3xl font-bold text-gray-900 mb-2">10,000+</div>
                  <div className="text-gray-600">Active Users</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="bg-white rounded-xl p-6 shadow-lg">
                  <BoltIcon className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                  <div className="text-3xl font-bold text-gray-900 mb-2">99.2%</div>
                  <div className="text-gray-600">Accuracy Rate</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="bg-white rounded-xl p-6 shadow-lg">
                  <ClockIcon className="h-12 w-12 text-green-600 mx-auto mb-4" />
                  <div className="text-3xl font-bold text-gray-900 mb-2">&lt;2s</div>
                  <div className="text-gray-600">Average Response</div>
                </div>
              </div>
              
              <div className="text-center">
                <div className="bg-white rounded-xl p-6 shadow-lg">
                  <ShieldCheckIcon className="h-12 w-12 text-red-600 mx-auto mb-4" />
                  <div className="text-3xl font-bold text-gray-900 mb-2">100%</div>
                  <div className="text-gray-600">GDPR Compliant</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-20 bg-white">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Frequently Asked Questions
              </h2>
              <p className="text-xl text-gray-600">
                Everything you need to know about our service
              </p>
            </div>

            <div className="space-y-6">
              {faqs.map((faq, index) => (
                <div key={index} className="bg-gray-50 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setShowFAQ(showFAQ === index ? null : index)}
                    className="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-100 transition-colors"
                  >
                    <span className="font-semibold text-gray-900">{faq.question}</span>
                    <div className={`transform transition-transform ${showFAQ === index ? 'rotate-180' : ''}`}>
                      <svg className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                  </button>
                  
                  {showFAQ === index && (
                    <div className="px-6 pb-4">
                      <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="bg-gradient-to-br from-blue-600 to-purple-700 py-20">
          <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Get Started?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of professionals who trust Intelligence Pro for their investigation needs.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/signup?plan=professional"
                className="bg-white text-blue-700 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Start Free Trial
              </Link>
              <Link
                href="/search"
                className="border-2 border-white text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white hover:text-blue-700 transition-all duration-300"
              >
                Try Free Search
              </Link>
            </div>
            
            <p className="text-blue-100 mt-6 text-sm">
              No credit card required • 30-day money-back guarantee
            </p>
          </div>
        </section>
      </div>
    </>
  );
};

export default PricingPage;