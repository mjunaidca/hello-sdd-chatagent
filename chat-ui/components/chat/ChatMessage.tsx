'use client'

import { motion } from 'framer-motion'
import { Card } from '@/components/ui/card'
import { ChatMessage as ChatMessageType } from '@/lib/types'
import { formatMessageTime, sanitizeMessageContent } from '@/lib/utils'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

interface ChatMessageProps {
  message: ChatMessageType
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.senderType === 'user'
  const isStreaming = message.status === 'streaming'
  const isFailed = message.status === 'failed'
  const isSending = message.status === 'sending'

  const sanitizedContent = sanitizeMessageContent(message.content)

  const getStatusIcon = () => {
    if (isSending) {
      return <Loader2 className="h-3 w-3 animate-spin text-muted-foreground" data-testid="status-icon" />
    }
    if (isFailed) {
      return <XCircle className="h-3 w-3 text-destructive" data-testid="status-icon" />
    }
    if (message.status === 'sent') {
      return <CheckCircle className="h-3 w-3 text-green-500" data-testid="status-icon" />
    }
    return null
  }

  const messageVariants = {
    hidden: {
      opacity: 0,
      y: 20,
      scale: 0.95,
      x: isUser ? 20 : -20
    },
    visible: {
      opacity: 1,
      y: 0,
      scale: 1,
      x: 0
    },
    exit: {
      opacity: 0,
      y: -10,
      scale: 0.95,
      x: isUser ? 10 : -10
    }
  }

  const bubbleVariants = {
    hidden: {
      scale: 0.8,
      opacity: 0
    },
    visible: {
      scale: 1,
      opacity: 1
    }
  }

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={messageVariants}
      transition={{
        duration: 0.4,
        ease: "easeOut"
      }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
      role="article"
      aria-label={`Message from ${isUser ? 'you' : 'assistant'}`}
    >
      <div className={`flex items-end gap-2 max-w-[85%] sm:max-w-[80%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div 
          className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
            isUser 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-muted text-muted-foreground'
          }`}
          aria-label={`Avatar for ${isUser ? 'user' : 'assistant'}`}
        >
          {isUser ? 'U' : 'A'}
        </div>

        {/* Message Bubble */}
        <motion.div
          variants={bubbleVariants}
          initial="hidden"
          animate="visible"
          transition={{
            duration: 0.2,
            delay: 0.1,
            ease: "easeOut"
          }}
        >
          <Card className={`px-4 py-2 max-w-full ${
            isUser 
              ? 'bg-primary text-primary-foreground' 
              : 'bg-muted text-muted-foreground'
          }`}>
          <div className="space-y-1">
            {/* Message Content */}
            <div 
              className="whitespace-pre-wrap break-words"
              aria-label={`Message content: ${sanitizedContent || (isStreaming ? 'Assistant is thinking...' : '')}`}
            >
              {sanitizedContent || (isStreaming ? 'Thinking...' : '')}
            </div>

            {/* Message Footer */}
            <div className={`flex items-center gap-1 text-xs ${
              isUser ? 'text-primary-foreground/70' : 'text-muted-foreground/70'
            }`}>
              <span>{formatMessageTime(message.timestamp)}</span>
              {getStatusIcon()}
            </div>
          </div>
          </Card>
        </motion.div>
      </div>
    </motion.div>
  )
}
