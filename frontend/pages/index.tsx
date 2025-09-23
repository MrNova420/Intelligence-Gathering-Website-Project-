import Head from 'next/head'
import { useState } from 'react'
import { Search, Shield, Target, Zap, Users, BarChart3, Lock, Globe } from 'lucide-react'

interface QueryForm {
  type: string
  value: string
}

export default function Home() {
  const [query, setQuery] = useState<QueryForm>({ type: 'email', value: '' })
  const [isScanning, setIsScanning] = useState(false)
  const [results, setResults] = useState<any>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.value.trim()) return

    setIsScanning(true)
    
    // Simulate API call
    setTimeout(() => {
      setResults({
        query: query.value,
        type: query.type,
        scanners_used: 87,
        sources_found: 23,
        confidence_score: 0.85,
        preview_data: {
          social_profiles: 5,
          public_records: 8,
          email_verification: 'verified',
          phone_lookup: '+1 555-***-****',
          location: 'San Francisco, CA'
        }
      })
      setIsScanning(false)
    }, 3000)
  }

  const scannerTypes = [
    { id: 'email', label: 'Email Address', icon: '📧' },
    { id: 'phone', label: 'Phone Number', icon: '📱' },
    { id: 'name', label: 'Full Name', icon: '👤' },
    { id: 'username', label: 'Username', icon: '🔍' },
    { id: 'image', label: 'Image/Photo', icon: '🖼️' },
  ]

  const features = [
    {
      icon: <Target className="w-8 h-8 text-primary-600" />,
      title: '100+ Scanner Tools',
      description: 'Comprehensive intelligence gathering across multiple data sources'
    },
    {
      icon: <Shield className="w-8 h-8 text-primary-600" />,
      title: 'Legal & Compliant',
      description: 'Only public data sources, GDPR/CCPA compliant operations'
    },
    {
      icon: <Zap className="w-8 h-8 text-primary-600" />,
      title: 'Real-time Results',
      description: 'Fast parallel scanning with confidence scoring'
    },
    {
      icon: <Lock className="w-8 h-8 text-primary-600" />,
      title: 'Secure & Private',
      description: 'End-to-end encryption and secure data handling'
    }
  ]

  return (
    <>
      <Head>
        <title>Intelligence Gathering Platform - 100+ Scanner Tools</title>
        <meta name="description" content="Professional intelligence gathering platform with 100+ scanner tools for comprehensive OSINT research" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-primary-900">
        {/* Header */}
        <header className="bg-dark-900/50 backdrop-blur-sm border-b border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
                  <Search className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">Intelligence Platform</h1>
                  <p className="text-gray-400 text-sm">100+ Scanner Tools</p>
                </div>
              </div>
              <nav className="flex space-x-6">
                <a href="#" className="text-gray-300 hover:text-white transition-colors">Dashboard</a>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">Reports</a>
                <a href="#" className="text-gray-300 hover:text-white transition-colors">API</a>
                <button className="btn-primary">
                  Login
                </button>
              </nav>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl font-bold text-white mb-6">
              Professional Intelligence Gathering
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Comprehensive OSINT research with 100+ scanner tools. Gather intelligence from 
              social media, public records, APIs, and more - all in one platform.
            </p>
            
            {/* Search Form */}
            <div className="max-w-2xl mx-auto">
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-5 gap-2 mb-4">
                  {scannerTypes.map((type) => (
                    <button
                      key={type.id}
                      type="button"
                      onClick={() => setQuery({ ...query, type: type.id })}
                      className={`p-3 rounded-lg border transition-all ${
                        query.type === type.id
                          ? 'bg-primary-600 border-primary-500 text-white'
                          : 'bg-white/10 border-gray-600 text-gray-300 hover:bg-white/20'
                      }`}
                    >
                      <div className="text-2xl mb-1">{type.icon}</div>
                      <div className="text-xs">{type.label}</div>
                    </button>
                  ))}
                </div>
                
                <div className="flex space-x-3">
                  <input
                    type="text"
                    value={query.value}
                    onChange={(e) => setQuery({ ...query, value: e.target.value })}
                    placeholder={`Enter ${scannerTypes.find(t => t.id === query.type)?.label.toLowerCase()} to investigate...`}
                    className="flex-1 px-4 py-3 rounded-lg bg-white/10 border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    disabled={isScanning}
                  />
                  <button
                    type="submit"
                    disabled={isScanning || !query.value.trim()}
                    className="btn-primary px-8 py-3 text-lg disabled:opacity-50"
                  >
                    {isScanning ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
                        <span>Scanning...</span>
                      </div>
                    ) : (
                      'Start Scan'
                    )}
                  </button>
                </div>
              </form>
            </div>

            {/* Scanning Progress */}
            {isScanning && (
              <div className="mt-8 max-w-2xl mx-auto">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
                  <div className="flex items-center justify-center space-x-3 mb-4">
                    <div className="w-8 h-8 border-2 border-primary-500/20 border-t-primary-500 rounded-full animate-spin"></div>
                    <span className="text-white font-medium">Running 100+ scanner tools...</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-primary-500 to-blue-500 h-2 rounded-full animate-pulse" style={{width: '70%'}}></div>
                  </div>
                  <div className="mt-3 text-sm text-gray-400 text-center">
                    Checking social media, public records, APIs, and more...
                  </div>
                </div>
              </div>
            )}

            {/* Results Preview */}
            {results && !isScanning && (
              <div className="mt-8 max-w-4xl mx-auto">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
                  <div className="text-center mb-6">
                    <h3 className="text-2xl font-bold text-white mb-2">Scan Complete!</h3>
                    <p className="text-gray-300">Found intelligence data from {results.sources_found} sources</p>
                  </div>
                  
                  <div className="grid md:grid-cols-3 gap-6 mb-6">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-primary-400">{results.scanners_used}</div>
                      <div className="text-gray-400">Scanners Used</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-400">{results.sources_found}</div>
                      <div className="text-gray-400">Sources Found</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-yellow-400">{Math.round(results.confidence_score * 100)}%</div>
                      <div className="text-gray-400">Confidence</div>
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-4 text-left">
                    <div className="bg-black/20 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Social Profiles</h4>
                      <p className="text-gray-300">{results.preview_data.social_profiles} profiles found</p>
                    </div>
                    <div className="bg-black/20 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Public Records</h4>
                      <p className="text-gray-300">{results.preview_data.public_records} records found</p>
                    </div>
                    <div className="bg-black/20 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Email Status</h4>
                      <p className="text-gray-300 capitalize">{results.preview_data.email_verification}</p>
                    </div>
                    <div className="bg-black/20 rounded-lg p-4">
                      <h4 className="font-semibold text-white mb-2">Location</h4>
                      <p className="text-gray-300">{results.preview_data.location}</p>
                    </div>
                  </div>

                  <div className="mt-6 text-center">
                    <p className="text-gray-400 mb-4">This is a preview. Upgrade for full detailed reports.</p>
                    <div className="space-x-3">
                      <button className="btn-primary">
                        Get Full Report ($9.99)
                      </button>
                      <button className="btn-secondary">
                        Download Preview
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 bg-black/20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-bold text-white mb-4">Comprehensive Intelligence Platform</h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Powered by 100+ scanner tools and integrated with leading intelligence sources
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="text-center">
                  <div className="w-16 h-16 bg-primary-600/10 rounded-full flex items-center justify-center mx-auto mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </div>
              ))}
            </div>

            {/* Scanner Categories */}
            <div className="mt-20">
              <h3 className="text-2xl font-bold text-white text-center mb-12">Scanner Categories</h3>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {[
                  { name: 'Social Media', count: 20, icon: '📱' },
                  { name: 'Email Intelligence', count: 15, icon: '📧' },
                  { name: 'Public Records', count: 25, icon: '📋' },
                  { name: 'Phone Lookup', count: 10, icon: '☎️' },
                  { name: 'Search Engines', count: 15, icon: '🔍' },
                  { name: 'Image Analysis', count: 15, icon: '🖼️' },
                  { name: 'Network Intel', count: 8, icon: '🌐' },
                  { name: 'AI Correlation', count: 5, icon: '🤖' }
                ].map((category, index) => (
                  <div key={index} className="bg-white/5 rounded-lg p-6 border border-gray-700 hover:bg-white/10 transition-colors">
                    <div className="text-3xl mb-3">{category.icon}</div>
                    <h4 className="font-semibold text-white mb-1">{category.name}</h4>
                    <p className="text-gray-400">{category.count} tools</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="bg-dark-900 py-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center">
              <div className="flex items-center justify-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                  <Search className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">Intelligence Platform</span>
              </div>
              <p className="text-gray-400 mb-4">
                Professional intelligence gathering with 100+ scanner tools
              </p>
              <div className="flex justify-center space-x-6 text-sm text-gray-400">
                <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
                <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
                <a href="#" className="hover:text-white transition-colors">API Documentation</a>
                <a href="#" className="hover:text-white transition-colors">Support</a>
              </div>
              <p className="text-gray-500 text-sm mt-4">
                © 2024 Intelligence Platform. All rights reserved.
              </p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}