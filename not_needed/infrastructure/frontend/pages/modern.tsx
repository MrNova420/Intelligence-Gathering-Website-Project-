import Head from 'next/head'
import React from 'react'
import { ModernHero, ModernFeatures, ModernDashboard } from '../components/modern'

export default function ModernHomePage() {
  const handleGetStarted = () => {
    // Navigate to dashboard or signup
    window.location.href = '/dashboard'
  }

  const handleWatchDemo = () => {
    // Open demo video or navigate to demo page
    console.log('Watch demo clicked')
  }

  return (
    <>
      <Head>
        <title>IntelliGather Pro - Next-Gen Intelligence Platform | Modern UI</title>
        <meta 
          name="description" 
          content="Experience the most advanced intelligence gathering platform with modern UI, AI-powered analysis, and real-time threat detection." 
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-slate-950">
        {/* Modern Hero Section */}
        <ModernHero 
          onGetStarted={handleGetStarted}
          onWatchDemo={handleWatchDemo}
        />

        {/* Modern Features Section */}
        <ModernFeatures />

        {/* Modern Dashboard Preview */}
        <ModernDashboard />

        {/* Modern Footer - Simplified */}
        <footer className="border-t border-slate-800/50 bg-slate-900/50 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-6 lg:px-8 py-12">
            <div className="text-center">
              <h3 className="text-2xl font-bold text-white mb-4">
                Ready to Transform Your Intelligence Operations?
              </h3>
              <p className="text-slate-300 mb-8 max-w-2xl mx-auto">
                Join thousands of security professionals who trust IntelliGather Pro 
                for their mission-critical intelligence gathering needs.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={handleGetStarted}
                  className="px-8 py-4 bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-500 
                           text-white font-semibold rounded-lg hover:from-blue-700 hover:via-purple-700 
                           hover:to-cyan-600 transition-all duration-200 transform hover:scale-105"
                >
                  Start Free Trial
                </button>
                <button
                  onClick={handleWatchDemo}
                  className="px-8 py-4 border border-slate-600 text-slate-200 font-semibold 
                           rounded-lg hover:bg-slate-800/50 hover:border-slate-500 
                           transition-all duration-200"
                >
                  Schedule Demo
                </button>
              </div>
            </div>
            
            <div className="mt-12 pt-8 border-t border-slate-800/50 text-center">
              <p className="text-slate-500">
                © 2024 IntelliGather Pro. All rights reserved. Enterprise Intelligence Platform.
              </p>
            </div>
          </div>
        </footer>
      </main>
    </>
  )
}