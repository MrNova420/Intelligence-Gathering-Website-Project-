/**
 * Enterprise Query Dashboard Component
 * 
 * AAA-grade React component with:
 * - Modern TypeScript patterns
 * - Real-time query tracking
 * - Advanced UI/UX design
 * - Accessibility compliance
 * - Performance optimization
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
  Search, 
  Filter, 
  Download, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  Clock, 
  AlertTriangle,
  TrendingUp,
  BarChart3,
  Eye,
  Settings
} from 'lucide-react';

// Types
interface QueryResult {
  id: string;
  queryType: string;
  target: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  createdAt: string;
  completedAt?: string;
  scannerResults: ScannerResult[];
  estimatedCompletion?: string;
}

interface ScannerResult {
  scannerName: string;
  category: string;
  status: string;
  executionTime?: number;
  confidenceScore?: number;
  data?: any;
}

interface QueryFilters {
  status?: string;
  queryType?: string;
  dateRange?: string;
  searchTerm?: string;
}

// Custom hooks
const useQueryData = (filters: QueryFilters) => {
  const [queries, setQueries] = useState<QueryResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchQueries = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      if (filters.status) params.append('status_filter', filters.status);
      if (filters.queryType) params.append('query_type', filters.queryType);
      if (filters.searchTerm) params.append('search', filters.searchTerm);

      const response = await fetch(`/api/v1/queries?${params}`);
      if (!response.ok) throw new Error('Failed to fetch queries');

      const data = await response.json();
      setQueries(data.data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    fetchQueries();
  }, [fetchQueries]);

  return { queries, loading, error, refetch: fetchQueries };
};

const useRealTimeUpdates = (queryId: string | null) => {
  const [progress, setProgress] = useState<any>(null);

  useEffect(() => {
    if (!queryId) return;

    const fetchProgress = async () => {
      try {
        const response = await fetch(`/api/v1/queries/${queryId}/progress`);
        if (response.ok) {
          const data = await response.json();
          setProgress(data);
        }
      } catch (error) {
        console.error('Failed to fetch progress:', error);
      }
    };

    // Initial fetch
    fetchProgress();

    // Set up polling for real-time updates
    const interval = setInterval(fetchProgress, 2000);
    return () => clearInterval(interval);
  }, [queryId]);

  return progress;
};

// Components
const StatusBadge: React.FC<{ status: string; className?: string }> = ({ status, className = '' }) => {
  const statusConfig = {
    pending: { color: 'bg-gray-100 text-gray-800', icon: Clock },
    running: { color: 'bg-blue-100 text-blue-800', icon: RefreshCw },
    completed: { color: 'bg-green-100 text-green-800', icon: CheckCircle },
    failed: { color: 'bg-red-100 text-red-800', icon: XCircle },
    cancelled: { color: 'bg-yellow-100 text-yellow-800', icon: AlertTriangle }
  };

  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.pending;
  const Icon = config.icon;

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${config.color} ${className}`}>
      <Icon className="w-3 h-3 mr-1" />
      {status.charAt(0).toUpperCase() + status.slice(1)}
    </span>
  );
};

const ProgressBar: React.FC<{ progress: number; status: string; className?: string }> = ({ 
  progress, 
  status, 
  className = '' 
}) => {
  const getProgressColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'failed': return 'bg-red-500';
      case 'running': return 'bg-blue-500';
      default: return 'bg-gray-300';
    }
  };

  return (
    <div className={`w-full bg-gray-200 rounded-full h-2 ${className}`}>
      <div 
        className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(status)}`}
        style={{ width: `${Math.min(progress, 100)}%` }}
        role="progressbar"
        aria-valuenow={progress}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Progress: ${progress}%`}
      />
    </div>
  );
};

const QueryCard: React.FC<{ 
  query: QueryResult; 
  onViewDetails: (query: QueryResult) => void;
  onDownloadReport: (queryId: string) => void;
}> = ({ query, onViewDetails, onDownloadReport }) => {
  const progress = useRealTimeUpdates(query.status === 'running' ? query.id : null);
  const currentProgress = progress?.progress_percentage || query.progress;

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-gray-900 truncate">
            {query.queryType.toUpperCase()} Query
          </h3>
          <p className="text-sm text-gray-600 truncate" title={query.target}>
            Target: {query.target}
          </p>
        </div>
        <StatusBadge status={query.status} />
      </div>

      {/* Progress */}
      {(query.status === 'running' || query.status === 'completed') && (
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>Progress</span>
            <span>{Math.round(currentProgress)}%</span>
          </div>
          <ProgressBar progress={currentProgress} status={query.status} />
        </div>
      )}

      {/* Scanner Results Summary */}
      {query.scannerResults.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>Scanner Results</span>
            <span>{query.scannerResults.length} scanners</span>
          </div>
          <div className="flex space-x-2">
            {query.scannerResults.slice(0, 3).map((result, index) => (
              <div
                key={index}
                className={`w-3 h-3 rounded-full ${
                  result.status === 'completed' ? 'bg-green-500' :
                  result.status === 'failed' ? 'bg-red-500' :
                  result.status === 'running' ? 'bg-blue-500' :
                  'bg-gray-300'
                }`}
                title={`${result.scannerName}: ${result.status}`}
              />
            ))}
            {query.scannerResults.length > 3 && (
              <span className="text-xs text-gray-500">
                +{query.scannerResults.length - 3} more
              </span>
            )}
          </div>
        </div>
      )}

      {/* Timestamps */}
      <div className="text-xs text-gray-500 mb-4">
        <div>Created: {new Date(query.createdAt).toLocaleString()}</div>
        {query.completedAt && (
          <div>Completed: {new Date(query.completedAt).toLocaleString()}</div>
        )}
        {query.estimatedCompletion && query.status === 'running' && (
          <div>Est. completion: {new Date(query.estimatedCompletion).toLocaleString()}</div>
        )}
      </div>

      {/* Actions */}
      <div className="flex space-x-2">
        <button
          onClick={() => onViewDetails(query)}
          className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200"
        >
          <Eye className="w-4 h-4 inline mr-1" />
          View Details
        </button>
        {query.status === 'completed' && (
          <button
            onClick={() => onDownloadReport(query.id)}
            className="bg-green-600 text-white px-3 py-2 rounded-md text-sm font-medium hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-colors duration-200"
          >
            <Download className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  );
};

