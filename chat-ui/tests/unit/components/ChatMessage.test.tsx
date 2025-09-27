/**
 * @jest-environment jsdom
 */

import React from 'react'
import { render, screen } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ChatMessage } from '@/components/chat/ChatMessage'
import { ChatMessage as ChatMessageType } from '@/lib/types'

const mockUserMessage: ChatMessageType = {
  id: 'msg-1',
  content: 'Hello, world!',
  timestamp: new Date('2024-01-01T12:00:00Z'),
  senderType: 'user',
  status: 'sent',
  sessionId: 'session-1',
  isTyping: false
}

const mockAssistantMessage: ChatMessageType = {
  id: 'msg-2',
  content: 'Hi there! How can I help you?',
  timestamp: new Date('2024-01-01T12:01:00Z'),
  senderType: 'assistant',
  status: 'sent',
  sessionId: 'session-1',
  isTyping: false
}

const mockStreamingMessage: ChatMessageType = {
  id: 'msg-3',
  content: '',
  timestamp: new Date('2024-01-01T12:02:00Z'),
  senderType: 'assistant',
  status: 'streaming',
  sessionId: 'session-1',
  isTyping: true
}

describe('ChatMessage Component', () => {
  it('should render user message correctly', () => {
    render(<ChatMessage message={mockUserMessage} />)
    
    expect(screen.getByText('Hello, world!')).toBeInTheDocument()
    expect(screen.getByText('U')).toBeInTheDocument()
    expect(screen.getByRole('article', { name: 'Message from you' })).toBeInTheDocument()
  })

  it('should render assistant message correctly', () => {
    render(<ChatMessage message={mockAssistantMessage} />)
    
    expect(screen.getByText('Hi there! How can I help you?')).toBeInTheDocument()
    expect(screen.getByText('A')).toBeInTheDocument()
    expect(screen.getByRole('article', { name: 'Message from assistant' })).toBeInTheDocument()
  })

  it('should render streaming message correctly', () => {
    render(<ChatMessage message={mockStreamingMessage} />)
    
    expect(screen.getByText('Thinking...')).toBeInTheDocument()
    expect(screen.getByText('A')).toBeInTheDocument()
  })

  it('should show correct timestamp format', () => {
    render(<ChatMessage message={mockUserMessage} />)
    
    // The exact format depends on the formatMessageTime function
    // This is a basic check that some time is displayed
    expect(screen.getByText(/12:00/)).toBeInTheDocument()
  })

  it('should show status icons for different message states', () => {
    const { rerender } = render(<ChatMessage message={mockUserMessage} />)
    
    // Check for sent status icon
    expect(screen.getByTestId('status-icon')).toBeInTheDocument()
    
    // Test failed message
    const failedMessage = { ...mockUserMessage, status: 'failed' as const }
    rerender(<ChatMessage message={failedMessage} />)
    
    // Check for failed status icon
    expect(screen.getByTestId('status-icon')).toBeInTheDocument()
  })

  it('should sanitize message content', () => {
    const messageWithScript = {
      ...mockUserMessage,
      content: 'Hello <script>alert("xss")</script> world!'
    }
    
    render(<ChatMessage message={messageWithScript} />)
    
    expect(screen.getByText('Hello  world!')).toBeInTheDocument()
    expect(screen.queryByText('script')).not.toBeInTheDocument()
  })

  it('should handle empty content gracefully', () => {
    const emptyMessage = { ...mockUserMessage, content: '' }
    
    render(<ChatMessage message={emptyMessage} />)
    
    expect(screen.getByRole('article')).toBeInTheDocument()
  })
})
