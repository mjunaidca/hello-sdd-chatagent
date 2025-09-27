# Data Model: Responsive Chat Interface

**Feature**: 002-user-lands-on  
**Date**: 2025-01-27

## Entities

### ChatMessage
Represents a single message in the conversation with content, timestamp, sender type, and status.

**Attributes**:
- `id: string` - Unique message identifier
- `content: string` - Message text content (no length limits, auto-wrap display)
- `timestamp: Date` - When the message was created
- `senderType: 'user' | 'assistant'` - Who sent the message
- `status: 'sending' | 'sent' | 'failed' | 'streaming'` - Current message state
- `sessionId: string` - Associated chat session
- `isTyping: boolean` - Whether this is a typing indicator (for assistant messages)

**Validation Rules**:
- `content` cannot be empty for non-typing messages
- `timestamp` must be valid Date object
- `senderType` must be one of the defined values
- `status` must be one of the defined values
- `sessionId` must be valid UUID format

**State Transitions**:
- User messages: `sending` → `sent` (on successful send)
- User messages: `sending` → `failed` (on send error)
- Assistant messages: `streaming` → `sent` (when streaming complete)
- Assistant messages: `streaming` → `failed` (when streaming fails)

### ChatSession
Represents the current conversation state with message history, user context, and server-side persistence.

**Attributes**:
- `id: string` - Unique session identifier (UUID)
- `userId: string | null` - Associated user ID (null for anonymous)
- `createdAt: Date` - Session creation timestamp
- `lastActivityAt: Date` - Last message or interaction time
- `isActive: boolean` - Whether session is currently active
- `deviceInfo: DeviceInfo` - Information about the user's device
- `messages: ChatMessage[]` - Array of messages in this session

**Validation Rules**:
- `id` must be valid UUID format
- `createdAt` must be before or equal to `lastActivityAt`
- `lastActivityAt` must be valid Date object
- `messages` array must contain valid ChatMessage objects

**State Transitions**:
- `isActive: false` → `isActive: true` (when user sends first message)
- `isActive: true` → `isActive: false` (after session timeout or explicit end)

### DeviceInfo
Represents information about the user's device for cross-device session sharing.

**Attributes**:
- `userAgent: string` - Browser user agent string
- `screenSize: { width: number, height: number }` - Device screen dimensions
- `isMobile: boolean` - Whether device is mobile
- `platform: string` - Operating system platform

**Validation Rules**:
- `screenSize.width` and `screenSize.height` must be positive numbers
- `isMobile` must be boolean
- `platform` cannot be empty string

## Relationships

### ChatSession → ChatMessage (One-to-Many)
- One session can have many messages
- Each message belongs to exactly one session
- Messages are ordered by timestamp within a session
- When session is deleted, all associated messages are deleted

### ChatSession → DeviceInfo (One-to-One)
- Each session has exactly one device info record
- Device info is created when session is first established
- Used for cross-device session sharing and responsive design

## Data Flow

### Message Creation Flow
1. User types message in `ChatInput`
2. `ChatMessage` created with status `sending`
3. Message sent to backend via SSE
4. Status updated to `sent` on success or `failed` on error
5. Message added to `ChatSession.messages` array

### Streaming Response Flow
1. Assistant response starts streaming
2. `ChatMessage` created with status `streaming` and `isTyping: true`
3. Typing indicator shown to user
4. When streaming complete, `isTyping: false` and status `sent`
5. Message added to session history

### Session Persistence Flow
1. Session created on first visit to `/chat`
2. Session stored in Redis for fast access
3. Messages persisted to PostgreSQL for durability
4. Session shared across devices via `sessionId`
5. Session expires after inactivity timeout

## Constraints

### Performance Constraints
- Maximum 1000 messages per session (older messages archived)
- Session timeout: 24 hours of inactivity
- Message content: No length limits (auto-wrap display)
- Auto-scroll: Pauses when user scrolls up, resumes at bottom

### Security Constraints
- All user input sanitized before storage
- Session IDs are cryptographically secure
- No sensitive data in client-side storage
- HTTPS required for production

### Accessibility Constraints
- All interactive elements have ARIA labels
- Keyboard navigation support for all features
- Screen reader compatibility for message content
- High contrast mode support
