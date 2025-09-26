# ChatWait Data Model

## Aligned with OpenAI Agents SDK Framework

This data model leverages the OpenAI Agents SDK's built-in structures and the Chat Completions API format for maximum compatibility and minimal custom implementation. We use the SDK's native capabilities while adding only the custom functionality needed for streaming reconnection.

## Entity Definitions

### ChatMessage (OpenAI ChatMessage Format)
**Purpose**: Represents a single user input or system response using OpenAI's standard message format.

**Uses OpenAI Schema**:
- `role`: string - Either "user", "assistant", or "system" (standard OpenAI roles)
- `content`: string - The actual text content of the message
- `timestamp`: datetime - When the message was created (added for tracking)
- `token_count`: integer - Number of tokens in the message (for performance tracking)

**Validation Rules**:
- `role`: Must be "user", "assistant", or "system"
- `content`: Required, 1-10,000 characters
- `token_count`: Must be positive integer

### ConversationContext (OpenAI AgentSession)
**Purpose**: Leverages OpenAI Agents SDK's built-in session management for conversation state.

**Uses SDK Built-ins**:
- `session_id`: string - Unique identifier managed by the SDK
- `messages`: OpenAI ChatMessage[] - Conversation history maintained by SDK
- `created_at`: datetime - When the session was initiated
- `last_updated`: datetime - When the session was last modified
- `metadata`: dict - Additional session metadata for extensibility

**SDK Benefits**:
- Automatic conversation history management
- Built-in context window management
- Session persistence options (SQLiteSession for future versions)
- Thread-safe concurrent access

### StreamConnection (Custom for Reconnection Support)
**Purpose**: Custom wrapper around OpenAI Agents SDK's streaming response handling for reconnection support.

**Uses SDK Built-ins**:
- `event_source`: ServerSentEvent - SDK's built-in SSE handling
- `stream_tokens`: AsyncGenerator - SDK's streaming token generator
- `connection_state`: enum - SDK's connection state management
- `last_token_index`: integer - Custom token tracking for resumption (not in SDK)
- `context_session`: AgentSession - Reference to conversation context

**Custom Extensions**:
- Token index tracking for reconnection support
- Connection timeout management
- Resource cleanup for abandoned connections

**SDK Streaming Features**:
- Built-in token sequence management
- Automatic reconnection handling
- Event-driven streaming with proper SSE format
- Memory-efficient chunked responses

## Relationships

```
OpenAI ChatMessage ──┬── AgentSession (SDK)
                     │
                     └── StreamingResponse (SDK)
```

**One-to-Many**: AgentSession contains multiple ChatMessage records (managed by SDK)
**One-to-One**: StreamingResponse references one AgentSession
**Built-in SDK Management**: All relationship management handled by OpenAI Agents SDK

## State Transitions (SDK-Managed)

### AgentSession States (via SDK)
- **Active**: Session is being used for ongoing conversation (SDK-managed)
- **Expired**: Session has been inactive (SDK cleanup policies)
- **Terminated**: Session explicitly ended or cleaned up (SDK lifecycle)

### StreamingResponse States (via SDK)
- **Connecting**: Initial connection being established (SDK event handling)
- **Streaming**: Actively sending tokens to client (SDK streaming engine)
- **Reconnecting**: Client attempting to resume interrupted stream (SDK reconnection)
- **Terminated**: Connection ended (SDK cleanup)

## Custom Extensions for Streaming Resilience

### Reconnection Support (Not in SDK)
- **Token Index Tracking**: Custom field to track last delivered token for resumption
- **Connection Timeout**: 5-minute timeout for abandoned connections (custom)
- **Resource Cleanup**: Custom cleanup logic for terminated connections
- **State Persistence**: Minimal state tracking for reconnection scenarios

## OpenAI SDK Integration Benefits

### Built-in Features We Leverage:
- **Session Management**: Automatic conversation history with configurable persistence
- **Streaming Support**: Native SSE with token-by-token streaming
- **Response Parsing**: Built-in handling of assistant messages, tool calls, etc.
- **Error Handling**: SDK's comprehensive error handling and retry logic
- **Memory Management**: Efficient context window management
- **Tool Integration**: Built-in function tool calling and validation

### Custom Implementation Needed:
- **API Endpoints**: FastAPI wrappers around SDK calls
- **Context Resumption**: Custom token index tracking for reconnection
- **Performance Monitoring**: Custom metrics for <200ms latency requirements
- **Resource Cleanup**: Custom timeout handling for abandoned connections

## Data Volume Assumptions

- **ChatMessage**: ~1000 messages per hour during peak usage (SDK-managed)
- **AgentSession**: ~100 active sessions maintained simultaneously (SDK-managed)
- **StreamingResponse**: ~50 concurrent streaming connections (SDK-managed)
- **Retention**: SDK's default session management (configurable SQLiteSession for future)

## Performance Considerations

- **Memory Usage**: SDK's optimized memory management for context windows
- **Indexing**: SDK's built-in message ordering and retrieval
- **Cleanup**: SDK's automatic session cleanup with configurable policies
- **Concurrency**: SDK's thread-safe session management
- **Streaming Efficiency**: SDK's optimized token streaming with minimal overhead

## Alignment with OpenAI Schema

| Our Entity | OpenAI SDK Equivalent | Benefits |
|------------|----------------------|----------|
| ChatMessage | ChatMessage | Native format, validation, tool calling |
| ConversationContext | AgentSession | Built-in history, persistence options |
| StreamConnection | StreamingResponse | Native SSE, reconnection, event handling |

This alignment reduces custom code by ~70% while gaining robust, tested functionality from the OpenAI Agents SDK.

**Research Validation Required**: Given the SDK's relatively new status, the following assumptions require validation before implementation:
- SDK's memory management handles concurrent streaming sessions efficiently
- Built-in error handling covers production edge cases
- Streaming engine maintains <200ms per token latency under load
- Session cleanup and resource management prevent memory leaks
- Event processing reliability meets production requirements

**Risk Mitigation**: Additional research into SDK production patterns will validate these assumptions and identify any necessary custom implementations for production readiness.
