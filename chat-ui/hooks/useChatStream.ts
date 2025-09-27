'use client'

import { useState, useCallback, useRef, useEffect } from 'react'
import { ChatState, ChatMessage, StreamingEvent } from '@/lib/types'
import { generateMessageId } from '@/lib/utils'

interface UseChatStreamOptions {
  apiBaseUrl?: string
  onError?: (error: string) => void
  onRetry?: () => void
}

export function useChatStream(options: UseChatStreamOptions = {}) {
  const { apiBaseUrl = 'http://localhost:8000/api/v1', onError, onRetry } = options
  
  const [chatState, setChatState] = useState<ChatState>({
    session: null,
    messages: [],
    isConnected: false,
    isStreaming: false,
    error: null,
    retryCount: 0
  })

  const eventSourceRef = useRef<EventSource | null>(null)
  const retryTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const maxRetries = 3

  // Cleanup function
  const cleanup = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
      eventSourceRef.current = null
    }
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current)
      retryTimeoutRef.current = null
    }
  }, [])

  // Initialize session (create a local session for frontend state management)
  const initializeSession = useCallback(async () => {
    try {
      // Create a local session for frontend state management
      const session = {
        id: `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        userId: null,
        createdAt: new Date(),
        lastActivityAt: new Date(),
        isActive: true,
        deviceInfo: {
          userAgent: navigator.userAgent,
          screenSize: {
            width: window.screen.width,
            height: window.screen.height
          },
          isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
          platform: navigator.platform
        },
        messages: []
      }
      
      setChatState(prev => ({
        ...prev,
        session,
        isConnected: true,
        error: null
      }))

      console.log('Session initialized:', session.id)
      return session
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to initialize session'
      setChatState(prev => ({
        ...prev,
        error: errorMessage,
        isConnected: false
      }))
      // Call onError if it exists, but don't make it a dependency
      if (onError) {
        onError(errorMessage)
      }
      throw error
    }
  }, []) // Remove onError dependency

  // Start streaming response
  const startStreaming = useCallback(async (message: string) => {
    console.log('startStreaming called with message:', message)
    
    return new Promise<void>((resolve, reject) => {
      // Get current state to avoid stale closure
      let assistantMessageId: string = ''
      
      setChatState(prev => {
        if (!prev.session) {
          console.warn('No active session, cannot start streaming')
          reject(new Error('No active session'))
          return prev
        }

        console.log('Current session for streaming:', prev.session.id)
        cleanup() // Clean up any existing connection

        const assistantMessage: ChatMessage = {
          id: generateMessageId(),
          content: '',
          timestamp: new Date(),
          senderType: 'assistant',
          status: 'streaming' as const,
          sessionId: prev.session.id,
          isTyping: true
        }

        assistantMessageId = assistantMessage.id

        // Start the streaming connection immediately with the current session
        try {
          const streamUrl = `${apiBaseUrl}/chat/streaming?message=${encodeURIComponent(message)}&context_id=${prev.session.id}`
          console.log('Starting streaming connection to:', streamUrl)
          
          const eventSource = new EventSource(streamUrl)
          console.log('EventSource created:', eventSource)
          
          eventSourceRef.current = eventSource

          // Track last activity to detect idle streams
          let lastActivity = Date.now()
          let idleCheckInterval: NodeJS.Timeout

          const checkForIdle = () => {
            const now = Date.now()
            if (now - lastActivity > 5000) { // 5 seconds of inactivity
              console.log('Stream appears idle, ending connection')
              eventSource.close()
              setChatState(prevState => ({
                ...prevState,
                messages: prevState.messages.map(msg => 
                  msg.id === assistantMessageId 
                    ? { 
                        ...msg, 
                        status: 'sent' as const,
                        isTyping: false
                      }
                    : msg
                ),
                isStreaming: false
              }))
              resolve()
            }
          }

          // Check for idle every 2 seconds
          idleCheckInterval = setInterval(checkForIdle, 2000)

          eventSource.onmessage = (event) => {
            lastActivity = Date.now() // Update last activity time
            try {
              console.log('Received streaming event:', event.data)
              const data = JSON.parse(event.data)
              console.log('Parsed streaming data:', data)
              
              // Handle the streaming response format from spec 001
              if (data.token || data.event_type === 'token') {
                const token = data.token || data.final_output || ''
                console.log('Received token:', token)
                setChatState(prevState => ({
                  ...prevState,
                  messages: prevState.messages.map(msg => 
                    msg.id === assistantMessageId 
                      ? { 
                          ...msg, 
                          content: (msg.content || '') + token,
                          isTyping: false
                        }
                      : msg
                  )
                }))
              } else if (data.type === 'end' || data.event_type === 'end') {
                console.log('Stream ended, closing connection')
                setChatState(prevState => ({
                  ...prevState,
                  messages: prevState.messages.map(msg => 
                    msg.id === assistantMessageId 
                      ? { 
                          ...msg, 
                          status: 'sent' as const,
                          isTyping: false
                        }
                      : msg
                  ),
                  isStreaming: false
                }))
                eventSource.close()
                resolve() // Resolve when streaming ends
              } else {
                console.log('Unknown streaming event type:', data)
              }
            } catch (parseError) {
              console.error('Failed to parse streaming event:', parseError, 'Raw data:', event.data)
              reject(parseError)
            }
          }

          eventSource.onerror = (error) => {
            console.error('EventSource failed:', error)
            eventSource.close()
            if (idleCheckInterval) {
              clearInterval(idleCheckInterval)
            }
            
            setChatState(prevState => {
              const newRetryCount = prevState.retryCount + 1
              
              if (newRetryCount < maxRetries) {
                const delay = Math.pow(2, newRetryCount) * 1000
                console.log(`Retrying in ${delay}ms (attempt ${newRetryCount + 1}/${maxRetries})`)
                
                retryTimeoutRef.current = setTimeout(() => {
                  if (onRetry) {
                    onRetry()
                  }
                  startStreaming(message).then(resolve).catch(reject)
                }, delay)
                
                return {
                  ...prevState,
                  isStreaming: false,
                  error: `Connection lost. Retrying... (attempt ${newRetryCount + 1}/${maxRetries})`,
                  retryCount: newRetryCount
                }
              } else {
                console.error('Max retries reached, giving up')
                const errorMsg = 'Connection failed after multiple retries. Please try again.'
                return {
                  ...prevState,
                  isStreaming: false,
                  error: errorMsg,
                  retryCount: newRetryCount
                }
              }
            })
          }

          // Add a timeout to prevent infinite waiting
          const timeout = setTimeout(() => {
            console.log('Streaming timeout reached, closing connection')
            eventSource.close()
            setChatState(prevState => ({
              ...prevState,
              isStreaming: false,
              error: 'Streaming timeout. Please try again.'
            }))
            reject(new Error('Streaming timeout'))
          }, 30000) // 30 second timeout

          // Clear timeout and interval when stream ends
          const originalResolve = resolve
          resolve = () => {
            clearTimeout(timeout)
            if (idleCheckInterval) {
              clearInterval(idleCheckInterval)
            }
            originalResolve()
          }

        } catch (error) {
          const errorMessage = error instanceof Error ? error.message : 'Failed to start streaming'
          setChatState(prevState => ({
            ...prevState,
            isStreaming: false,
            error: errorMessage
          }))
          if (onError) {
            onError(errorMessage)
          }
          reject(error)
        }

        return {
          ...prev,
          messages: [...prev.messages, assistantMessage],
          isStreaming: true,
          error: null
        }
      })
    })
  }, []) // Remove dependencies to prevent infinite loops

  // Send message and start streaming
  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    console.log('sendMessage called with:', content.trim())

    // Get current state to avoid stale closure
    let currentSession: any = null
    let userMessageId: string = ''
    
    setChatState(prev => {
      if (!prev.session) {
        console.warn('No active session, cannot send message')
        return prev
      }

      currentSession = prev.session

      const userMessage: ChatMessage = {
        id: generateMessageId(),
        content: content.trim(),
        timestamp: new Date(),
        senderType: 'user',
        status: 'sending' as const,
        sessionId: prev.session.id,
        isTyping: false
      }

      userMessageId = userMessage.id

      // Add user message immediately
      const newState = {
        ...prev,
        messages: [...prev.messages, userMessage]
      }

      // Update user message status to sent
      return {
        ...newState,
        messages: newState.messages.map(msg => 
          msg.id === userMessage.id 
            ? { ...msg, status: 'sent' as const }
            : msg
        )
      }
    })

    if (!currentSession) {
      console.error('No session available for sending message')
      return
    }

    // Start streaming response directly
    console.log('Calling startStreaming with message:', content.trim())
    try {
      await startStreaming(content.trim())
      console.log('startStreaming completed successfully')
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to send message'
      console.error('startStreaming failed:', errorMessage)
      
      setChatState(prevState => ({
        ...prevState,
        messages: prevState.messages.map(msg => 
          msg.id === userMessageId 
            ? { ...msg, status: 'failed' as const }
            : msg
        ),
        error: errorMessage
      }))
      
      // Call onError if it exists
      if (onError) {
        onError(errorMessage)
      }
    }
  }, []) // Remove dependencies to prevent infinite loops

  // Manual retry
  const retry = useCallback(() => {
    setChatState(prev => ({
      ...prev,
      error: null,
      retryCount: 0
    }))
    if (onRetry) {
      onRetry()
    }
  }, []) // Remove onRetry dependency

  // Cleanup on unmount
  useEffect(() => {
    return cleanup
  }, [cleanup])

  return {
    chatState,
    sendMessage,
    retry,
    initializeSession
  }
}
