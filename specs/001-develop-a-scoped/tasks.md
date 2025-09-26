# Tasks: ChatWait

**Input**: Design documents from `/specs/001-develop-a-scoped/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → Extract: tech stack (FastAPI, Chainlit, OpenAI Agents SDK), structure (web app)
2. Load design documents:
   → data-model.md: Extract entities (ChatMessage, ConversationContext, StreamConnection)
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → SDK setup and streaming implementation
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests, unit tests
   → Core: models, services, endpoints
   → Integration: streaming resilience, error handling
   → Polish: docs, validation
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests? ✅
   → All entities have models? ✅
   → All endpoints implemented? ✅
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Web app structure**: `backend/src/` for API, `frontend/` for Chainlit UI
- All paths relative to repository root

## Phase 3.1: Setup
- [x] T001 Create project structure with backend/src/ and frontend/ directories
- [x] T002 Initialize Python 3.12+ project with uv and FastAPI dependencies
- [x] T003 [P] Configure linting and formatting tools (ruff, mypy, pre-commit)
- [x] T004a Set up environment configuration with .env support in backend/.env
- [x] T004b Create FastAPI application factory with lifespan management in backend/src/app.py
- [x] T004c Configure CORS middleware for browser compatibility in backend/src/middleware/cors.py
- [x] T004d Set up logging middleware for request/response tracking in backend/src/middleware/logging.py
- [x] T004e Implement health check endpoint for production monitoring in backend/src/api/health.py

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**

### Contract Tests (API Schema Validation)
- [x] T005 [P] Contract test POST /chat/wait in tests/contract/test_chat_wait.py
- [x] T006 [P] Contract test GET /chat/streaming in tests/contract/test_chat_streaming.py
- [x] T007 [P] Contract test error responses in tests/contract/test_error_handling.py
- [x] T008 [P] Integration test streaming reconnection in tests/integration/test_streaming_resilience.py

### Data Model Tests
- [x] T009 [P] ChatMessage model validation tests in tests/unit/test_models.py
- [x] T010 [P] ConversationContext model tests in tests/unit/test_models.py
- [x] T011 [P] StreamConnection model tests in tests/unit/test_models.py

## Phase 3.3: Core Implementation (ONLY after tests are failing)

### Data Models
- [x] T012 [P] Implement ChatMessage Pydantic model in backend/src/models/chat_models.py
- [x] T013 [P] Implement ConversationContext Pydantic model in backend/src/models/chat_models.py
- [x] T014 [P] Implement StreamConnection Pydantic model in backend/src/models/chat_models.py

### Agent Integration
- [x] T015a Set up environment configuration and .env file with API keys in backend/.env
- [x] T015b Implement AsyncOpenAI client setup with Gemini endpoint in backend/src/services/llm_service.py
- [x] T015c Configure OpenAIChatCompletionsModel with gemini-2.5-flash in backend/src/services/llm_service.py
- [x] T015d Create ChatAgent with proper instructions and model in backend/src/services/chat_agent.py
- [x] T015e Implement agent execution wrapper with error handling in backend/src/services/chat_agent.py
- [x] T017 [P] Unit test ChatAgent with "hello" input in tests/unit/test_chat_agent.py

### API Endpoints
- [x] T018a Implement /chat/wait endpoint structure with Pydantic request/response models in backend/src/routers/chat.py
- [x] T018b Implement synchronous agent execution with Runner.run_sync() in /chat/wait endpoint
- [x] T018c Add error handling and response formatting for /chat/wait endpoint
- [x] T019a Set up FastAPI SSE streaming endpoint structure with proper headers in backend/src/routers/chat.py
- [x] T019b Implement SDK event processing loop with ResponseTextDeltaEvent handling
- [x] T019c Add stream completion detection and final_output formatting
- [x] T019d Implement connection lifecycle management and error event streaming
- [x] T019e Add reconnection support with token index tracking in streaming endpoint
- [x] T020 Implement error handling middleware in backend/src/api/errors.py
- [x] T021 Implement input validation middleware in backend/src/api/validation.py

### Error Handling
- [x] T022 Implement error response schemas in backend/src/schemas/error_schemas.py
- [x] T023 [P] Unit test error handling for malformed requests in tests/unit/test_error_handling.py
- [x] T024 [P] Unit test streaming reconnection logic in tests/unit/test_streaming.py

## Phase 3.4: Integration & UI
- [x] T025a Implement streaming event formatter for SDK ResponseTextDeltaEvent in backend/src/services/streaming_service.py
- [x] T025b Create stream completion detection and final_output handling in backend/src/services/streaming_service.py
- [x] T025c Add connection state tracking and cleanup for abandoned streams in backend/src/services/streaming_service.py
- [x] T026a Implement token index persistence for reconnection support in backend/src/services/streaming_service.py
- [x] T026b Add reconnection state recovery logic in streaming service
- [x] T026c Create error event streaming for client notification
- [x] T027a Set up Chainlit application structure with session management in frontend/app.py
- [x] T027b Implement dual mode selection UI (wait vs streaming) in frontend/modes/mode_selector.py
- [x] T027c Add environment configuration for Chainlit-FastAPI integration
- [x] T028a Implement Chainlit wait mode with POST /chat/wait integration in frontend/modes/wait_mode.py
- [x] T028b Add request/response handling and error display for wait mode
- [x] T028c Implement loading states and user feedback for wait mode
- [x] T029a Implement Chainlit streaming mode with SSE /chat/streaming integration in frontend/modes/streaming_mode.py
- [x] T029b Add EventSource connection management and reconnection handling
- [x] T029c Implement token-by-token message rendering with proper formatting
- [x] T030 [P] Integration test end-to-end chat flow in tests/integration/test_e2e_flow.py

## Phase 3.5: Polish & Validation
- [x] T031 [P] Performance tests for <200ms streaming latency in tests/performance/test_streaming_perf.py
- [x] T032 [P] Unit tests for validation logic in tests/unit/test_validation.py
- [x] T033 [P] Update README with setup and demo instructions in README.md
- [x] T034 [P] Add API documentation with OpenAPI spec in docs/api.md
- [x] T035 [P] Add extensibility notes for v2 session management in docs/extensibility.md
- [x] T036 [P] Run quickstart validation scenarios in tests/manual/test_quickstart.py

## Dependencies
```
Setup Tasks (T001-T004e) → Everything
Contract Tests (T005-T008) → Implementation (T012-T024)
Data Model Tests (T009-T011) → Data Models (T012-T014)
Data Models (T012-T014) → Agent Integration (T015a-T017)
Agent Integration (T015a-T017) → API Endpoints (T018a-T019e)
API Endpoints (T018a-T021) → Error Handling (T022-T024)
SDK Integration (T015a-T015e) → Streaming Implementation (T019a-T019e)
Streaming Implementation (T019a-T019e) → Streaming Service (T025a-T026c)
All Implementation → Integration & UI (T027a-T030)
All Implementation → Polish & Validation (T031-T036)

