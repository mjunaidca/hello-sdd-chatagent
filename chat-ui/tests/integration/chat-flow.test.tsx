/**
 * @jest-environment jsdom
 */

import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ChatContainer } from '@/components/chat/ChatContainer'

// Mock the useChatStream hook
jest.mock('@/hooks/useChatStream', () => ({
  useChatStream: () => ({
    chatState: {
      session: {
        id: 'test-session-123',
        userId: null,
        createdAt: new Date(),
        lastActivityAt: new Date(),
        isActive: true,
        deviceInfo: {
          userAgent: 'test-agent',
          screenSize: { width: 1920, height: 1080 },
          isMobile: false,
          platform: 'test'
        },
        messages: []
      },
      messages: [],
      isConnected: true,
      isStreaming: false,
      error: null,
      retryCount: 0
    },
    sendMessage: jest.fn(),
    retry: jest.fn(),
    initializeSession: jest.fn()
  })
}))

describe('Chat Flow Integration Tests', () => {
  it('should render chat interface', () => {
    render(<ChatContainer />)
    
    expect(screen.getByRole('main', { name: 'Chat interface' })).toBeInTheDocument()
    expect(screen.getByText('Chat Assistant')).toBeInTheDocument()
    expect(screen.getByText('Connected')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Type your message...')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Send message' })).toBeInTheDocument()
  })

  it('should show empty state when no messages', () => {
    render(<ChatContainer />)
    
    expect(screen.getByText('Start a conversation by typing a message below.')).toBeInTheDocument()
  })

  it('should handle message input', () => {
    render(<ChatContainer />)
    
    const input = screen.getByPlaceholderText('Type your message...')
    fireEvent.change(input, { target: { value: 'Hello, world!' } })
    
    expect(input).toHaveValue('Hello, world!')
  })

  it('should submit message on enter key', () => {
    const mockSendMessage = jest.fn()
    jest.doMock('@/hooks/useChatStream', () => ({
      useChatStream: () => ({
        chatState: {
          session: { id: 'test-session-123' },
          messages: [],
          isConnected: true,
          isStreaming: false,
          error: null,
          retryCount: 0
        },
        sendMessage: mockSendMessage,
        retry: jest.fn(),
        initializeSession: jest.fn()
      })
    }))

    render(<ChatContainer />)
    
    const input = screen.getByPlaceholderText('Type your message...')
    fireEvent.change(input, { target: { value: 'Test message' } })
    fireEvent.keyDown(input, { key: 'Enter', code: 'Enter' })
    
    expect(mockSendMessage).toHaveBeenCalledWith('Test message')
  })

  it('should submit message on send button click', () => {
    const mockSendMessage = jest.fn()
    jest.doMock('@/hooks/useChatStream', () => ({
      useChatStream: () => ({
        chatState: {
          session: { id: 'test-session-123' },
          messages: [],
          isConnected: true,
          isStreaming: false,
          error: null,
          retryCount: 0
        },
        sendMessage: mockSendMessage,
        retry: jest.fn(),
        initializeSession: jest.fn()
      })
    }))

    render(<ChatContainer />)
    
    const input = screen.getByPlaceholderText('Type your message...')
    const sendButton = screen.getByRole('button', { name: 'Send message' })
    
    fireEvent.change(input, { target: { value: 'Test message' } })
    fireEvent.click(sendButton)
    
    expect(mockSendMessage).toHaveBeenCalledWith('Test message')
  })

  it('should disable input when streaming', () => {
    jest.doMock('@/hooks/useChatStream', () => ({
      useChatStream: () => ({
        chatState: {
          session: { id: 'test-session-123' },
          messages: [],
          isConnected: true,
          isStreaming: true,
          error: null,
          retryCount: 0
        },
        sendMessage: jest.fn(),
        retry: jest.fn(),
        initializeSession: jest.fn()
      })
    }))

    render(<ChatContainer />)
    
    const input = screen.getByPlaceholderText('Type your message...')
    const sendButton = screen.getByRole('button', { name: 'Send message' })
    
    expect(input).toBeDisabled()
    expect(sendButton).toBeDisabled()
  })

  it('should show error banner when there is an error', () => {
    jest.doMock('@/hooks/useChatStream', () => ({
      useChatStream: () => ({
        chatState: {
          session: { id: 'test-session-123' },
          messages: [],
          isConnected: false,
          isStreaming: false,
          error: 'Connection failed',
          retryCount: 1
        },
        sendMessage: jest.fn(),
        retry: jest.fn(),
        initializeSession: jest.fn()
      })
    }))

    render(<ChatContainer />)
    
    expect(screen.getByText('Connection failed')).toBeInTheDocument()
    expect(screen.getByText('Retry attempt 1')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument()
  })
})
