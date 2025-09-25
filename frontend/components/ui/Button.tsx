import React from 'react'
import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'
import { clsx } from 'clsx'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  loading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  gradient?: boolean
  glassmorphism?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    className,
    variant = 'primary',
    size = 'md',
    loading = false,
    leftIcon,
    rightIcon,
    gradient = false,
    glassmorphism = false,
    children,
    disabled,
    ...props
  }, ref) => {
    const baseClasses = clsx(
      // Base styles
      'relative inline-flex items-center justify-center font-medium transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'rounded-lg border',
      
      // Size variants
      {
        'px-3 py-1.5 text-sm gap-1.5': size === 'sm',
        'px-4 py-2 text-sm gap-2': size === 'md',
        'px-6 py-3 text-base gap-2': size === 'lg',
        'px-8 py-4 text-lg gap-3': size === 'xl',
      },
      
      // Variant styles
      {
        // Primary - inspired by GitHub's primary button
        'bg-blue-600 hover:bg-blue-700 text-white border-blue-600 focus:ring-blue-500': 
          variant === 'primary' && !gradient,
        
        // Secondary - inspired by Linear's secondary buttons
        'bg-slate-800 hover:bg-slate-700 text-slate-100 border-slate-700 focus:ring-slate-500': 
          variant === 'secondary',
        
        // Outline - inspired by GitHub's outline button
        'bg-transparent hover:bg-slate-800/50 text-slate-300 border-slate-600 hover:border-slate-500 focus:ring-slate-500': 
          variant === 'outline',
        
        // Ghost - inspired by Discord's ghost buttons
        'bg-transparent hover:bg-slate-800/30 text-slate-400 hover:text-slate-200 border-transparent focus:ring-slate-500': 
          variant === 'ghost',
        
        // Danger - inspired by modern error states
        'bg-red-600 hover:bg-red-700 text-white border-red-600 focus:ring-red-500': 
          variant === 'danger',
      },
      
      // Gradient variant - inspired by modern SaaS platforms
      {
        'bg-gradient-to-r from-blue-600 via-purple-600 to-cyan-500 hover:from-blue-700 hover:via-purple-700 hover:to-cyan-600 text-white border-transparent': 
          gradient && variant === 'primary',
      },
      
      // Glassmorphism effect - inspired by modern design trends
      {
        'backdrop-blur-sm bg-white/10 border-white/20 hover:bg-white/20': glassmorphism,
      },
      
      className
    )

    const iconSize = size === 'sm' ? 'w-4 h-4' : size === 'xl' ? 'w-6 h-6' : 'w-5 h-5'

    return (
      <motion.button
        ref={ref}
        className={baseClasses}
        disabled={disabled || loading}
        whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
        whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
        transition={{ type: "spring", stiffness: 400, damping: 25 }}
        {...props}
      >
        {loading && (
          <Loader2 className={clsx('animate-spin', iconSize)} />
        )}
        {!loading && leftIcon && (
          <span className={iconSize}>{leftIcon}</span>
        )}
        {children}
        {!loading && rightIcon && (
          <span className={iconSize}>{rightIcon}</span>
        )}
      </motion.button>
    )
  }
)

Button.displayName = 'Button'

export { Button }
export type { ButtonProps }