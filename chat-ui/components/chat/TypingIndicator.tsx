'use client'

import { motion } from 'framer-motion'
import { Card } from '@/components/ui/card'

export function TypingIndicator() {
  const dotVariants = {
    initial: { y: 0, scale: 1 },
    animate: {
      y: [-6, 6, -6],
      scale: [1, 1.2, 1]
    }
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0
    }
  }

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      transition={{
        duration: 0.3,
        ease: "easeOut"
      }}
      className="flex justify-start"
      role="status"
      aria-label="Assistant is typing"
    >
      <div className="flex items-end gap-2 max-w-[80%]">
        {/* Avatar */}
        <div 
          className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium bg-muted text-muted-foreground"
          aria-label="Assistant avatar"
        >
          A
        </div>

        {/* Typing Bubble */}
        <Card className="px-4 py-2 bg-muted text-muted-foreground">
          <div className="flex items-center gap-1">
            <span className="text-sm mr-2" aria-hidden="true">Assistant is typing</span>
            <div className="flex gap-1" aria-hidden="true">
              {[0, 1, 2].map((index) => (
                <motion.div
                  key={index}
                  variants={dotVariants}
                  initial="initial"
                  animate="animate"
                  transition={{
                    duration: 1.4,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                  style={{ animationDelay: `${index * 0.2}s` }}
                  className="w-2 h-2 bg-muted-foreground rounded-full"
                />
              ))}
            </div>
            <span className="sr-only">Assistant is typing a response</span>
          </div>
        </Card>
      </div>
    </motion.div>
  )
}
