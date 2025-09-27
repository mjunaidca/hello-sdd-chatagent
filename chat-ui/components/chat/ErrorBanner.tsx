'use client'

import { motion } from 'framer-motion'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { AlertCircle, RefreshCw, X } from 'lucide-react'

interface ErrorBannerProps {
  error: string
  onRetry: () => void
  retryCount: number
  onDismiss?: () => void
}

export function ErrorBanner({ error, onRetry, retryCount, onDismiss }: ErrorBannerProps) {
  const bannerVariants = {
    hidden: {
      opacity: 0,
      y: -30,
      scale: 0.9,
      x: -10
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      x: 0
    },
    exit: {
      opacity: 0,
      y: -20,
      scale: 0.95,
      x: 10
    }
  }

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      exit="exit"
      variants={bannerVariants}
      transition={{
        duration: 0.4,
        ease: "easeOut"
      }}
      className="mx-4 mb-2"
    >
      <Card className="border-destructive bg-destructive/10 p-3">
        <div className="flex items-start gap-3">
          <AlertCircle className="h-4 w-4 text-destructive flex-shrink-0 mt-0.5" />
          
          <div className="flex-1 min-w-0">
            <p className="text-sm text-destructive font-medium">
              Connection Error
            </p>
            <p className="text-xs text-muted-foreground mt-1">
              {error}
            </p>
            {retryCount > 0 && (
              <p className="text-xs text-muted-foreground mt-1">
                Retry attempt {retryCount}
              </p>
            )}
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onRetry}
              className="h-8 px-3 text-xs"
            >
              <RefreshCw className="h-3 w-3 mr-1" />
              Retry
            </Button>
            
            {onDismiss && (
              <Button
                variant="ghost"
                size="sm"
                onClick={onDismiss}
                className="h-8 w-8 p-0"
                aria-label="Dismiss error"
              >
                <X className="h-3 w-3" />
              </Button>
            )}
          </div>
        </div>
      </Card>
    </motion.div>
  )
}
