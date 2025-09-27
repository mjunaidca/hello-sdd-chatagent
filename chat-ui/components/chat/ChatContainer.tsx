'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { ChatInput } from './ChatInput'
import { ChatMessage } from './ChatMessage'
import { TypingIndicator } from './TypingIndicator'
import { ErrorBanner } from './ErrorBanner'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Card } from '@/components/ui/card'
import { ChatMessage as ChatMessageType } from '@/lib/types'
import { useChatStream } from '@/hooks/useChatStream'
import { sessionManager } from '@/lib/session'

export function ChatContainer() {
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [isUserScrolling, setIsUserScrolling] = useState(false)

  const { chatState, sendMessage, retry, initializeSession } = useChatStream({
    onError: (error) => {
      console.error('Chat error:', error)
    },
    onRetry: () => {
      console.log('Retrying connection...')
    }
  })

  // Initialize session on mount
  useEffect(() => {
    initializeSession()
  }, [initializeSession])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (!isUserScrolling && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [chatState.messages, isUserScrolling])

  // Handle scroll events to detect user scrolling
  const handleScroll = () => {
    if (!scrollAreaRef.current) return
    
    const { scrollTop, scrollHeight, clientHeight } = scrollAreaRef.current
    const isAtBottom = scrollHeight - scrollTop - clientHeight < 50
    
    setIsUserScrolling(!isAtBottom)
  }

  // Enhanced auto-scroll with smooth behavior
  const scrollToBottom = useCallback((force = false) => {
    if (!messagesEndRef.current) return
    
    if (force || !isUserScrolling) {
      messagesEndRef.current.scrollIntoView({ 
        behavior: 'smooth',
        block: 'end'
      })
    }
  }, [isUserScrolling])

  const handleRetry = () => {
    retry()
  }

  return (
    <div className="flex flex-col h-screen bg-background" role="main" aria-label="Chat interface">
      {/* Header */}
      <header className="flex-shrink-0 p-3 sm:p-4 border-b">
        <h1 className="text-lg sm:text-xl font-semibold">Chat Assistant</h1>
        <div className="flex items-center gap-2 mt-1">
          <div 
            className={`w-2 h-2 rounded-full ${chatState.isConnected ? 'bg-green-500' : 'bg-red-500'}`}
            aria-label={`Connection status: ${chatState.isConnected ? 'Connected' : 'Disconnected'}`}
          />
          <span className="text-xs sm:text-sm text-muted-foreground">
            {chatState.isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </header>

      {/* Messages Area */}
      <main className="flex-1 overflow-hidden" aria-label="Chat messages">
        <ScrollArea 
          ref={scrollAreaRef}
          className="h-full p-2 sm:p-4"
          onScrollCapture={handleScroll}
        >
          <div className="space-y-4" role="log" aria-live="polite" aria-label="Chat conversation">
            {chatState.messages.length === 0 && (
              <div className="text-center text-muted-foreground py-8">
                <p>Start a conversation by typing a message below.</p>
              </div>
            )}
            
            {chatState.messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            
            {chatState.isStreaming && <TypingIndicator />}
            
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>
      </main>

      {/* Error Banner */}
      {chatState.error && (
        <ErrorBanner 
          error={chatState.error} 
          onRetry={handleRetry}
          retryCount={chatState.retryCount}
        />
      )}

      {/* Input Area */}
      <footer className="flex-shrink-0 p-3 sm:p-4 border-t">
        <ChatInput 
          onSendMessage={sendMessage}
          disabled={chatState.isStreaming}
        />
      </footer>
    </div>
  )
}
