import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  TrendingUp, TrendingDown, Activity, Users, Globe, 
  Shield, Zap, Database, Eye, Target, Brain, Search
} from 'lucide-react'
import { Card, CardHeader, CardContent } from '../ui/Card'
import { Badge, StatusBadge } from '../ui/Badge'
import { Button } from '../ui/Button'

interface MetricCard {
  id: string
  title: string
  value: string
  change: string
  trend: 'up' | 'down' | 'stable'
  icon: React.ReactNode
  color: string
}

interface LiveActivity {
  id: string
  type: 'scan' | 'alert' | 'analysis' | 'discovery'
  message: string
  timestamp: string
  severity: 'low' | 'medium' | 'high' | 'critical'
}

const ModernDashboard: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date())
  const [activities, setActivities] = useState<LiveActivity[]>([])
  const [metrics, setMetrics] = useState<MetricCard[]>([])

  // Initialize dashboard data
  useEffect(() => {
    const initialMetrics: MetricCard[] = [
      {
        id: 'active-scans',
        title: 'Active Scans',
        value: '1,247',
        change: '+12%',
        trend: 'up',
        icon: <Activity className="w-6 h-6" />,
        color: 'text-blue-400'
      },
      {
        id: 'accuracy-rate',
        title: 'Accuracy Rate',
        value: '97.8%',
        change: '+0.2%',
        trend: 'up',
        icon: <Target className="w-6 h-6" />,
        color: 'text-green-400'
      },
      {
        id: 'intel-sources',
        title: 'Intel Sources',
        value: '129',
        change: '+3',
        trend: 'up',
        icon: <Database className="w-6 h-6" />,
        color: 'text-purple-400'
      },
      {
        id: 'threat-level',
        title: 'Threat Level',
        value: 'MEDIUM',
        change: '-1',
        trend: 'down',
        icon: <Shield className="w-6 h-6" />,
        color: 'text-yellow-400'
      }
    ]
    setMetrics(initialMetrics)

    const initialActivities: LiveActivity[] = [
      {
        id: '1',
        type: 'alert',
        message: 'Suspicious domain registered: malware-c2.com',
        timestamp: '2m ago',
        severity: 'high'
      },
      {
        id: '2',
        type: 'discovery',
        message: 'New social media profile linked to target entity',
        timestamp: '5m ago',
        severity: 'medium'
      },
      {
        id: '3',
        type: 'analysis',
        message: 'Email validation completed: 94.7% confidence',
        timestamp: '8m ago',
        severity: 'low'
      },
      {
        id: '4',
        type: 'scan',
        message: 'Phone number verified across 12 countries',
        timestamp: '12m ago',
        severity: 'medium'
      }
    ]
    setActivities(initialActivities)
  }, [])

  // Update current time (client-side only to avoid hydration mismatch)
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date())
    }, 1000)
    return () => clearInterval(timer)
  }, [])

  // Format time in a way that's consistent
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  }

  // Simulate real-time activity updates
  useEffect(() => {
    const interval = setInterval(() => {
      const newActivity: LiveActivity = {
        id: Date.now().toString(),
        type: ['scan', 'alert', 'analysis', 'discovery'][Math.floor(Math.random() * 4)] as any,
        message: [
          'New IP address flagged in threat database',
          'OSINT scan completed: 23 new data points',
          'Domain reputation check: clean',
          'Social media monitoring: new mentions detected',
          'Email breach check: no compromises found'
        ][Math.floor(Math.random() * 5)],
        timestamp: 'now',
        severity: ['low', 'medium', 'high'][Math.floor(Math.random() * 3)] as any
      }

      setActivities(prev => [newActivity, ...prev.slice(0, 9)])
    }, 8000)

    return () => clearInterval(interval)
  }, [])

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'scan': return <Search className="w-4 h-4" />
      case 'alert': return <Shield className="w-4 h-4" />
      case 'analysis': return <Brain className="w-4 h-4" />
      case 'discovery': return <Eye className="w-4 h-4" />
      default: return <Activity className="w-4 h-4" />
    }
  }

  const getSeverityVariant = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error'
      case 'high': return 'warning'
      case 'medium': return 'info'
      case 'low': return 'success'
      default: return 'default'
    }
  }

  return (
    <section className="py-24 relative">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
      
      <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-3 mb-4">
            <Badge variant="success" dot pulse>
              Live Intelligence Dashboard
            </Badge>
            <Badge variant="info">
              {formatTime(currentTime)}
            </Badge>
          </div>
          
          <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
            REAL-TIME INTELLIGENCE{' '}
            <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">
              VISUALIZATION
            </span>
          </h2>
          
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Transform raw intelligence data into actionable insights with interactive visualizations, 
            network graphs, geospatial mapping, and predictive analytics powered by advanced machine learning.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Metrics Cards */}
          <div className="lg:col-span-2 space-y-6">
            {/* Key Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="grid grid-cols-1 md:grid-cols-2 gap-6"
            >
              {metrics.map((metric, index) => (
                <motion.div
                  key={metric.id}
                  initial={{ opacity: 0, scale: 0.8 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card variant="elevated" hover className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm text-slate-400 mb-1">{metric.title}</p>
                        <p className="text-2xl font-bold text-white">{metric.value}</p>
                      </div>
                      <div className={`${metric.color}`}>
                        {metric.icon}
                      </div>
                    </div>
                    <div className="flex items-center mt-4">
                      {metric.trend === 'up' ? (
                        <TrendingUp className="w-4 h-4 text-green-400 mr-1" />
                      ) : metric.trend === 'down' ? (
                        <TrendingDown className="w-4 h-4 text-red-400 mr-1" />
                      ) : (
                        <div className="w-4 h-4 bg-gray-400 rounded-full mr-1" />
                      )}
                      <span className={`text-sm ${
                        metric.trend === 'up' ? 'text-green-400' : 
                        metric.trend === 'down' ? 'text-red-400' : 'text-gray-400'
                      }`}>
                        {metric.change} vs last month
                      </span>
                    </div>
                  </Card>
                </motion.div>
              ))}
            </motion.div>

            {/* Intelligence Analytics Preview */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.4 }}
            >
              <Card variant="elevated" className="p-6">
                <CardHeader 
                  title="Advanced Analytics Engine"
                  subtitle="Interactive data visualization and correlation"
                  action={
                    <Badge variant="purple">
                      STREAMING
                    </Badge>
                  }
                />
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                      { icon: <Globe className="w-6 h-6" />, label: 'Network Analysis', desc: 'Interactive relationship mapping and entity correlation' },
                      { icon: <Target className="w-6 h-6" />, label: 'Geospatial Intel', desc: 'Global threat mapping and location-based analysis' },
                      { icon: <Brain className="w-6 h-6" />, label: 'Predictive Analytics', desc: 'AI-powered threat prediction and risk assessment' },
                      { icon: <Activity className="w-6 h-6" />, label: 'Timeline Analysis', desc: 'Temporal correlation and event sequence analysis' }
                    ].map((item, index) => (
                      <motion.div
                        key={index}
                        whileHover={{ scale: 1.05, y: -5 }}
                        className="text-center p-4 rounded-lg bg-slate-800/50 border border-slate-700/50"
                      >
                        <div className="text-blue-400 mb-2 flex justify-center">
                          {item.icon}
                        </div>
                        <h4 className="text-sm font-semibold text-white mb-1">{item.label}</h4>
                        <p className="text-xs text-slate-400">{item.desc}</p>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>

          {/* Live Activity Feed */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.6 }}
          >
            <Card variant="elevated" className="p-6 h-full">
              <CardHeader 
                title="Live Intelligence Feed"
                action={<StatusBadge status="online" />}
              />
              <CardContent>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                  <AnimatePresence>
                    {activities.map((activity) => (
                      <motion.div
                        key={activity.id}
                        initial={{ opacity: 0, y: 20, scale: 0.8 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: -20, scale: 0.8 }}
                        className="flex items-start gap-3 p-3 rounded-lg bg-slate-800/30 border border-slate-700/30 hover:bg-slate-800/50 transition-colors"
                      >
                        <div className="flex-shrink-0 mt-1">
                          <div className="text-blue-400">
                            {getActivityIcon(activity.type)}
                          </div>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm text-slate-200 break-words">
                            {activity.message}
                          </p>
                          <div className="flex items-center gap-2 mt-1">
                            <p className="text-xs text-slate-500">{activity.timestamp}</p>
                            <Badge 
                              variant={getSeverityVariant(activity.severity) as any}
                              size="sm"
                            >
                              {activity.severity.toUpperCase()}
                            </Badge>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
                
                <div className="mt-6 pt-4 border-t border-slate-700/50">
                  <Button variant="outline" size="sm" className="w-full">
                    View All Activities
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Quick Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.8 }}
          className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {[
            { value: '47', label: 'Active Queries' },
            { value: '1.2K', label: 'Data Points' },
            { value: '98.7%', label: 'Accuracy' }
          ].map((stat, index) => (
            <Card key={index} variant="glass" className="p-6 text-center">
              <div className="text-2xl font-bold text-blue-400">{stat.value}</div>
              <div className="text-sm text-slate-400">{stat.label}</div>
            </Card>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

export { ModernDashboard }