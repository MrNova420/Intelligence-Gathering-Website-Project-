import React, { useState, useEffect } from 'react'
import { motion, useAnimation } from 'framer-motion'
import { 
  Search, Shield, Zap, TrendingUp, Users, Globe,
  Brain, Radar, Target, Activity, Database, Network
} from 'lucide-react'
import { Button } from '../ui/Button'
import { Badge } from '../ui/Badge'
import { Input } from '../ui/Input'

interface ModernHeroProps {
  onGetStarted?: () => void
  onWatchDemo?: () => void
}

const ModernHero: React.FC<ModernHeroProps> = ({ onGetStarted, onWatchDemo }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [currentMetric, setCurrentMetric] = useState(0)
  const controls = useAnimation()

  // Animated metrics that cycle through different values
  const metrics = [
    { value: '129+', label: 'Intel Sources', icon: Database, color: 'text-blue-400' },
    { value: '97.8%', label: 'Accuracy Rate', icon: Target, color: 'text-green-400' },
    { value: '<0.5s', label: 'Response Time', icon: Zap, color: 'text-yellow-400' },
    { value: '500M+', label: 'Data Points', icon: Globe, color: 'text-purple-400' },
  ]

  // Real-time activity indicators
  const activities = [
    'Suspicious domain registered: malware-c2.com',
    'New social media profile linked to target entity',
    'Email validation completed: 94.7% confidence',
    'Phone number verified in 12 countries',
    'OSINT scan completed: 47 new data points',
  ]

  const [currentActivity, setCurrentActivity] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentMetric((prev) => (prev + 1) % metrics.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentActivity((prev) => (prev + 1) % activities.length)
    }, 4000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    controls.start({
      background: [
        'radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.1) 0%, transparent 50%)',
        'radial-gradient(circle at 80% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%)',
        'radial-gradient(circle at 40% 80%, rgba(6, 182, 212, 0.1) 0%, transparent 50%)',
      ],
      transition: { duration: 8, repeat: Infinity, repeatType: 'reverse' }
    })
  }, [controls])

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Animated Background */}
      <motion.div
        className="absolute inset-0 -z-10"
        animate={controls}
      />
      
      {/* Grid Pattern Overlay */}
      <div className="absolute inset-0 -z-10 opacity-20">
        <div 
          className="h-full w-full"
          style={{
            backgroundImage: `
              linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px)
            `,
            backgroundSize: '50px 50px'
          }}
        />
      </div>

      <div className="relative max-w-7xl mx-auto px-6 lg:px-8 pt-20 pb-16">
        {/* Status Bar */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center justify-center mb-8"
        >
          <Badge 
            variant="success" 
            dot 
            pulse 
            className="bg-green-500/10 border border-green-500/20"
          >
            SYSTEM OPERATIONAL - 99.97% UPTIME
          </Badge>
        </motion.div>

        {/* Main Hero Content */}
        <div className="text-center space-y-8">
          {/* Main Heading */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-4"
          >
            <h1 className="text-4xl sm:text-6xl lg:text-7xl font-bold tracking-tight">
              <span className="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                NEXT-GEN
              </span>
              <br />
              <span className="text-white">INTELLIGENCE</span>
              <br />
              <span className="bg-gradient-to-r from-purple-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent">
                PLATFORM
              </span>
            </h1>
            
            <p className="text-xl sm:text-2xl text-slate-300 max-w-4xl mx-auto leading-relaxed">
              Harness the power of{' '}
              <span className="text-blue-400 font-semibold">AI-driven analysis</span>,{' '}
              <span className="text-purple-400 font-semibold">real-time threat detection</span>, and{' '}
              <span className="text-cyan-400 font-semibold">comprehensive OSINT capabilities</span>{' '}
              in the world's most advanced intelligence gathering ecosystem.
            </p>
          </motion.div>

          {/* Interactive Search Preview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="max-w-2xl mx-auto"
          >
            <div className="relative">
              <Input
                variant="search"
                inputSize="lg"
                placeholder="Enter email, phone, username, or domain to analyze..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-slate-900/80 backdrop-blur-sm border-slate-600/50"
              />
              <motion.div
                className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-500 rounded-lg blur opacity-20"
                animate={{ opacity: [0.2, 0.4, 0.2] }}
                transition={{ duration: 2, repeat: Infinity }}
              />
            </div>
          </motion.div>

          {/* Animated Metrics */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="grid grid-cols-2 lg:grid-cols-4 gap-6 max-w-4xl mx-auto"
          >
            {metrics.map((metric, index) => {
              const Icon = metric.icon
              return (
                <motion.div
                  key={index}
                  className="text-center p-6 rounded-xl bg-slate-900/50 border border-slate-800/50 backdrop-blur-sm"
                  whileHover={{ scale: 1.05, y: -5 }}
                  animate={currentMetric === index ? { 
                    borderColor: ['rgba(59, 130, 246, 0.3)', 'rgba(139, 92, 246, 0.5)', 'rgba(59, 130, 246, 0.3)'],
                    scale: [1, 1.02, 1]
                  } : {}}
                  transition={{ duration: 0.5 }}
                >
                  <Icon className={`w-8 h-8 mx-auto mb-2 ${metric.color}`} />
                  <div className="text-2xl font-bold text-white">{metric.value}</div>
                  <div className="text-sm text-slate-400">{metric.label}</div>
                </motion.div>
              )
            })}
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Button
              size="lg"
              gradient
              leftIcon={<Radar className="w-5 h-5" />}
              rightIcon={<TrendingUp className="w-5 h-5" />}
              onClick={onGetStarted}
              className="px-8 py-4"
            >
              Launch Intelligence Ops
            </Button>
            
            <Button
              size="lg"
              variant="outline"
              leftIcon={<Activity className="w-5 h-5" />}
              onClick={onWatchDemo}
              className="px-8 py-4"
            >
              Watch Platform Demo
            </Button>
          </motion.div>

          {/* Trust Indicators */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            className="mt-16"
          >
            <p className="text-sm text-slate-500 mb-6">TRUSTED BY INDUSTRY LEADERS</p>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {[
                { stat: '87%', label: 'Fortune 500' },
                { stat: '120+', label: 'Government Agencies' },
                { stat: '500+', label: 'Security Firms' },
                { stat: '200+', label: 'Law Enforcement' },
              ].map((item, index) => (
                <div key={index} className="text-center">
                  <div className="text-2xl font-bold text-blue-400">{item.stat}</div>
                  <div className="text-sm text-slate-400">{item.label}</div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Live Activity Feed */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 1.2 }}
          className="fixed right-6 top-1/2 transform -translate-y-1/2 w-80 space-y-4 hidden xl:block"
        >
          <div className="bg-slate-900/80 backdrop-blur-sm border border-slate-700/50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              <Badge variant="success" dot pulse size="sm">
                Live Intelligence Feed
              </Badge>
            </div>
            
            <motion.div
              key={currentActivity}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-2"
            >
              <p className="text-sm text-slate-200">{activities[currentActivity]}</p>
              <p className="text-xs text-slate-500">
                {Math.floor(Math.random() * 10) + 1}m ago
              </p>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export { ModernHero }