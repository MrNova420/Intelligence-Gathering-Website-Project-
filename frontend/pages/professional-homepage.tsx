/**
 * Professional Intelligence Gathering Homepage
 * Industry-leading design inspired by Spokeo, Social Catfish, and BeenVerified
 * Enterprise-grade conversion optimization and user experience
 */

import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  MagnifyingGlassIcon, 
  ShieldCheckIcon, 
  ClockIcon,
  StarIcon,
  UserGroupIcon,
  DocumentTextIcon,
  GlobeAltIcon,
  CheckCircleIcon,
  ArrowRightIcon,
  PlayIcon
} from '@heroicons/react/24/outline';

// Professional component interfaces
interface SearchResult {
  id: string;
  name: string;
  location: string;
  confidence: number;
  preview: string;
}

interface TestimonialData {
  name: string;
  role: string;
  content: string;
  rating: number;
  avatar: string;
}

interface FeatureData {
  icon: React.ComponentType<any>;
  title: string;
  description: string;
  highlight: string;
}

const ProfessionalHomePage: NextPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState<'person' | 'email' | 'phone'>('person');
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  // Professional testimonials data
  const testimonials: TestimonialData[] = [
    {
      name: "Sarah Johnson",
      role: "Private Investigator",
      content: "This platform has revolutionized my investigations. The accuracy and depth of information is unmatched in the industry.",
      rating: 5,
      avatar: "/api/placeholder/64/64"
    },
    {
      name: "Michael Chen",
      role: "Background Check Specialist", 
      content: "Finally found a service that delivers comprehensive reports instantly. The professional presentation makes client delivery seamless.",
      rating: 5,
      avatar: "/api/placeholder/64/64"
    },
    {
      name: "Jennifer Davis",
      role: "HR Director",
      content: "The most reliable people search platform we've used. Enterprise features and compliance make it perfect for business use.",
      rating: 5,
      avatar: "/api/placeholder/64/64"
    }
  ];

  // Professional features showcase
  const features: FeatureData[] = [
    {
      icon: MagnifyingGlassIcon,
      title: "Advanced People Search",
      description: "Find anyone with just a name, email, or phone number using our AI-powered search algorithms.",
      highlight: "99.2% accuracy rate"
    },
    {
      icon: ShieldCheckIcon,
      title: "Background Verification",
      description: "Comprehensive background checks including criminal records, court documents, and public records.",
      highlight: "Legal & compliant"
    },
    {
      icon: GlobeAltIcon,
      title: "Social Media Intelligence",
      description: "Discover social profiles, connections, and digital footprints across 50+ platforms.",
      highlight: "50+ platforms"
    },
    {
      icon: DocumentTextIcon,
      title: "Professional Reports",
      description: "Detailed, publication-ready reports in PDF, HTML, and Excel formats.",
      highlight: "Multiple formats"
    }
  ];

  // Auto-rotate testimonials
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials.length]);

  // Professional search handler
  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    
    setIsSearching(true);
    
    // Simulate professional search experience
    setTimeout(() => {
      setIsSearching(false);
      setShowResults(true);
    }, 2500);
  };

  // Mock search results for demonstration
  const mockResults: SearchResult[] = [
    {
      id: '1',
      name: 'John Smith',
      location: 'San Francisco, CA',
      confidence: 98,
      preview: 'Software Engineer, 34 years old, 3 known addresses...'
    },
    {
      id: '2', 
      name: 'John M. Smith',
      location: 'Los Angeles, CA',
      confidence: 87,
      preview: 'Business Owner, 42 years old, 2 known phone numbers...'
    }
  ];

  return (
    <>
      <Head>
        <title>Intelligence Pro - Professional People Search & Background Checks</title>
        <meta name="description" content="Industry-leading people search, background checks, and social media intelligence. Trusted by professionals worldwide." />
        <meta name="keywords" content="people search, background check, social media intelligence, public records, reverse lookup" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Professional Navigation */}
      <nav className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Intelligence Pro
                </h1>
              </div>
            </div>
            
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-8">
                <Link href="/search" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Search
                </Link>
                <Link href="/pricing" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Pricing
                </Link>
                <Link href="/reports" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Sample Reports
                </Link>
                <Link href="/login" className="text-blue-600 hover:text-blue-800 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Sign In
                </Link>
                <Link href="/signup" className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                  Get Started
                </Link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section - Professional Design */}
      <section className="bg-gradient-to-br from-blue-50 via-white to-purple-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 leading-tight mb-6">
                Professional
                <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent block">
                  People Intelligence
                </span>
              </h1>
              
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Industry-leading people search, background verification, and social media intelligence. 
                Trusted by investigators, HR professionals, and businesses worldwide.
              </p>

              {/* Trust Indicators */}
              <div className="flex items-center space-x-8 mb-8">
                <div className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                  <span className="text-sm font-medium text-gray-700">99.2% Accuracy</span>
                </div>
                <div className="flex items-center">
                  <ShieldCheckIcon className="h-5 w-5 text-blue-500 mr-2" />
                  <span className="text-sm font-medium text-gray-700">GDPR Compliant</span>
                </div>
                <div className="flex items-center">
                  <ClockIcon className="h-5 w-5 text-purple-500 mr-2" />
                  <span className="text-sm font-medium text-gray-700">Instant Results</span>
                </div>
              </div>

              {/* Call-to-Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-4">
                <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl">
                  Start Free Search
                </button>
                <button className="flex items-center justify-center border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-blue-600 hover:text-blue-600 transition-all duration-300">
                  <PlayIcon className="h-5 w-5 mr-2" />
                  Watch Demo
                </button>
              </div>
            </motion.div>

            {/* Professional Search Interface */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="bg-white rounded-2xl shadow-2xl p-8 border border-gray-100"
            >
              <div className="mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Try It Now</h3>
                <p className="text-gray-600">Search millions of records instantly</p>
              </div>

              {/* Search Type Selector */}
              <div className="flex space-x-2 mb-6">
                {[
                  { type: 'person' as const, label: 'Person', icon: UserGroupIcon },
                  { type: 'email' as const, label: 'Email', icon: MagnifyingGlassIcon },
                  { type: 'phone' as const, label: 'Phone', icon: GlobeAltIcon }
                ].map(({ type, label, icon: Icon }) => (
                  <button
                    key={type}
                    onClick={() => setSearchType(type)}
                    className={`flex items-center px-4 py-2 rounded-lg font-medium transition-all ${
                      searchType === type
                        ? 'bg-blue-600 text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="h-4 w-4 mr-2" />
                    {label}
                  </button>
                ))}
              </div>

              {/* Search Input */}
              <div className="relative mb-6">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder={
                    searchType === 'person' ? 'Enter name (e.g., John Smith)' :
                    searchType === 'email' ? 'Enter email address' :
                    'Enter phone number'
                  }
                  className="w-full px-6 py-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:outline-none transition-colors"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button
                  onClick={handleSearch}
                  disabled={isSearching || !searchTerm.trim()}
                  className="absolute right-2 top-2 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isSearching ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2"></div>
                      Searching...
                    </div>
                  ) : (
                    <>Search</>
                  )}
                </button>
              </div>

              {/* Search Results Preview */}
              <AnimatePresence>
                {showResults && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-3"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="font-semibold text-gray-900">Found {mockResults.length} matches</h4>
                      <span className="text-sm text-blue-600 font-medium">Upgrade for full results</span>
                    </div>
                    
                    {mockResults.map((result) => (
                      <div key={result.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors cursor-pointer">
                        <div className="flex items-center justify-between mb-2">
                          <h5 className="font-semibold text-gray-900">{result.name}</h5>
                          <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                            {result.confidence}% match
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{result.location}</p>
                        <p className="text-sm text-gray-500">{result.preview}</p>
                        <button className="text-blue-600 text-sm font-medium mt-2 hover:text-blue-800 transition-colors">
                          View Full Report →
                        </button>
                      </div>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Social Proof Section */}
      <section className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Trusted by Professionals Worldwide</h2>
            <p className="text-xl text-gray-600">Join thousands of investigators, HR professionals, and businesses</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 items-center opacity-60">
            {/* Placeholder for professional logos */}
            <div className="text-center">
              <div className="bg-gray-200 h-12 rounded-lg flex items-center justify-center">
                <span className="font-bold text-gray-500">CLIENT LOGO</span>
              </div>
            </div>
            <div className="text-center">
              <div className="bg-gray-200 h-12 rounded-lg flex items-center justify-center">
                <span className="font-bold text-gray-500">CLIENT LOGO</span>
              </div>
            </div>
            <div className="text-center">
              <div className="bg-gray-200 h-12 rounded-lg flex items-center justify-center">
                <span className="font-bold text-gray-500">CLIENT LOGO</span>
              </div>
            </div>
            <div className="text-center">
              <div className="bg-gray-200 h-12 rounded-lg flex items-center justify-center">
                <span className="font-bold text-gray-500">CLIENT LOGO</span>
              </div>
            </div>
          </div>

          {/* Statistics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">500M+</div>
              <div className="text-gray-600">Records Searched</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">99.2%</div>
              <div className="text-gray-600">Accuracy Rate</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">10K+</div>
              <div className="text-gray-600">Professional Users</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Industry-Leading Intelligence Capabilities
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Professional-grade tools and data sources that deliver comprehensive, 
              accurate results for your most demanding investigations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
              >
                <div className="bg-gradient-to-br from-blue-50 to-purple-50 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                  <feature.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 mb-4 leading-relaxed">{feature.description}</p>
                <div className="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-medium inline-block">
                  {feature.highlight}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">What Professionals Say</h2>
            <p className="text-xl text-gray-600">Real feedback from industry experts</p>
          </div>

          <div className="max-w-4xl mx-auto">
            <AnimatePresence mode="wait">
              <motion.div
                key={currentTestimonial}
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.5 }}
                className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-2xl p-8 text-center"
              >
                <div className="flex justify-center mb-4">
                  {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                    <StarIcon key={i} className="h-6 w-6 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <blockquote className="text-xl text-gray-700 mb-8 leading-relaxed">
                  "{testimonials[currentTestimonial].content}"
                </blockquote>
                
                <div className="flex items-center justify-center">
                  <img
                    src={testimonials[currentTestimonial].avatar}
                    alt={testimonials[currentTestimonial].name}
                    className="w-12 h-12 rounded-full mr-4"
                  />
                  <div className="text-left">
                    <div className="font-semibold text-gray-900">
                      {testimonials[currentTestimonial].name}
                    </div>
                    <div className="text-gray-600">
                      {testimonials[currentTestimonial].role}
                    </div>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>

            {/* Testimonial Navigation */}
            <div className="flex justify-center mt-8 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-all ${
                    index === currentTestimonial ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Preview Section */}
      <section className="bg-gradient-to-br from-blue-600 to-purple-700 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Professional Plans for Every Need
            </h2>
            <p className="text-xl text-blue-100">
              From individual searches to enterprise solutions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Basic Plan */}
            <div className="bg-white rounded-2xl p-8 relative">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Basic</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$9.99</span>
                <span className="text-gray-600 ml-2">per report</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Basic background check</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Contact information</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Social media profiles</span>
                </li>
              </ul>
              <button className="w-full bg-gray-100 text-gray-900 py-3 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
                Get Started
              </button>
            </div>

            {/* Professional Plan */}
            <div className="bg-white rounded-2xl p-8 relative border-4 border-blue-500">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                  Most Popular
                </span>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Professional</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$29.99</span>
                <span className="text-gray-600 ml-2">per month</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Unlimited searches</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Comprehensive reports</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Criminal records</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Property records</span>
                </li>
              </ul>
              <button className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                Start Free Trial
              </button>
            </div>

            {/* Enterprise Plan */}
            <div className="bg-white rounded-2xl p-8 relative">
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Enterprise</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">Custom</span>
                <span className="text-gray-600 ml-2">pricing</span>
              </div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">API access</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">White-label reports</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Priority support</span>
                </li>
                <li className="flex items-center">
                  <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3" />
                  <span className="text-gray-700">Custom integrations</span>
                </li>
              </ul>
              <button className="w-full bg-purple-600 text-white py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors">
                Contact Sales
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA Section */}
      <section className="bg-white py-20">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of professionals who trust Intelligence Pro for their investigation needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 transition-all duration-300 shadow-lg hover:shadow-xl">
              Start Free Trial
            </button>
            <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl font-semibold text-lg hover:border-blue-600 hover:text-blue-600 transition-all duration-300">
              View Sample Report
            </button>
          </div>
        </div>
      </section>

      {/* Professional Footer */}
      <footer className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Intelligence Pro
              </h3>
              <p className="text-gray-400 mb-4">
                Professional people search and background verification platform trusted by industry experts.
              </p>
              <div className="flex space-x-4">
                {/* Social media links would go here */}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Services</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/people-search" className="hover:text-white transition-colors">People Search</Link></li>
                <li><Link href="/background-check" className="hover:text-white transition-colors">Background Checks</Link></li>
                <li><Link href="/reverse-lookup" className="hover:text-white transition-colors">Reverse Lookup</Link></li>
                <li><Link href="/social-media" className="hover:text-white transition-colors">Social Media Intelligence</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">About Us</Link></li>
                <li><Link href="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">Contact</Link></li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/help" className="hover:text-white transition-colors">Help Center</Link></li>
                <li><Link href="/api-docs" className="hover:text-white transition-colors">API Documentation</Link></li>
                <li><Link href="/status" className="hover:text-white transition-colors">System Status</Link></li>
                <li><Link href="/support" className="hover:text-white transition-colors">Contact Support</Link></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400">
              © 2024 Intelligence Pro. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">Privacy</Link>
              <Link href="/terms" className="text-gray-400 hover:text-white transition-colors">Terms</Link>
              <Link href="/cookies" className="text-gray-400 hover:text-white transition-colors">Cookies</Link>
            </div>
          </div>
        </div>
      </footer>
    </>
  );
};

export default ProfessionalHomePage;