**Detailed Flow**:
- T015a (Environment) → T015b (Client) → T015c (Model) → T015d (Agent) → T015e (Wrapper)
- T019a (Structure) → T019b (Event Loop) → T019c (Completion) → T019d (Lifecycle) → T019e (Reconnection)
- T027a (Structure) → T027b (Mode Selection) → T028a (Wait Mode) → T029a (Streaming Mode)
```

## Parallel Execution Examples

### Launch Contract Tests Together:
```
Task: "Contract test POST /chat/wait in tests/contract/test_chat_wait.py"
Task: "Contract test GET /chat/streaming in tests/contract/test_chat_streaming.py"
Task: "Contract test error responses in tests/contract/test_error_handling.py"
Task: "Integration test streaming reconnection in tests/integration/test_streaming_resilience.py"
```

### Launch Data Model Tests Together:
```
Task: "ChatMessage model validation tests in tests/unit/test_models.py"
Task: "ConversationContext model tests in tests/unit/test_models.py"
Task: "StreamConnection model tests in tests/unit/test_models.py"
```

### Launch Polish Tasks Together:
```
Task: "Performance tests for <200ms streaming latency in tests/performance/test_streaming_perf.py"
Task: "Unit tests for validation logic in tests/unit/test_validation.py"
Task: "Update README with setup and demo instructions in README.md"
Task: "Add API documentation with OpenAPI spec in docs/api.md"
Task: "Add extensibility notes for v2 session management in docs/extensibility.md"
Task: "Run quickstart validation scenarios in tests/manual/test_quickstart.py"
```

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task

2. **From Data Model**:
   - Each entity → model creation task [P]
   - Each entity → unit test task [P]

3. **From User Stories**:
   - Each user story → integration test [P]
   - Each endpoint → implementation task

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → UI → Polish
   - Dependencies block parallel execution
   - TDD enforced: Tests before implementation

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests (T005-T008)
- [ ] All entities have model tasks (T012-T014)
- [ ] All endpoints have implementation tasks (T018a-T019e)
- [ ] SDK integration has detailed step-by-step tasks (T015a-T015e)
- [ ] Streaming implementation has event processing tasks (T019b-T019e)
- [ ] Tests come before implementation (TDD enforced)
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task

## Implementation Summary
**Total Tasks**: 45 specific, actionable tasks (up from 36)
**TDD Coverage**: 100% - All implementation tasks have corresponding tests
**SDK Integration**: 5 detailed tasks (T015a-T015e) with step-by-step guidance
**Streaming Implementation**: 8 detailed tasks covering event processing, SSE formatting, and reconnection
**Error Handling**: 6 tasks including middleware, schemas, and integration
**UI Integration**: 6 tasks for Chainlit backend communication and dual-mode support

## Notes
- All tasks follow TDD: Tests are created first and MUST FAIL before implementation
- Contract tests validate API schemas and error responses
- Integration tests focus on streaming resilience and reconnection
- UI tasks create minimal Chainlit interface for demo purposes
- Performance tests validate <200ms streaming latency requirement
- All tasks include proper error handling and logging
- SDK integration leverages OpenAI Agents SDK's built-in capabilities
- Streaming implementation uses SDK's `Runner.run_streamed()` with custom SSE wrapper