const FilterPanel: React.FC<{
  filters: QueryFilters;
  onFiltersChange: (filters: QueryFilters) => void;
}> = ({ filters, onFiltersChange }) => {
  const updateFilter = (key: keyof QueryFilters, value: string) => {
    onFiltersChange({ ...filters, [key]: value || undefined });
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
      <div className="flex items-center space-x-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="w-5 h-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search queries..."
              value={filters.searchTerm || ''}
              onChange={(e) => updateFilter('searchTerm', e.target.value)}
              className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <select
          value={filters.status || ''}
          onChange={(e) => updateFilter('status', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Statuses</option>
          <option value="pending">Pending</option>
          <option value="running">Running</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>

        <select
          value={filters.queryType || ''}
          onChange={(e) => updateFilter('queryType', e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Types</option>
          <option value="email">Email</option>
          <option value="phone">Phone</option>
          <option value="name">Name</option>
          <option value="username">Username</option>
          <option value="domain">Domain</option>
        </select>
      </div>
    </div>
  );
};

const StatsOverview: React.FC<{ queries: QueryResult[] }> = ({ queries }) => {
  const stats = useMemo(() => {
    const total = queries.length;
    const completed = queries.filter(q => q.status === 'completed').length;
    const running = queries.filter(q => q.status === 'running').length;
    const failed = queries.filter(q => q.status === 'failed').length;
    const successRate = total > 0 ? Math.round((completed / total) * 100) : 0;

    return { total, completed, running, failed, successRate };
  }, [queries]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center">
          <BarChart3 className="w-5 h-5 text-blue-600 mr-2" />
          <div>
            <p className="text-sm text-gray-600">Total Queries</p>
            <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center">
          <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
          <div>
            <p className="text-sm text-gray-600">Completed</p>
            <p className="text-2xl font-bold text-gray-900">{stats.completed}</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center">
          <RefreshCw className="w-5 h-5 text-blue-600 mr-2" />
          <div>
            <p className="text-sm text-gray-600">Running</p>
            <p className="text-2xl font-bold text-gray-900">{stats.running}</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center">
          <XCircle className="w-5 h-5 text-red-600 mr-2" />
          <div>
            <p className="text-sm text-gray-600">Failed</p>
            <p className="text-2xl font-bold text-gray-900">{stats.failed}</p>
          </div>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div className="flex items-center">
          <TrendingUp className="w-5 h-5 text-green-600 mr-2" />
          <div>
            <p className="text-sm text-gray-600">Success Rate</p>
            <p className="text-2xl font-bold text-gray-900">{stats.successRate}%</p>
          </div>
        </div>
      </div>
    </div>
  );
};

// Main Component
export const EnterpriseQueryDashboard: React.FC = () => {
  const [filters, setFilters] = useState<QueryFilters>({});
  const [selectedQuery, setSelectedQuery] = useState<QueryResult | null>(null);
  const { queries, loading, error, refetch } = useQueryData(filters);

  const handleViewDetails = useCallback((query: QueryResult) => {
    setSelectedQuery(query);
    // Open modal or navigate to details page
  }, []);

  const handleDownloadReport = useCallback(async (queryId: string) => {
    try {
      const response = await fetch(`/api/v1/reports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query_id: queryId, format: 'pdf' })
      });

      if (response.ok) {
        const data = await response.json();
        // Handle download or show success message
        console.log('Report generation started:', data);
      }
    } catch (error) {
      console.error('Failed to generate report:', error);
    }
  }, []);

  const handleRefresh = useCallback(() => {
    refetch();
  }, [refetch]);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Intelligence Queries</h1>
            <p className="text-gray-600 mt-1">Monitor and manage your intelligence gathering operations</p>
          </div>
          <div className="flex space-x-3">
            <button
              onClick={handleRefresh}
              disabled={loading}
              className="bg-white border border-gray-300 rounded-md px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button className="bg-blue-600 text-white rounded-md px-4 py-2 text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
              <Settings className="w-4 h-4 mr-2" />
              Settings
            </button>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <StatsOverview queries={queries} />

      {/* Filters */}
      <FilterPanel filters={filters} onFiltersChange={setFilters} />

      {/* Content */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <div className="flex">
            <XCircle className="w-5 h-5 text-red-400 mr-2 mt-0.5" />
            <div>
              <h3 className="text-sm font-medium text-red-800">Error loading queries</h3>
              <p className="text-sm text-red-700 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {loading && queries.length === 0 ? (
        <div className="flex items-center justify-center py-12">
          <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mr-3" />
          <span className="text-lg text-gray-600">Loading queries...</span>
        </div>
      ) : queries.length === 0 ? (
        <div className="text-center py-12">
          <Search className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No queries found</h3>
          <p className="text-gray-600">Start by submitting your first intelligence query.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {queries.map((query) => (
            <QueryCard
              key={query.id}
              query={query}
              onViewDetails={handleViewDetails}
              onDownloadReport={handleDownloadReport}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default EnterpriseQueryDashboard;