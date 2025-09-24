import Head from 'next/head'
import { useState, useEffect } from 'react'
import { 
  Search, Shield, Target, Zap, Users, BarChart3, Lock, Globe, 
  TrendingUp, Calendar, FileText, Download, Eye, Clock, 
  AlertTriangle, CheckCircle, XCircle, Activity, Database,
  Filter, Settings, Bell, User, LogOut, ChevronDown, Plus,
  Map, Smartphone, Mail, Link as LinkIcon, Image, Network,
  Brain, Radar, Fingerprint, Crosshair, Star, ArrowRight,
  Play, Pause, Volume2, ChevronLeft, ChevronRight, Quote,
  Award, Layers, Cpu, Cloud, GitBranch, Workflow, Zap as ZapIcon
} from 'lucide-react'

interface Testimonial {
  name: string
  role: string
  company: string
  avatar: string
  content: string
  rating: number
}

interface Feature {
  icon: React.ReactNode
  title: string
  description: string
  gradient: string
}

export default function Landing() {
  const [currentTestimonial, setCurrentTestimonial] = useState(0)
  const [isVideoPlaying, setIsVideoPlaying] = useState(false)
  const [hoveredFeature, setHoveredFeature] = useState<number | null>(null)

  const testimonials: Testimonial[] = [
    {
      name: "Sarah Chen",
      role: "Security Analyst",
      company: "CyberDefense Corp",
      avatar: "/api/placeholder/64/64",
      content: "This platform has revolutionized our threat intelligence gathering. The comprehensive scanner tools and real-time analysis have improved our incident response time by 60%.",
      rating: 5
    },
    {
      name: "Marcus Rodriguez",
      role: "Private Investigator",
      company: "Rodriguez Investigations",
      avatar: "/api/placeholder/64/64",
      content: "As a PI, I need reliable and comprehensive intelligence tools. This platform provides everything I need in one place - from social media analysis to public records searches.",
      rating: 5
    },
    {
      name: "Dr. Emily Watson",
      role: "Research Director",
      company: "Academic Research Institute",
      avatar: "/api/placeholder/64/64",
      content: "The AI-powered correlation and pattern recognition features have accelerated our research significantly. The compliance features ensure we stay within ethical boundaries.",
      rating: 5
    }
  ]

  const advancedFeatures: Feature[] = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms automatically correlate data patterns and identify relationships across multiple intelligence sources.",
      gradient: "from-purple-500 to-pink-500"
    },
    {
      icon: <Layers className="w-8 h-8" />,
      title: "Multi-Source Aggregation",
      description: "Seamlessly combine intelligence from 100+ sources including social media, public records, dark web, and proprietary databases.",
      gradient: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Enterprise Security",
      description: "Bank-grade encryption, role-based access control, and comprehensive audit logging ensure your operations remain secure and compliant.",
      gradient: "from-green-500 to-emerald-500"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "Real-Time Processing",
      description: "Parallel processing architecture delivers results in seconds, not hours. Live monitoring and instant alerts keep you ahead of threats.",
      gradient: "from-orange-500 to-red-500"
    },
    {
      icon: <Cloud className="w-8 h-8" />,
      title: "Scalable Infrastructure",
      description: "Cloud-native architecture scales automatically with your needs. Handle everything from single queries to enterprise-wide operations.",
      gradient: "from-indigo-500 to-purple-500"
    },
    {
      icon: <Workflow className="w-8 h-8" />,
      title: "Automated Workflows",
      description: "Create custom intelligence gathering workflows with automated triggers, notifications, and report generation.",
      gradient: "from-teal-500 to-green-500"
    }
  ]

  const industryLogos = [
    { name: "CyberSecurity", width: "w-32" },
    { name: "Law Enforcement", width: "w-28" },
    { name: "Financial Services", width: "w-36" },
    { name: "Private Investigation", width: "w-32" },
    { name: "Academic Research", width: "w-30" },
    { name: "Legal Services", width: "w-28" }
  ]

  const stats = [
    { value: "500M+", label: "Data Points Analyzed", icon: <Database className="w-6 h-6" /> },
    { value: "99.7%", label: "Uptime Guarantee", icon: <Activity className="w-6 h-6" /> },
    { value: "< 3s", label: "Average Response Time", icon: <ZapIcon className="w-6 h-6" /> },
    { value: "129", label: "Scanner Tools", icon: <Radar className="w-6 h-6" /> }
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [testimonials.length])

  return (
    <>
      <Head>
        <title>Intelligence Platform - Professional OSINT & Threat Intelligence</title>
        <meta name="description" content="Advanced intelligence gathering platform with 129 scanner tools, AI-powered analysis, and enterprise-grade security. Trusted by security professionals worldwide." />
        <meta name="keywords" content="OSINT, threat intelligence, cybersecurity, investigation, data analysis" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-slate-900 text-white overflow-hidden">
        {/* Animated Background */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-blue-900/20 to-purple-900/20" />
          <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
          <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-5" />
        </div>

        {/* Navigation */}
        <nav className="relative z-50 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <Radar className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold">Intelligence Platform</h1>
                  <p className="text-xs text-slate-400">Professional Grade</p>
                </div>
              </div>
              
              <div className="hidden md:flex space-x-8">
                <a href="#features" className="text-slate-300 hover:text-white transition-colors">Features</a>
                <a href="#solutions" className="text-slate-300 hover:text-white transition-colors">Solutions</a>
                <a href="#pricing" className="text-slate-300 hover:text-white transition-colors">Pricing</a>
                <a href="#testimonials" className="text-slate-300 hover:text-white transition-colors">Reviews</a>
                <a href="/dashboard" className="text-slate-300 hover:text-white transition-colors">Dashboard</a>
              </div>

              <div className="flex items-center space-x-4">
                <button className="text-slate-300 hover:text-white transition-colors">
                  Sign In
                </button>
                <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105">
                  Start Free Trial
                </button>
              </div>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="relative py-20 lg:py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div className="space-y-8">
                <div className="space-y-4">
                  <div className="inline-flex items-center space-x-2 bg-blue-500/10 border border-blue-500/20 rounded-full px-4 py-2">
                    <Award className="w-4 h-4 text-blue-400" />
                    <span className="text-sm text-blue-300">Trusted by 10,000+ Security Professionals</span>
                  </div>
                  
                  <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                    Advanced
                    <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                      {" "}Intelligence
                    </span>
                    <br />
                    Gathering Platform
                  </h1>
                  
                  <p className="text-xl text-slate-300 leading-relaxed">
                    Harness the power of 129 scanner tools, AI-driven analysis, and enterprise-grade security 
                    to gather comprehensive intelligence from across the digital landscape.
                  </p>
                </div>

                <div className="flex flex-col sm:flex-row gap-4">
                  <button className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 flex items-center justify-center space-x-2">
                    <span className="font-semibold">Start Free Trial</span>
                    <ArrowRight className="w-5 h-5" />
                  </button>
                  
                  <button 
                    onClick={() => setIsVideoPlaying(!isVideoPlaying)}
                    className="border border-slate-600 text-white px-8 py-4 rounded-xl hover:bg-slate-800 transition-all flex items-center justify-center space-x-2"
                  >
                    {isVideoPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                    <span>Watch Demo</span>
                  </button>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 pt-8">
                  {stats.map((stat, index) => (
                    <div key={index} className="text-center">
                      <div className="flex justify-center mb-2 text-blue-400">
                        {stat.icon}
                      </div>
                      <div className="text-2xl font-bold">{stat.value}</div>
                      <div className="text-sm text-slate-400">{stat.label}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Hero Visual */}
              <div className="relative">
                <div className="relative bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-slate-700 overflow-hidden">
                  {!isVideoPlaying ? (
                    <div className="aspect-video flex items-center justify-center bg-slate-800">
                      <button 
                        onClick={() => setIsVideoPlaying(true)}
                        className="w-20 h-20 bg-blue-600 rounded-full flex items-center justify-center hover:bg-blue-700 transition-colors transform hover:scale-110"
                      >
                        <Play className="w-8 h-8 text-white ml-1" />
                      </button>
                    </div>
                  ) : (
                    <div className="aspect-video bg-slate-800 p-4">
                      <div className="h-full bg-slate-900 rounded-lg border border-slate-700 flex items-center justify-center">
                        <div className="text-center">
                          <Activity className="w-12 h-12 text-blue-400 mx-auto mb-4 animate-pulse" />
                          <p className="text-slate-300">Live Platform Demo</p>
                          <p className="text-sm text-slate-400">Real-time intelligence gathering in action</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
                
                {/* Floating Elements */}
                <div className="absolute -top-4 -right-4 bg-green-500/20 border border-green-500/30 rounded-lg p-3 backdrop-blur-sm">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-5 h-5 text-green-400" />
                    <span className="text-sm text-green-300">99.7% Uptime</span>
                  </div>
                </div>
                
                <div className="absolute -bottom-4 -left-4 bg-blue-500/20 border border-blue-500/30 rounded-lg p-3 backdrop-blur-sm">
                  <div className="flex items-center space-x-2">
                    <ZapIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm text-blue-300">Sub-3s Response</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Trusted By Section */}
        <section className="py-16 border-y border-slate-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <p className="text-slate-400 text-lg">Trusted by industry leaders worldwide</p>
            </div>
            <div className="flex justify-center items-center space-x-12 opacity-60">
              {industryLogos.map((logo, index) => (
                <div key={index} className={`${logo.width} h-12 bg-slate-700 rounded flex items-center justify-center`}>
                  <span className="text-xs text-slate-400">{logo.name}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Advanced Features Section */}
        <section id="features" className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                Advanced Intelligence
                <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                  {" "}Capabilities
                </span>
              </h2>
              <p className="text-xl text-slate-300 max-w-3xl mx-auto">
                Powered by cutting-edge technology and designed for the most demanding intelligence operations
              </p>
            </div>

            <div className="grid lg:grid-cols-3 gap-8">
              {advancedFeatures.map((feature, index) => (
                <div
                  key={index}
                  onMouseEnter={() => setHoveredFeature(index)}
                  onMouseLeave={() => setHoveredFeature(null)}
                  className={`relative p-8 bg-slate-800/50 rounded-2xl border border-slate-700 hover:border-slate-600 transition-all duration-300 transform hover:scale-105 ${
                    hoveredFeature === index ? 'shadow-2xl shadow-blue-500/20' : ''
                  }`}
                >
                  <div className={`inline-flex p-3 rounded-xl bg-gradient-to-br ${feature.gradient} mb-6`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
                  <p className="text-slate-300 leading-relaxed">{feature.description}</p>
                  
                  {hoveredFeature === index && (
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 rounded-2xl pointer-events-none" />
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Testimonials Section */}
        <section id="testimonials" className="py-20 bg-slate-800/30">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                What Security Professionals
                <span className="bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
                  {" "}Are Saying
                </span>
              </h2>
            </div>

            <div className="relative max-w-4xl mx-auto">
              <div className="bg-slate-800/50 rounded-2xl border border-slate-700 p-8 lg:p-12">
                <div className="flex items-start space-x-6">
                  <Quote className="w-12 h-12 text-blue-400 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-lg lg:text-xl text-slate-200 leading-relaxed mb-6">
                      {testimonials[currentTestimonial].content}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                          <User className="w-6 h-6 text-white" />
                        </div>
                        <div>
                          <p className="font-semibold text-white">{testimonials[currentTestimonial].name}</p>
                          <p className="text-sm text-slate-400">
                            {testimonials[currentTestimonial].role} at {testimonials[currentTestimonial].company}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex space-x-1">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Navigation Dots */}
              <div className="flex justify-center space-x-3 mt-8">
                {testimonials.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentTestimonial(index)}
                    className={`w-3 h-3 rounded-full transition-colors ${
                      index === currentTestimonial ? 'bg-blue-500' : 'bg-slate-600 hover:bg-slate-500'
                    }`}
                  />
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 rounded-3xl p-12 lg:p-16 text-center">
              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                Ready to Transform Your Intelligence Operations?
              </h2>
              <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
                Join thousands of security professionals who trust our platform for their most critical intelligence gathering needs.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button className="bg-white text-slate-900 px-8 py-4 rounded-xl font-semibold hover:bg-slate-100 transition-all transform hover:scale-105">
                  Start 14-Day Free Trial
                </button>
                <button className="border border-white/30 text-white px-8 py-4 rounded-xl hover:bg-white/10 transition-all">
                  Schedule Demo
                </button>
              </div>
              
              <p className="text-sm text-blue-100 mt-6">
                No credit card required • Full access to all features • Cancel anytime
              </p>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="py-16 border-t border-slate-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid md:grid-cols-4 gap-8">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <Radar className="w-5 h-5 text-white" />
                  </div>
                  <span className="text-xl font-bold">Intelligence Platform</span>
                </div>
                <p className="text-slate-400">
                  Advanced intelligence gathering for the modern world.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Product</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">API</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Integrations</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Company</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Blog</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                </ul>
              </div>
              
              <div>
                <h4 className="font-semibold mb-4">Support</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Help Center</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Status</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                </ul>
              </div>
            </div>
            
            <div className="border-t border-slate-800 mt-12 pt-8 text-center text-slate-400">
              <p>&copy; 2024 Intelligence Platform. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  )
}