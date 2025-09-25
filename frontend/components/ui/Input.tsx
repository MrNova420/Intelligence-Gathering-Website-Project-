import React from 'react'
import { motion } from 'framer-motion'
import { clsx } from 'clsx'
import { Eye, EyeOff, Search, AlertCircle, CheckCircle } from 'lucide-react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  description?: string
  error?: string
  success?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  variant?: 'default' | 'search' | 'ghost'
  inputSize?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({
    className,
    type = 'text',
    label,
    description,
    error,
    success,
    leftIcon,
    rightIcon,
    variant = 'default',
    inputSize = 'md',
    loading = false,
    disabled,
    ...props
  }, ref) => {
    const [showPassword, setShowPassword] = React.useState(false)
    const [isFocused, setIsFocused] = React.useState(false)
    
    const isPassword = type === 'password'
    const inputType = isPassword && showPassword ? 'text' : type
    const hasError = !!error
    const hasSuccess = !!success && !hasError

    const containerClasses = clsx(
      'relative w-full',
      disabled && 'opacity-50 cursor-not-allowed'
    )

    const inputClasses = clsx(
      // Base styles
      'w-full transition-all duration-200 font-medium placeholder:text-slate-500',
      'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900',
      'disabled:cursor-not-allowed disabled:opacity-50',
      
      // Size variants
      {
        'px-3 py-2 text-sm rounded-md': inputSize === 'sm',
        'px-4 py-3 text-sm rounded-lg': inputSize === 'md',
        'px-6 py-4 text-base rounded-lg': inputSize === 'lg',
      },
      
      // Left icon padding
      {
        'pl-10': leftIcon && inputSize === 'sm',
        'pl-12': leftIcon && inputSize === 'md',
        'pl-14': leftIcon && inputSize === 'lg',
      },
      
      // Right icon/button padding
      {
        'pr-10': (rightIcon || isPassword) && inputSize === 'sm',
        'pr-12': (rightIcon || isPassword) && inputSize === 'md',
        'pr-14': (rightIcon || isPassword) && inputSize === 'lg',
      },
      
      // Variant styles
      {
        // Default - inspired by GitHub inputs
        'bg-slate-900/50 border border-slate-700 text-slate-100 focus:border-blue-500 focus:ring-blue-500/20': 
          variant === 'default' && !hasError && !hasSuccess,
        
        // Search - inspired by modern search interfaces
        'bg-slate-800/50 border border-slate-600 text-slate-100 focus:border-cyan-500 focus:ring-cyan-500/20': 
          variant === 'search' && !hasError && !hasSuccess,
        
        // Ghost - inspired by Linear's ghost inputs
        'bg-transparent border-0 border-b-2 border-slate-700 rounded-none text-slate-100 focus:border-blue-500 focus:ring-0': 
          variant === 'ghost' && !hasError && !hasSuccess,
      },
      
      // Error state
      {
        'border-red-500 focus:border-red-500 focus:ring-red-500/20 text-red-100': hasError,
      },
      
      // Success state
      {
        'border-green-500 focus:border-green-500 focus:ring-green-500/20 text-green-100': hasSuccess,
      },
      
      className
    )

    const iconSize = inputSize === 'sm' ? 'w-4 h-4' : inputSize === 'lg' ? 'w-6 h-6' : 'w-5 h-5'
    const iconPosition = {
      left: inputSize === 'sm' ? 'left-3' : inputSize === 'lg' ? 'left-4' : 'left-3',
      right: inputSize === 'sm' ? 'right-3' : inputSize === 'lg' ? 'right-4' : 'right-3',
    }

    return (
      <div className={containerClasses}>
        {label && (
          <motion.label
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="block text-sm font-medium text-slate-200 mb-2"
          >
            {label}
          </motion.label>
        )}
        
        {description && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-xs text-slate-400 mb-2"
          >
            {description}
          </motion.p>
        )}

        <div className="relative">
          {/* Left Icon */}
          {leftIcon && (
            <div className={clsx(
              'absolute top-1/2 transform -translate-y-1/2 text-slate-400',
              iconPosition.left
            )}>
              <span className={iconSize}>{leftIcon}</span>
            </div>
          )}
          
          {/* Search Icon for search variant */}
          {variant === 'search' && !leftIcon && (
            <div className={clsx(
              'absolute top-1/2 transform -translate-y-1/2 text-slate-400',
              iconPosition.left
            )}>
              <Search className={iconSize} />
            </div>
          )}

          {/* Input Field */}
          <motion.input
            ref={ref}
            type={inputType}
            className={inputClasses}
            disabled={disabled}
            onFocus={() => setIsFocused(true)}
            onBlur={() => setIsFocused(false)}
            whileFocus={{ scale: 1.01 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            {...props}
          />

          {/* Right Icons */}
          <div className={clsx(
            'absolute top-1/2 transform -translate-y-1/2 flex items-center gap-2',
            iconPosition.right
          )}>
            {/* Loading Indicator */}
            {loading && (
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                className={clsx('border-2 border-slate-500 border-t-blue-500 rounded-full', {
                  'w-4 h-4': inputSize === 'sm',
                  'w-5 h-5': inputSize === 'md', 
                  'w-6 h-6': inputSize === 'lg',
                })}
              />
            )}
            
            {/* Status Icons */}
            {!loading && hasError && (
              <AlertCircle className={clsx(iconSize, 'text-red-400')} />
            )}
            {!loading && hasSuccess && (
              <CheckCircle className={clsx(iconSize, 'text-green-400')} />
            )}
            
            {/* Password Toggle */}
            {isPassword && (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="text-slate-400 hover:text-slate-200 transition-colors"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? (
                  <EyeOff className={iconSize} />
                ) : (
                  <Eye className={iconSize} />
                )}
              </button>
            )}
            
            {/* Custom Right Icon */}
            {rightIcon && !isPassword && !loading && !hasError && !hasSuccess && (
              <span className={clsx(iconSize, 'text-slate-400')}>
                {rightIcon}
              </span>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 text-sm text-red-400 flex items-center gap-1"
          >
            <AlertCircle className="w-4 h-4" />
            {error}
          </motion.p>
        )}

        {/* Success Message */}
        {success && !error && (
          <motion.p
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-2 text-sm text-green-400 flex items-center gap-1"
          >
            <CheckCircle className="w-4 h-4" />
            {success}
          </motion.p>
        )}

        {/* Focus Ring Effect */}
        {isFocused && (
          <motion.div
            layoutId="focus-ring"
            className="absolute inset-0 rounded-lg ring-2 ring-blue-500/20 pointer-events-none"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export { Input }
export type { InputProps }