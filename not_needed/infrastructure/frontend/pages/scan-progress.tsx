import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'

interface ScanProgress {
  scanId: string
  status: 'starting' | 'scanning' | 'aggregating' | 'generating_report' | 'completed' | 'error'
  progress: number
  currentScanner?: string
  scannersCompleted: number
  totalScanners: number
  entitiesFound: number
  estimatedTimeRemaining?: number
  results?: any
  error?: string
}

interface ScannerProgress {
  name: string
  status: 'pending' | 'running' | 'completed' | 'error'
  progress: number
  entitiesFound: number
  confidence: number
  timeElapsed?: number
}

export default function ScanProgressPage() {
  const router = useRouter()
  const { scanId } = router.query
  
  const [scanProgress, setScanProgress] = useState<ScanProgress>({
    scanId: scanId as string || '',
    status: 'starting',
    progress: 0,
    scannersCompleted: 0,
    totalScanners: 0,
    entitiesFound: 0
  })
  
  const [scannerDetails, setScannerDetails] = useState<ScannerProgress[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [errorCount, setErrorCount] = useState(0)

  useEffect(() => {
    if (!scanId) return

    // In a real implementation, this would use WebSockets
    // For now, we'll simulate with polling
    simulateWebSocketConnection()
    
    return () => {
      // Cleanup WebSocket connection
    }
  }, [scanId])

  const simulateWebSocketConnection = () => {
    setIsConnected(true)
    simulateScanProgress()
  }

  const simulateScanProgress = async () => {
    const scanners = [
      'email_validator', 'email_reputation', 'email_breach_scanner', 'social_media_email_scanner',
      'phone_validator', 'phone_location_scanner', 'phone_spam_scanner', 'phone_carrier_scanner',
      'twitter_scanner', 'linkedin_scanner', 'instagram_scanner', 'facebook_scanner', 'github_scanner',
      'public_records_search', 'court_records_search', 'business_registry', 'property_records'
    ]

    const totalScanners = scanners.length
    let scannersCompleted = 0
    let totalEntities = 0
    const scannerProgressArray: ScannerProgress[] = []

    // Initialize scanner progress
    scanners.forEach(scanner => {
      scannerProgressArray.push({
        name: scanner,
        status: 'pending',
        progress: 0,
        entitiesFound: 0,
        confidence: 0
      })
    })
    setScannerDetails([...scannerProgressArray])

    // Update initial progress
    setScanProgress(prev => ({
      ...prev,
      status: 'scanning',
      totalScanners,
      progress: 5
    }))

    // Simulate each scanner running
    for (let i = 0; i < scanners.length; i++) {
      const scanner = scanners[i]
      
      // Start scanner
      scannerProgressArray[i].status = 'running'
      scannerProgressArray[i].timeElapsed = 0
      setScannerDetails([...scannerProgressArray])
      
      setScanProgress(prev => ({
        ...prev,
        currentScanner: scanner.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
      }))

      // Simulate scanner progress
      for (let progress = 0; progress <= 100; progress += 20) {
        await new Promise(resolve => setTimeout(resolve, 200))
        
        scannerProgressArray[i].progress = progress
        scannerProgressArray[i].timeElapsed = (scannerProgressArray[i].timeElapsed || 0) + 0.2
        
        // Simulate finding entities
        if (progress > 50 && Math.random() > 0.3) {
          const newEntities = Math.floor(Math.random() * 3)
          scannerProgressArray[i].entitiesFound += newEntities
          totalEntities += newEntities
          scannerProgressArray[i].confidence = Math.random() * 0.4 + 0.6 // 0.6-1.0
        }
        
        setScannerDetails([...scannerProgressArray])
      }

      // Complete scanner
      scannerProgressArray[i].status = Math.random() > 0.9 ? 'error' : 'completed'
      if (scannerProgressArray[i].status === 'error') {
        setErrorCount(prev => prev + 1)
      } else {
        scannersCompleted++
      }
      
      setScannerDetails([...scannerProgressArray])
      
      // Update overall progress
      const overallProgress = Math.min((scannersCompleted / totalScanners) * 80, 80)
      setScanProgress(prev => ({
        ...prev,
        progress: overallProgress,
        scannersCompleted,
        entitiesFound: totalEntities,
        estimatedTimeRemaining: Math.max(0, (totalScanners - scannersCompleted) * 2)
      }))
    }

    // Aggregation phase
    setScanProgress(prev => ({
      ...prev,
      status: 'aggregating',
      currentScanner: 'Data Aggregation Engine',
      progress: 85
    }))
    
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Report generation phase
    setScanProgress(prev => ({
      ...prev,
      status: 'generating_report',
      currentScanner: 'Report Generator',
      progress: 95
    }))
    
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Complete
    setScanProgress(prev => ({
      ...prev,
      status: 'completed',
      progress: 100,
      currentScanner: undefined,
      results: {
        totalEntities: totalEntities,
        highConfidenceEntities: Math.floor(totalEntities * 0.7),
        scanSuccessRate: ((scannersCompleted / totalScanners) * 100).toFixed(1)
      }
    }))
  }

  const handleViewResults = () => {
    router.push(`/results/${scanId}`)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-500'
      case 'running': return 'text-blue-500'
      case 'error': return 'text-red-500'
      default: return 'text-gray-500'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return '✅'
      case 'running': return '🔄'
      case 'error': return '❌'
      default: return '⏳'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Intelligence Scan in Progress</h1>
          <div className="flex items-center justify-center space-x-4 text-gray-300">
            <span className={`flex items-center ${isConnected ? 'text-green-400' : 'text-red-400'}`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${isConnected ? 'bg-green-400' : 'bg-red-400'}`}></div>
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
            <span>Scan ID: {scanId}</span>
          </div>
        </div>

        {/* Main Progress Card */}
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-8 border border-gray-600 mb-8">
            {/* Overall Progress */}
            <div className="mb-8">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-semibold text-white">
                  {scanProgress.status === 'starting' && 'Initializing Scan...'}
                  {scanProgress.status === 'scanning' && 'Running Intelligence Scanners...'}
                  {scanProgress.status === 'aggregating' && 'Aggregating Results...'}
                  {scanProgress.status === 'generating_report' && 'Generating Report...'}
                  {scanProgress.status === 'completed' && 'Scan Complete!'}
                  {scanProgress.status === 'error' && 'Scan Error'}
                </h2>
                <span className="text-white text-lg font-bold">{scanProgress.progress}%</span>
              </div>
              
              <div className="w-full bg-gray-700 rounded-full h-4 mb-4">
                <div 
                  className="bg-gradient-to-r from-primary-500 to-blue-500 h-4 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${scanProgress.progress}%` }}
                ></div>
              </div>

              {scanProgress.currentScanner && (
                <p className="text-gray-300 mb-2">
                  Currently running: <span className="text-white font-medium">{scanProgress.currentScanner}</span>
                </p>
              )}

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <div className="text-xl font-bold text-white">{scanProgress.scannersCompleted}</div>
                  <div className="text-sm text-gray-400">Scanners Complete</div>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <div className="text-xl font-bold text-white">{scanProgress.totalScanners}</div>
                  <div className="text-sm text-gray-400">Total Scanners</div>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <div className="text-xl font-bold text-green-400">{scanProgress.entitiesFound}</div>
                  <div className="text-sm text-gray-400">Entities Found</div>
                </div>
                <div className="bg-gray-800/50 rounded-lg p-4">
                  <div className="text-xl font-bold text-white">
                    {scanProgress.estimatedTimeRemaining ? `${scanProgress.estimatedTimeRemaining}s` : '--'}
                  </div>
                  <div className="text-sm text-gray-400">Est. Time Left</div>
                </div>
              </div>
            </div>

            {/* Error Summary */}
            {errorCount > 0 && (
              <div className="bg-red-900/20 border border-red-600 rounded-lg p-4 mb-6">
                <p className="text-red-400">
                  <span className="font-semibold">{errorCount}</span> scanner(s) encountered errors but the scan continues...
                </p>
              </div>
            )}

            {/* Results Summary (when completed) */}
            {scanProgress.status === 'completed' && scanProgress.results && (
              <div className="bg-green-900/20 border border-green-600 rounded-lg p-6 mb-6">
                <h3 className="text-xl font-semibold text-green-400 mb-4">Scan Results Summary</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-2xl font-bold text-white">{scanProgress.results.totalEntities}</div>
                    <div className="text-sm text-gray-400">Total Entities</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-green-400">{scanProgress.results.highConfidenceEntities}</div>
                    <div className="text-sm text-gray-400">High Confidence</div>
                  </div>
                  <div>
                    <div className="text-2xl font-bold text-blue-400">{scanProgress.results.scanSuccessRate}%</div>
                    <div className="text-sm text-gray-400">Success Rate</div>
                  </div>
                </div>
                
                <div className="text-center mt-6">
                  <button 
                    onClick={handleViewResults}
                    className="btn-primary px-8 py-3 text-lg"
                  >
                    View Full Results
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Scanner Details */}
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-gray-600">
            <h3 className="text-xl font-semibold text-white mb-4">Scanner Progress Details</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {scannerDetails.map((scanner, index) => (
                <div key={index} className="bg-gray-800/50 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-white truncate">
                      {scanner.name.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                    </span>
                    <span className={`text-lg ${getStatusColor(scanner.status)}`}>
                      {getStatusIcon(scanner.status)}
                    </span>
                  </div>
                  
                  {scanner.status !== 'pending' && (
                    <>
                      <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                        <div 
                          className={`h-2 rounded-full transition-all duration-300 ${
                            scanner.status === 'error' ? 'bg-red-500' : 
                            scanner.status === 'completed' ? 'bg-green-500' : 'bg-blue-500'
                          }`}
                          style={{ width: `${scanner.progress}%` }}
                        ></div>
                      </div>
                      
                      <div className="flex justify-between text-xs text-gray-400">
                        <span>Entities: {scanner.entitiesFound}</span>
                        {scanner.status === 'completed' && (
                          <span>Conf: {(scanner.confidence * 100).toFixed(0)}%</span>
                        )}
                        {scanner.timeElapsed && (
                          <span>{scanner.timeElapsed.toFixed(1)}s</span>
                        )}
                      </div>
                    </>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}