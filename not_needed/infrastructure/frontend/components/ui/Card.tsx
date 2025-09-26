import React from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined' | 'glass'
  hover?: boolean
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  gradient?: boolean
  glowEffect?: boolean
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({
    className,
    variant = 'default',
    hover = false,
    padding = 'md',
    gradient = false,
    glowEffect = false,
    children,
    ...props
  }, ref) => {
    const baseClasses = clsx(
      // Base styles
      'relative rounded-lg transition-all duration-200',
      
      // Padding variants
      {
        'p-0': padding === 'none',
        'p-3': padding === 'sm',
        'p-4': padding === 'md',
        'p-6': padding === 'lg',
        'p-8': padding === 'xl',
      },
      
      // Variant styles
      {
        // Default - inspired by GitHub cards
        'bg-slate-900/50 border border-slate-800/50': variant === 'default',
        
        // Elevated - inspired by Linear's elevated surfaces
        'bg-slate-900/80 border border-slate-700/50 shadow-xl': variant === 'elevated',
        
        // Outlined - inspired by Discord's outlined containers
        'bg-slate-900/20 border-2 border-slate-700/50': variant === 'outlined',
        
        // Glass - inspired by modern glassmorphism
        'bg-white/5 backdrop-blur-sm border border-white/10': variant === 'glass',
      },
      
      // Gradient background
      {
        'bg-gradient-to-br from-slate-900/50 via-slate-800/30 to-slate-900/50': gradient,
      },
      
      // Hover effects
      {
        'hover:bg-slate-800/60 hover:border-slate-600/50 cursor-pointer': hover && variant === 'default',
        'hover:bg-slate-800/90 hover:shadow-2xl hover:border-slate-600/50': hover && variant === 'elevated',
        'hover:bg-slate-800/30 hover:border-slate-600/60': hover && variant === 'outlined',
        'hover:bg-white/10 hover:border-white/20': hover && variant === 'glass',
      },
      
      className
    )

    const motionProps = hover ? {
      whileHover: { y: -2, scale: 1.01 },
      transition: { type: "spring", stiffness: 400, damping: 25 }
    } : {}

    return (
      <motion.div
        ref={ref}
        className={baseClasses}
        {...motionProps}
        {...props}
      >
        {/* Glow effect - inspired by modern UI trends */}
        {glowEffect && (
          <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-cyan-500/20 blur-xl -z-10" />
        )}
        {children}
      </motion.div>
    )
  }
)

Card.displayName = 'Card'

// Card Header Component
interface CardHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string
  subtitle?: string
  action?: React.ReactNode
}

const CardHeader = React.forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className, title, subtitle, action, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          'flex items-center justify-between pb-4 border-b border-slate-800/50',
          className
        )}
        {...props}
      >
        <div className="space-y-1">
          {title && (
            <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
          )}
          {subtitle && (
            <p className="text-sm text-slate-400">{subtitle}</p>
          )}
          {children}
        </div>
        {action && <div className="flex-shrink-0">{action}</div>}
      </div>
    )
  }
)

CardHeader.displayName = 'CardHeader'

// Card Content Component
const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx('pt-4', className)}
        {...props}
      />
    )
  }
)

CardContent.displayName = 'CardContent'

// Card Footer Component  
const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          'pt-4 border-t border-slate-800/50 flex items-center justify-between',
          className
        )}
        {...props}
      />
    )
  }
)

CardFooter.displayName = 'CardFooter'

export { Card, CardHeader, CardContent, CardFooter }
export type { CardProps, CardHeaderProps }