import React, { useState } from 'react'
import { motion, useInView } from 'framer-motion'
import { 
  Brain, Layers, Radar, BarChart3, Shield, Zap,
  Network, Globe, Target, Activity, Database, Search,
  Users, Lock, TrendingUp, Eye, Cpu, Cloud
} from 'lucide-react'
import { Card, CardHeader, CardContent } from '../ui/Card'
import { Badge } from '../ui/Badge'
import { Button } from '../ui/Button'

interface Feature {
  id: string
  icon: React.ReactNode
  title: string
  description: string
  details: string[]
  gradient: string
  category: string
  comingSoon?: boolean
}

const ModernFeatures: React.FC = () => {
  const [activeFeature, setActiveFeature] = useState<string | null>(null)
  const ref = React.useRef(null)
  const isInView = useInView(ref, { once: true })

  const features: Feature[] = [
    {
      id: 'ai-intelligence',
      icon: <Brain className="w-8 h-8" />,
      title: 'AI-Powered Intelligence',
      description: 'Advanced machine learning algorithms automatically correlate data patterns, identify relationships, and predict threats with 97.8% accuracy.',
      details: [
        'Natural Language Processing for content analysis',
        'Pattern recognition across multiple data sources',
        'Predictive threat modeling and risk assessment',
        'Automated entity relationship mapping'
      ],
      gradient: 'from-purple-500 to-pink-500',
      category: 'AI & ML'
    },
    {
      id: 'multi-source',
      icon: <Layers className="w-8 h-8" />,
      title: 'Multi-Source Aggregation',
      description: 'Seamlessly integrate intelligence from 129+ sources including social media, dark web, public records, and proprietary threat feeds.',
      details: [
        'Social media platform integration',
        'Dark web monitoring and analysis',
        'Public records and government databases',
        'Custom API integrations and data feeds'
      ],
      gradient: 'from-blue-500 to-cyan-500',
      category: 'Data Sources'
    },
    {
      id: 'threat-detection',
      icon: <Radar className="w-8 h-8" />,
      title: 'Real-Time Threat Detection',
      description: 'Continuous monitoring with instant alerting on emerging threats, suspicious activities, and security indicators.',
      details: [
        'Real-time threat intelligence feeds',
        'Behavioral anomaly detection',
        'Automated alerting and notification system',
        'Threat landscape visualization'
      ],
      gradient: 'from-red-500 to-orange-500',
      category: 'Security'
    },
    {
      id: 'analytics',
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Advanced Analytics',
      description: 'Interactive visualizations, network graphs, and geospatial mapping provide comprehensive situational awareness.',
      details: [
        'Interactive network graph visualization',
        'Geospatial intelligence mapping',
        'Timeline analysis and correlation',
        'Custom dashboard creation'
      ],
      gradient: 'from-green-500 to-emerald-500',
      category: 'Analytics'
    },
    {
      id: 'security',
      icon: <Shield className="w-8 h-8" />,
      title: 'Enterprise Security',
      description: 'Bank-grade encryption, role-based access control, and comprehensive audit logging ensure maximum security.',
      details: [
        'AES-256 encryption for data at rest',
        'Role-based access control (RBAC)',
        'Comprehensive audit logging',
        'SOC 2 Type II compliance'
      ],
      gradient: 'from-indigo-500 to-purple-500',
      category: 'Security'
    },
    {
      id: 'performance',
      icon: <Zap className="w-8 h-8" />,
      title: 'Lightning Performance',
      description: 'Sub-second response times with parallel processing architecture that scales to handle enterprise workloads.',
      details: [
        'Distributed processing architecture',
        'In-memory caching and optimization',
        'Auto-scaling infrastructure',
        'Global CDN deployment'
      ],
      gradient: 'from-yellow-500 to-red-500',
      category: 'Performance'
    }
  ]

  const categories = Array.from(new Set(features.map(f => f.category)))

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 15
      }
    }
  }

  return (
    <section ref={ref} className="py-24 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900" />
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <Badge variant="purple" className="mb-4">
            ENTERPRISE INTELLIGENCE CAPABILITIES
          </Badge>
          <h2 className="text-4xl lg:text-5xl font-bold text-white mb-6">
            ADVANCED{' '}
            <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              AI-POWERED
            </span>
            <br />
            INTELLIGENCE OPERATIONS
          </h2>
          <p className="text-xl text-slate-300 max-w-3xl mx-auto">
            Deploy cutting-edge machine learning algorithms and comprehensive OSINT capabilities 
            to gather, analyze, and correlate intelligence data from across the digital landscape 
            with unprecedented speed and accuracy.
          </p>
        </motion.div>

        {/* Category Filter */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={isInView ? { opacity: 1 } : {}}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="flex flex-wrap justify-center gap-3 mb-12"
        >
          {categories.map((category) => (
            <Badge
              key={category}
              variant="outline"
              className="cursor-pointer hover:bg-slate-700/50 transition-colors"
            >
              {category}
            </Badge>
          ))}
        </motion.div>

        {/* Features Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {features.map((feature) => (
            <motion.div
              key={feature.id}
              variants={itemVariants}
              onHoverStart={() => setActiveFeature(feature.id)}
              onHoverEnd={() => setActiveFeature(null)}
            >
              <Card
                variant="elevated"
                hover
                glowEffect={activeFeature === feature.id}
                className="h-full group"
              >
                <CardContent padding="lg">
                  {/* Feature Icon */}
                  <div className="mb-6">
                    <div className={`
                      inline-flex p-3 rounded-xl bg-gradient-to-r ${feature.gradient} 
                      text-white shadow-lg group-hover:scale-110 transition-transform duration-200
                    `}>
                      {feature.icon}
                    </div>
                    {feature.comingSoon && (
                      <Badge variant="warning" size="sm" className="ml-3">
                        Coming Soon
                      </Badge>
                    )}
                  </div>

                  {/* Feature Content */}
                  <div className="space-y-4">
                    <h3 className="text-xl font-semibold text-white group-hover:text-blue-400 transition-colors">
                      {feature.title}
                    </h3>
                    
                    <p className="text-slate-300 leading-relaxed">
                      {feature.description}
                    </p>

                    {/* Feature Details */}
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={
                        activeFeature === feature.id
                          ? { opacity: 1, height: 'auto' }
                          : { opacity: 0, height: 0 }
                      }
                      transition={{ duration: 0.3 }}
                      className="overflow-hidden"
                    >
                      <ul className="space-y-2 text-sm text-slate-400">
                        {feature.details.map((detail, index) => (
                          <li key={index} className="flex items-start gap-2">
                            <div className="w-2 h-2 bg-blue-400 rounded-full mt-2 flex-shrink-0" />
                            {detail}
                          </li>
                        ))}
                      </ul>
                    </motion.div>

                    {/* Learn More Button */}
                    <Button
                      variant="ghost"
                      size="sm"
                      rightIcon={<TrendingUp className="w-4 h-4" />}
                      className="group-hover:text-blue-400"
                    >
                      Learn More
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </motion.div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={isInView ? { opacity: 1, y: 0 } : {}}
          transition={{ delay: 1, duration: 0.6 }}
          className="text-center mt-16"
        >
          <Button
            size="lg"
            gradient
            leftIcon={<Activity className="w-5 h-5" />}
            className="px-8 py-4"
          >
            Explore All Capabilities
          </Button>
        </motion.div>
      </div>
    </section>
  )
}

export { ModernFeatures }