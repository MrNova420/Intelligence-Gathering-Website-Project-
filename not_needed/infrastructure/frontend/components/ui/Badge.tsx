import React from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'purple' | 'cyan'
  size?: 'sm' | 'md' | 'lg'
  outline?: boolean
  dot?: boolean
  pulse?: boolean
  removable?: boolean
  onRemove?: () => void
}

const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({
    className,
    variant = 'default',
    size = 'md',
    outline = false,
    dot = false,
    pulse = false,
    removable = false,
    onRemove,
    children,
    ...props
  }, ref) => {
    const baseClasses = clsx(
      // Base styles
      'inline-flex items-center font-medium rounded-full transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900',
      
      // Size variants
      {
        'px-2 py-0.5 text-xs gap-1': size === 'sm',
        'px-2.5 py-1 text-xs gap-1.5': size === 'md', 
        'px-3 py-1.5 text-sm gap-2': size === 'lg',
      },
      
      // Color variants - filled
      {
        // Default - inspired by GitHub's default labels
        'bg-slate-700 text-slate-200 ring-slate-600': variant === 'default' && !outline,
        
        // Success - inspired by GitHub's success states
        'bg-green-600/20 text-green-400 ring-green-500/30': variant === 'success' && !outline,
        
        // Warning - inspired by Discord's warning badges
        'bg-yellow-600/20 text-yellow-400 ring-yellow-500/30': variant === 'warning' && !outline,
        
        // Error - inspired by GitHub's error states
        'bg-red-600/20 text-red-400 ring-red-500/30': variant === 'error' && !outline,
        
        // Info - inspired by Linear's info badges
        'bg-blue-600/20 text-blue-400 ring-blue-500/30': variant === 'info' && !outline,
        
        // Purple - inspired by Discord's purple accents
        'bg-purple-600/20 text-purple-400 ring-purple-500/30': variant === 'purple' && !outline,
        
        // Cyan - inspired by modern design systems
        'bg-cyan-600/20 text-cyan-400 ring-cyan-500/30': variant === 'cyan' && !outline,
      },
      
      // Color variants - outline
      {
        'bg-transparent border text-slate-300 border-slate-600': variant === 'default' && outline,
        'bg-transparent border text-green-400 border-green-500/50': variant === 'success' && outline,
        'bg-transparent border text-yellow-400 border-yellow-500/50': variant === 'warning' && outline,
        'bg-transparent border text-red-400 border-red-500/50': variant === 'error' && outline,
        'bg-transparent border text-blue-400 border-blue-500/50': variant === 'info' && outline,
        'bg-transparent border text-purple-400 border-purple-500/50': variant === 'purple' && outline,
        'bg-transparent border text-cyan-400 border-cyan-500/50': variant === 'cyan' && outline,
      },
      
      className
    )

    const dotColors = {
      default: 'bg-slate-400',
      success: 'bg-green-400',
      warning: 'bg-yellow-400', 
      error: 'bg-red-400',
      info: 'bg-blue-400',
      purple: 'bg-purple-400',
      cyan: 'bg-cyan-400',
    }

    return (
      <motion.span
        ref={ref}
        className={baseClasses}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.8 }}
        transition={{ type: "spring", stiffness: 500, damping: 30 }}
        {...props}
      >
        {dot && (
          <span 
            className={clsx(
              'w-2 h-2 rounded-full',
              dotColors[variant],
              pulse && 'animate-pulse'
            )}
          />
        )}
        {children}
        {removable && onRemove && (
          <button
            onClick={onRemove}
            className="ml-1 hover:bg-slate-600/50 rounded-full p-0.5 transition-colors"
            aria-label="Remove badge"
          >
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </motion.span>
    )
  }
)

Badge.displayName = 'Badge'

// Status Badge Component - for specific use cases
interface StatusBadgeProps extends Omit<BadgeProps, 'variant'> {
  status: 'online' | 'offline' | 'idle' | 'busy' | 'unknown'
}

const StatusBadge = React.forwardRef<HTMLSpanElement, StatusBadgeProps>(
  ({ status, ...props }, ref) => {
    const statusConfig = {
      online: { variant: 'success' as const, text: 'Online', pulse: true },
      offline: { variant: 'default' as const, text: 'Offline', pulse: false },
      idle: { variant: 'warning' as const, text: 'Idle', pulse: false },
      busy: { variant: 'error' as const, text: 'Busy', pulse: false },
      unknown: { variant: 'default' as const, text: 'Unknown', pulse: false },
    }

    const config = statusConfig[status]

    return (
      <Badge
        ref={ref}
        variant={config.variant}
        dot
        pulse={config.pulse}
        {...props}
      >
        {config.text}
      </Badge>
    )
  }
)

StatusBadge.displayName = 'StatusBadge'

export { Badge, StatusBadge }
export type { BadgeProps, StatusBadgeProps }