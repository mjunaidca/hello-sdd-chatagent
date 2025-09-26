# ChatWait Quickstart Validation

## Overview
This document provides step-by-step validation scenarios to test the ChatWait chatbot service functionality. Each scenario validates specific user stories and acceptance criteria from the specification.

## Prerequisites
- ChatWait service running on http://localhost:8000
- curl or similar HTTP client available
- Text editor for viewing streaming responses

## Test Scenario 1: Synchronous Chat (FR-001)
**Validates**: /chat/wait endpoint functionality

```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you today?"}'
```

**Expected Response**:
```json
{
  "message": "Hello! I'm doing well, thank you for asking. How can I help you today?",
  "context_id": "123e4567-e89b-12d3-a456-426614174000",
  "token_count": 15,
  "processing_time_ms": 245.6
}
```

**Validation Steps**:
1. ✅ Verify response contains complete message
2. ✅ Verify context_id is valid UUID
3. ✅ Verify token_count is reasonable for response length
4. ✅ Verify processing_time_ms is under 200ms (performance requirement)

## Test Scenario 2: Streaming Chat (FR-002)
**Validates**: /chat/streaming endpoint with SSE functionality

**Step 1: Start streaming request**
```bash
curl -N "http://localhost:8000/chat/streaming?message=Tell%20me%20about%20Python%20async%20programming"
```

**Expected Response Stream**:
```
data: {"token": "Python", "token_index": 0, "context_id": "123e4567-e89b-12d3-a456-426614174000"}
data: {"token": " ", "token_index": 1, "context_id": "123e4567-e89b-12d3-a456-426614174000"}
data: {"token": "async", "token_index": 2, "context_id": "123e4567-e89b-12d3-a456-426614174000"}
data: {"token": " ", "token_index": 3, "context_id": "123e4567-e89b-12d3-a456-426614174000"}
data: {"token": "programming", "token_index": 4, "context_id": "123e4567-e89b-12d3-a456-426614174000"}
...
data: {"type": "end", "context_id": "123e4567-e89b-12d3-a456-426614174000"}
```

**Validation Steps**:
1. ✅ Verify SSE event format with token and token_index
2. ✅ Verify context_id consistency across all events
3. ✅ Verify token_index increments sequentially
4. ✅ Verify "end" event received at completion
5. ✅ Verify per-token latency <200ms (performance requirement)

## Test Scenario 3: Streaming Reconnection (FR-003)
**Validates**: Streaming resilience and reconnection capability

**Step 1: Start initial streaming request**
```bash
curl -N "http://localhost:8000/chat/streaming?message=Write%20a%20short%20story%20about%20AI"
```

**Step 2: Monitor until you see token_index=5, then interrupt connection**

**Step 3: Reconnect with last_token_index**
```bash
curl -N "http://localhost:8000/chat/streaming?message=Write%20a%20short%20story%20about%20AI&last_token_index=5&context_id=<context_id_from_step1>"
```

**Expected Response**:
- Stream resumes from token_index=6 (no duplicate tokens)
- No context loss in the story continuation
- Consistent context_id across reconnection

**Validation Steps**:
1. ✅ Verify reconnection resumes from correct token_index
2. ✅ Verify no duplicate tokens sent
3. ✅ Verify context continuity maintained
4. ✅ Verify same context_id preserved

## Test Scenario 4: Error Handling (FR-004)
**Validates**: Error response format and user-friendly messages

**Test 1: Missing message parameter**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response**:
```json
{
  "error_code": "MISSING_MESSAGE",
  "message": "Message content is required and must be between 1 and 10000 characters"
}
```

**Test 2: Empty message**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
```

**Expected Response**:
```json
{
  "error_code": "EMPTY_MESSAGE",
  "message": "Message cannot be empty. Please provide a valid message."
}
```

**Test 3: Message too long**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "'$(python3 -c 'print("x" * 10001)')'"}'
```

**Expected Response**:
```json
{
  "error_code": "MESSAGE_TOO_LONG",
  "message": "Message exceeds maximum length of 10000 characters"
}
```

**Validation Steps**:
1. ✅ Verify all error responses use JSON format with error_code and message
2. ✅ Verify error messages are user-friendly and actionable
3. ✅ Verify no internal implementation details exposed
4. ✅ Verify appropriate HTTP status codes returned

## Test Scenario 5: Multi-turn Conversation (FR-005)
**Validates**: Conversational context awareness

**Step 1: Initial message**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "What is machine learning?"}'
```

**Step 2: Follow-up with context**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "Can you give me a simple example?", "context_id": "<context_id_from_step1>"}'
```

**Expected Response**:
- Second response should reference machine learning concepts
- Should provide a practical example related to the ML explanation

**Validation Steps**:
1. ✅ Verify second response shows understanding of previous context
2. ✅ Verify context_id is maintained across turns
3. ✅ Verify conversational flow is natural and coherent

## Test Scenario 6: Performance Validation (FR-007)
**Validates**: Natural streaming latency requirement

```bash
#!/bin/bash
# Measure streaming latency
start_time=$(date +%s%N)
curl -N "http://localhost:8000/chat/streaming?message=Explain%20quantum%20computing" | \
  while read line; do
    if [[ $line == data:* ]]; then
      current_time=$(date +%s%N)
      latency_ms=$(( (current_time - start_time) / 1000000 ))
      echo "Token latency: ${latency_ms}ms"
      start_time=$current_time
      # Break after first few tokens to check initial latency
      token_count=$((token_count + 1))
      if [ $token_count -gt 3 ]; then break; fi
    fi
  done
```

**Validation Steps**:
1. ✅ Verify per-token latency <200ms
2. ✅ Verify consistent latency across tokens
3. ✅ Verify overall response time reasonable for content length

## Test Scenario 7: Extensibility Validation (FR-008, FR-011)
**Validates**: Optional client-managed context support

**Step 1: Request without context (should work)**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

**Step 2: Request with context (should work identically)**
```bash
curl -X POST http://localhost:8000/chat/wait \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "context_id": "optional-context-123"}'
```

**Validation Steps**:
1. ✅ Both requests succeed regardless of context_id presence
2. ✅ No breaking changes when optional parameters are included
3. ✅ System designed for future extensibility

## Cleanup
- Stop the ChatWait service when testing is complete
- All tests should be repeatable without side effects (stateless design)

## Success Criteria
- ✅ All 7 test scenarios pass
- ✅ No internal errors or implementation details exposed
- ✅ Performance requirements met (<200ms latency)
- ✅ Both interaction modes work reliably
- ✅ Error handling provides clear, actionable feedback
