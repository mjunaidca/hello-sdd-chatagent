'use client'

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Send, Loader2 } from 'lucide-react'
import { isValidMessageContent } from '@/lib/utils'

interface ChatInputProps {
  onSendMessage: (content: string) => void
  disabled?: boolean
}

export function ChatInput({ onSendMessage, disabled = false }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [isSending, setIsSending] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!message.trim() || !isValidMessageContent(message) || disabled || isSending) {
      return
    }

    setIsSending(true)
    const messageToSend = message.trim()
    
    try {
      await onSendMessage(messageToSend)
      // Only clear the message after successful send
      setMessage('')
    } catch (error) {
      console.error('Failed to send message:', error)
      // Don't clear the message on error so user can retry
    } finally {
      setIsSending(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleTouchEnd = (e: React.TouchEvent) => {
    // Prevent double-tap zoom on mobile
    e.preventDefault()
  }

  // Focus input on mount
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  const isDisabled = disabled || isSending || !message.trim() || !isValidMessageContent(message)

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <div className="flex-1">
        <Input
          ref={inputRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          onTouchEnd={handleTouchEnd}
          placeholder="Type your message..."
          disabled={disabled || isSending}
          className="min-h-[44px] text-sm sm:text-base touch-manipulation"
          maxLength={10000}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="off"
          spellCheck="false"
        />
      </div>
      <Button 
        type="submit" 
        disabled={isDisabled}
        size="icon"
        className="min-h-[44px] min-w-[44px] flex-shrink-0"
        aria-label="Send message"
      >
        {isSending ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : (
          <Send className="h-4 w-4" />
        )}
      </Button>
    </form>
  )
}
