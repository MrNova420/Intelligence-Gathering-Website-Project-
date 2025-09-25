/**
 * Professional Search Page
 * Advanced search interface similar to Spokeo, Social Catfish with conversion optimization
 */

import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import {
  MagnifyingGlassIcon,
  UserIcon,
  EnvelopeIcon,
  DevicePhoneMobileIcon,
  MapPinIcon,
  CalendarIcon,
  ShieldCheckIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XMarkIcon,
  EyeIcon,
  StarIcon,
  CreditCardIcon
} from '@heroicons/react/24/outline';

interface SearchResult {
  id: string;
  name: string;
  age?: number;
  location: string;
  confidence: number;
  preview: {
    addresses: string[];
    phones: string[];
    emails: string[];
    relatives: string[];
    socialProfiles: number;
  };
  riskLevel: 'low' | 'medium' | 'high';
  isPremium: boolean;
}

interface SearchFilters {
  location?: string;
  ageRange?: { min: number; max: number };
  includeRelatives?: boolean;
  includeCriminalRecords?: boolean;
}

const SearchPage: NextPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchType, setSearchType] = useState<'person' | 'email' | 'phone'>('person');
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<SearchFilters>({});
  const [selectedResult, setSelectedResult] = useState<SearchResult | null>(null);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);

  // Mock search results
  const mockResults: SearchResult[] = [
    {
      id: '1',
      name: 'John David Smith',
      age: 34,
      location: 'San Francisco, CA',
      confidence: 98,
      preview: {
        addresses: ['123 Market St, San Francisco, CA', '456 Oak Ave, Berkeley, CA'],
        phones: ['(415) 555-0123', '(510) 555-0456'],
        emails: ['john.smith@email.com', 'j.smith@company.com'],
        relatives: ['Sarah Smith', 'Michael Smith', 'Jennifer Davis'],
        socialProfiles: 5
      },
      riskLevel: 'low',
      isPremium: false
    },
    {
      id: '2',
      name: 'John Michael Smith',
      age: 42,
      location: 'Los Angeles, CA',
      confidence: 87,
      preview: {
        addresses: ['789 Sunset Blvd, Los Angeles, CA'],
        phones: ['(323) 555-0789'],
        emails: ['johnm.smith@email.com'],
        relatives: ['Maria Smith', 'David Smith Jr.'],
        socialProfiles: 3
      },
      riskLevel: 'medium',
      isPremium: true
    },
    {
      id: '3',
      name: 'John Robert Smith',
      age: 28,
      location: 'Sacramento, CA',
      confidence: 75,
      preview: {
        addresses: ['321 Pine St, Sacramento, CA'],
        phones: ['(916) 555-0321'],
        emails: ['jr.smith@domain.com'],
        relatives: ['Lisa Smith', 'Robert Smith Sr.'],
        socialProfiles: 7
      },
      riskLevel: 'high',
      isPremium: true
    }
  ];

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;
    
    setIsSearching(true);
    
    // Simulate search delay
    setTimeout(() => {
      setResults(mockResults);
      setIsSearching(false);
    }, 2000);
  };

  const getRiskBadgeColor = (level: string) => {
    switch (level) {
      case 'low': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const handleViewFullReport = (result: SearchResult) => {
    if (result.isPremium) {
      setShowUpgradeModal(true);
    } else {
      setSelectedResult(result);
    }
  };

  return (
    <>
      <Head>
        <title>Advanced People Search - Intelligence Pro</title>
        <meta name="description" content="Search millions of records instantly. Find anyone with our advanced people search technology." />
      </Head>

      {/* Navigation */}
      <nav className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Intelligence Pro
            </Link>
            
            <div className="flex items-center space-x-4">
              <Link href="/pricing" className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
                Pricing
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

      <div className="min-h-screen bg-gray-50">
        {/* Search Header */}
        <section className="bg-gradient-to-br from-blue-600 to-purple-700 py-12">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-white mb-4">
                Advanced People Search
              </h1>
              <p className="text-xl text-blue-100">
                Search millions of public records instantly
              </p>
            </div>

            {/* Search Interface */}
            <div className="bg-white rounded-2xl shadow-2xl p-8">
              {/* Search Type Selector */}
              <div className="flex justify-center space-x-4 mb-6">
                {[
                  { type: 'person' as const, label: 'Person', icon: UserIcon },
                  { type: 'email' as const, label: 'Email', icon: EnvelopeIcon },
                  { type: 'phone' as const, label: 'Phone', icon: DevicePhoneMobileIcon }
                ].map(({ type, label, icon: Icon }) => (
                  <button
                    key={type}
                    onClick={() => setSearchType(type)}
                    className={`flex items-center px-6 py-3 rounded-xl font-medium transition-all ${
                      searchType === type
                        ? 'bg-blue-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    <Icon className="h-5 w-5 mr-2" />
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
                    searchType === 'person' ? 'Enter full name (e.g., John Smith)' :
                    searchType === 'email' ? 'Enter email address' :
                    'Enter phone number'
                  }
                  className="w-full px-8 py-6 text-xl border-2 border-gray-200 rounded-2xl focus:border-blue-500 focus:outline-none transition-colors"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={handleSearch}
                  disabled={isSearching || !searchTerm.trim()}
                  className="flex-1 bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  {isSearching ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                      Searching...
                    </div>
                  ) : (
                    <>Search Now</>
                  )}
                </button>
                
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="px-6 py-4 border-2 border-gray-300 text-gray-700 rounded-xl font-semibold hover:border-blue-600 hover:text-blue-600 transition-all"
                >
                  Advanced Filters
                </button>
              </div>

              {/* Advanced Filters */}
              <AnimatePresence>
                {showFilters && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="mt-6 pt-6 border-t border-gray-200"
                  >
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Location
                        </label>
                        <input
                          type="text"
                          placeholder="City, State"
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                          value={filters.location || ''}
                          onChange={(e) => setFilters({ ...filters, location: e.target.value })}
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Age Range
                        </label>
                        <div className="grid grid-cols-2 gap-2">
                          <input
                            type="number"
                            placeholder="Min age"
                            className="px-4 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                            value={filters.ageRange?.min || ''}
                            onChange={(e) => setFilters({
                              ...filters,
                              ageRange: { ...filters.ageRange, min: parseInt(e.target.value) || 0, max: filters.ageRange?.max || 100 }
                            })}
                          />
                          <input
                            type="number"
                            placeholder="Max age"
                            className="px-4 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none"
                            value={filters.ageRange?.max || ''}
                            onChange={(e) => setFilters({
                              ...filters,
                              ageRange: { min: filters.ageRange?.min || 0, max: parseInt(e.target.value) || 100 }
                            })}
                          />
                        </div>
                      </div>
                    </div>
                    
                    <div className="mt-4 space-y-2">
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.includeRelatives || false}
                          onChange={(e) => setFilters({ ...filters, includeRelatives: e.target.checked })}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">Include relatives and associates</span>
                      </label>
                      
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={filters.includeCriminalRecords || false}
                          onChange={(e) => setFilters({ ...filters, includeCriminalRecords: e.target.checked })}
                          className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm text-gray-700">Include criminal background check</span>
                      </label>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </section>

        {/* Search Results */}
        {results.length > 0 && (
          <section className="py-12">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Search Results ({results.length} found)
                </h2>
                <p className="text-gray-600">
                  Showing results for "{searchTerm}" - {searchType} search
                </p>
              </div>

              <div className="space-y-6">
                {results.map((result) => (
                  <motion.div
                    key={result.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden hover:shadow-xl transition-all duration-300"
                  >
                    <div className="p-6">
                      {/* Result Header */}
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-2xl font-bold text-gray-900 mb-1">
                            {result.name}
                          </h3>
                          <div className="flex items-center space-x-4 text-gray-600">
                            {result.age && (
                              <span className="flex items-center">
                                <CalendarIcon className="h-4 w-4 mr-1" />
                                {result.age} years old
                              </span>
                            )}
                            <span className="flex items-center">
                              <MapPinIcon className="h-4 w-4 mr-1" />
                              {result.location}
                            </span>
                          </div>
                        </div>
                        
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskBadgeColor(result.riskLevel)}`}>
                            {result.riskLevel.toUpperCase()} RISK
                          </span>
                          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">
                            {result.confidence}% MATCH
                          </span>
                        </div>
                      </div>

                      {/* Preview Information */}
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                            <MapPinIcon className="h-4 w-4 mr-2 text-gray-500" />
                            Addresses ({result.preview.addresses.length})
                          </h4>
                          <div className="space-y-1">
                            {result.preview.addresses.slice(0, 2).map((address, idx) => (
                              <p key={idx} className="text-sm text-gray-600">
                                {result.isPremium ? '••• ••• ••••' : address}
                              </p>
                            ))}
                            {result.preview.addresses.length > 2 && (
                              <p className="text-xs text-blue-600 font-medium">
                                +{result.preview.addresses.length - 2} more
                              </p>
                            )}
                          </div>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                            <DevicePhoneMobileIcon className="h-4 w-4 mr-2 text-gray-500" />
                            Phones ({result.preview.phones.length})
                          </h4>
                          <div className="space-y-1">
                            {result.preview.phones.map((phone, idx) => (
                              <p key={idx} className="text-sm text-gray-600">
                                {result.isPremium ? '(•••) •••-••••' : phone}
                              </p>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                            <EnvelopeIcon className="h-4 w-4 mr-2 text-gray-500" />
                            Emails ({result.preview.emails.length})
                          </h4>
                          <div className="space-y-1">
                            {result.preview.emails.map((email, idx) => (
                              <p key={idx} className="text-sm text-gray-600">
                                {result.isPremium ? '•••@••••.com' : email}
                              </p>
                            ))}
                          </div>
                        </div>

                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                            <UserIcon className="h-4 w-4 mr-2 text-gray-500" />
                            Relatives ({result.preview.relatives.length})
                          </h4>
                          <div className="space-y-1">
                            {result.preview.relatives.slice(0, 2).map((relative, idx) => (
                              <p key={idx} className="text-sm text-gray-600">
                                {result.isPremium ? '••• ••••••' : relative}
                              </p>
                            ))}
                            {result.preview.relatives.length > 2 && (
                              <p className="text-xs text-blue-600 font-medium">
                                +{result.preview.relatives.length - 2} more
                              </p>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Additional Info */}
                      <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                        <div className="flex items-center space-x-4 text-sm text-gray-600">
                          <span className="flex items-center">
                            <StarIcon className="h-4 w-4 mr-1" />
                            {result.preview.socialProfiles} social profiles
                          </span>
                          <span className="flex items-center">
                            <ShieldCheckIcon className="h-4 w-4 mr-1" />
                            Background check available
                          </span>
                        </div>
                        
                        <div className="flex space-x-3">
                          <button
                            onClick={() => handleViewFullReport(result)}
                            className="bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors flex items-center"
                          >
                            <EyeIcon className="h-4 w-4 mr-2" />
                            View Full Report
                            {result.isPremium && (
                              <CreditCardIcon className="h-4 w-4 ml-2" />
                            )}
                          </button>
                          
                          <button className="border border-gray-300 text-gray-700 px-6 py-2 rounded-lg font-semibold hover:border-blue-600 hover:text-blue-600 transition-colors">
                            Save Result
                          </button>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Load More */}
              <div className="text-center mt-12">
                <button className="bg-gray-100 text-gray-700 px-8 py-3 rounded-xl font-semibold hover:bg-gray-200 transition-colors">
                  Load More Results
                </button>
              </div>
            </div>
          </section>
        )}

        {/* Upgrade Modal */}
        <AnimatePresence>
          {showUpgradeModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
            >
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.95, opacity: 0 }}
                className="bg-white rounded-2xl p-8 max-w-md w-full"
              >
                <div className="text-center">
                  <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CreditCardIcon className="h-8 w-8 text-blue-600" />
                  </div>
                  
                  <h3 className="text-2xl font-bold text-gray-900 mb-4">
                    Upgrade to View Full Report
                  </h3>
                  
                  <p className="text-gray-600 mb-6">
                    Access complete contact information, background details, and comprehensive reports.
                  </p>
                  
                  <div className="space-y-3 mb-6">
                    <div className="flex items-center text-left">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-sm text-gray-700">Unlimited searches</span>
                    </div>
                    <div className="flex items-center text-left">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-sm text-gray-700">Complete contact information</span>
                    </div>
                    <div className="flex items-center text-left">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-sm text-gray-700">Background check reports</span>
                    </div>
                    <div className="flex items-center text-left">
                      <CheckCircleIcon className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-sm text-gray-700">Social media profiles</span>
                    </div>
                  </div>
                  
                  <div className="flex space-x-3">
                    <button
                      onClick={() => setShowUpgradeModal(false)}
                      className="flex-1 border border-gray-300 text-gray-700 py-3 rounded-lg font-semibold hover:border-gray-400 transition-colors"
                    >
                      Cancel
                    </button>
                    <Link
                      href="/pricing"
                      className="flex-1 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center"
                    >
                      Upgrade Now
                    </Link>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
};

export default SearchPage;