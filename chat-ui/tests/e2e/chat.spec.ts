import { test, expect } from '@playwright/test'

test.describe('Chat Interface E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Mock the streaming API response
    await page.route('**/api/v1/chat/streaming*', async (route) => {
      // Mock EventSource for streaming
      await page.evaluate(() => {
        class MockEventSource {
          onmessage = null
          onerror = null
          readyState = 1
          url = ''
          
          constructor(url: string) {
            this.url = url
            // Simulate streaming response
            setTimeout(() => {
              if (this.onmessage) {
                this.onmessage({
                  data: JSON.stringify({
                    token: 'Hello',
                    token_index: 0,
                    context_id: 'test-session-123',
                    type: 'token'
                  })
                })
              }
            }, 100)
            
            setTimeout(() => {
              if (this.onmessage) {
                this.onmessage({
                  data: JSON.stringify({
                    token: ' world!',
                    token_index: 1,
                    context_id: 'test-session-123',
                    type: 'token'
                  })
                })
              }
            }, 200)
            
            setTimeout(() => {
              if (this.onmessage) {
                this.onmessage({
                  data: JSON.stringify({
                    type: 'end',
                    context_id: 'test-session-123'
                  })
                })
              }
            }, 300)
          }
          
          close() {}
        }
        
        // @ts-ignore
        window.EventSource = MockEventSource
      })
      
      await route.fulfill({
        status: 200,
        contentType: 'text/event-stream',
        body: 'data: {"token": "Hello", "token_index": 0, "context_id": "test-session-123", "type": "token"}\n\n'
      })
    })

    await page.goto('/chat')
  })

  test('should load chat interface', async ({ page }) => {
    await expect(page.getByRole('main', { name: 'Chat interface' })).toBeVisible()
    await expect(page.getByText('Chat Assistant')).toBeVisible()
    await expect(page.getByText('Connected')).toBeVisible()
    await expect(page.getByPlaceholderText('Type your message...')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Send message' })).toBeVisible()
  })

  test('should show empty state initially', async ({ page }) => {
    await expect(page.getByText('Start a conversation by typing a message below.')).toBeVisible()
  })

  test('should send a message', async ({ page }) => {
    const input = page.getByPlaceholderText('Type your message...')
    const sendButton = page.getByRole('button', { name: 'Send message' })
    
    await input.fill('Hello, world!')
    await sendButton.click()
    
    // Wait for the message to appear
    await expect(page.getByText('Hello, world!')).toBeVisible()
  })

  test('should send message on Enter key', async ({ page }) => {
    const input = page.getByPlaceholderText('Type your message...')
    
    await input.fill('Test message')
    await input.press('Enter')
    
    // Wait for the message to appear
    await expect(page.getByText('Test message')).toBeVisible()
  })

  test('should handle long messages', async ({ page }) => {
    const longMessage = 'This is a very long message that should wrap properly in the chat interface. '.repeat(10)
    const input = page.getByPlaceholderText('Type your message...')
    const sendButton = page.getByRole('button', { name: 'Send message' })
    
    await input.fill(longMessage)
    await sendButton.click()
    
    // Wait for the message to appear
    await expect(page.getByText(longMessage)).toBeVisible()
  })

  test('should be responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 })
    
    // Check that the interface is still usable on mobile
    await expect(page.getByRole('main', { name: 'Chat interface' })).toBeVisible()
    await expect(page.getByPlaceholderText('Type your message...')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Send message' })).toBeVisible()
  })

  test('should handle keyboard navigation', async ({ page }) => {
    const input = page.getByPlaceholderText('Type your message...')
    const sendButton = page.getByRole('button', { name: 'Send message' })
    
    // Tab to the input
    await page.keyboard.press('Tab')
    await expect(input).toBeFocused()
    
    // Type a message
    await input.fill('Keyboard test')
    
    // Tab to the send button
    await page.keyboard.press('Tab')
    await expect(sendButton).toBeFocused()
    
    // Press Enter to send
    await page.keyboard.press('Enter')
    
    // Wait for the message to appear
    await expect(page.getByText('Keyboard test')).toBeVisible()
  })

  test('should show connection status', async ({ page }) => {
    // Check that connection status is visible
    await expect(page.getByText('Connected')).toBeVisible()
    
    // The connection indicator should be green
    const statusIndicator = page.locator('[aria-label="Connection status: Connected"]')
    await expect(statusIndicator).toBeVisible()
  })

  test('should handle input validation', async ({ page }) => {
    const input = page.getByPlaceholderText('Type your message...')
    const sendButton = page.getByRole('button', { name: 'Send message' })
    
    // Try to send empty message
    await input.fill('')
    await expect(sendButton).toBeDisabled()
    
    // Try to send message with only whitespace
    await input.fill('   ')
    await expect(sendButton).toBeDisabled()
    
    // Send valid message
    await input.fill('Valid message')
    await expect(sendButton).toBeEnabled()
  })

  test('should scroll to bottom on new messages', async ({ page }) => {
    // Send multiple messages to create scrollable content
    const input = page.getByPlaceholderText('Type your message...')
    const sendButton = page.getByRole('button', { name: 'Send message' })
    
    for (let i = 1; i <= 5; i++) {
      await input.fill(`Message ${i}`)
      await sendButton.click()
      await expect(page.getByText(`Message ${i}`)).toBeVisible()
    }
    
    // The last message should be visible (scrolled to bottom)
    await expect(page.getByText('Message 5')).toBeVisible()
  })
})
