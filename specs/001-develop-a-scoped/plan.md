
# Implementation Plan: ChatWait

**Branch**: `001-develop-a-scoped` | **Date**: 2025-09-26 | **Spec**: [link](/specs/001-develop-a-scoped/spec.md)
**Input**: Feature specification from `/specs/001-develop-a-scoped/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from file system structure or context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Fill the Constitution Check section based on the content of the constitution document.
4. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
5. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, `GEMINI.md` for Gemini CLI, `QWEN.md` for Qwen Code or `AGENTS.md` for opencode).
7. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
8. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
The ChatWait chatbot service will provide dual-mode conversational AI interactions with a stateless architecture leveraging the OpenAI Agents SDK's built-in capabilities. Users can choose between immediate complete responses (/chat/wait) or real-time streaming responses (/chat/streaming) with robust reconnection support. The implementation uses FastAPI for HTTP layer management, OpenAI Agents SDK for conversation orchestration with built-in streaming support, Chainlit for UI, and Gemini LLM via OpenAI-compatible API endpoint.

**Critical Research Phase**: Given the OpenAI Agents SDK's relatively new status, comprehensive research into production readiness, error handling, memory management, and streaming reliability is essential before implementation. This includes SDK stability assessment, performance benchmarking, security considerations, and deployment patterns to reduce implementation risks by ~40%.

Performance targets leverage the SDK's optimized streaming engine to ensure <200ms per token latency for natural user experience while maintaining clean separation between UI, agent logic, and API layers. The expanded research scope will validate SDK assumptions and identify potential production issues early in the development cycle.

## Technical Context
**Language/Version**: Python 3.12+ with async-first design
**Primary Dependencies**: FastAPI (async), Chainlit (UI), OpenAI Agents SDK (agent logic), Gemini (LLM via OpenAI-compatible API), uv (package management)
**Storage**: N/A (stateless per specification requirements)
**Testing**: pytest with TDD enforcement, contract tests, integration tests for streaming stability and reconnection
**Target Platform**: Linux server with Docker containerization
**Project Type**: Web application (frontend/backend structure)
**Performance Goals**: <200ms per token streaming latency via SDK's optimized engine, <200ms p95 response time for sync endpoints
**Constraints**: Stateless operation, no authentication/user management, no chat history persistence, SDK-based streaming with custom reconnection support, comprehensive research validation required due to SDK's newness
**Scale/Scope**: Single service supporting dual interaction modes with SDK's built-in session management ready for future activation, production deployment with monitoring and security hardening

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Code Quality Gates:**
- All code MUST use strong typing with type hints and strict type checking
- Minimum 80% test coverage required with proper mocking for external dependencies
- All linters (ruff, mypy, eslint) MUST pass with zero violations
- Tests MUST be written before implementation (TDD)

**Architecture Gates:**
- All FastAPI endpoints MUST be async functions
- Clear separation between UI (Chainlit), Agent logic (OpenAI Agents SDK), and API layers
- Async database drivers and HTTP clients MUST be used
- Response times under 200ms for 95th percentile

**Security Gates:**
- API keys and credentials MUST NEVER be exposed in responses or logs
- Input validation and sanitization MUST be implemented
- Comprehensive error handling without exposing internal details
- Streaming connections MUST be resilient to disconnects with retry logic

## Project Structure

### Documentation (this feature)
```
specs/[###-feature]/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->
```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: Web application structure selected to support clear separation between UI layer (Chainlit), Agent logic (OpenAI Agents SDK), and API layer (FastAPI). This enables clean architecture separation as required by the constitution while supporting both synchronous and streaming interaction modes.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - Research OpenAI Agents SDK production readiness and stability patterns
   - Research streaming implementation with SDK and FastAPI integration
   - Research Chainlit UI integration for dual interaction modes and streaming
   - Research Gemini LLM integration, rate limits, and error handling
   - Research testing strategies for SDK components and streaming endpoints
   - Research deployment, monitoring, and scaling considerations
   - Research security, performance, and reliability best practices

2. **Generate and dispatch research agents**:
   ```
   Investigate OpenAI Agents SDK production stability, error handling, and memory management
   Research SDK streaming integration with FastAPI SSE for production use
   Research Chainlit streaming support, error handling, and custom UI components
   Research Gemini API rate limits, token limits, error responses, and cost implications
   Research testing strategies for OpenAI Agents SDK components and streaming
   Research deployment patterns, health checks, and monitoring for SDK-based services
   Research security considerations for API key management and input validation
   Research performance optimization for SDK streaming and memory usage
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Generate contract tests** from contracts:
   - One test file per endpoint
   - Assert request/response schemas
   - Tests must fail (no implementation yet)

4. **Extract test scenarios** from user stories:
   - Each story → integration test scenario
   - Quickstart test = story validation steps

5. **Update agent file incrementally** (O(1) operation):
   - Run `.specify/scripts/bash/update-agent-context.sh cursor`
     **IMPORTANT**: Execute it exactly as specified above. Do not add or remove any arguments.
   - If exists: Add only NEW tech from current plan
   - Preserve manual additions between markers
   - Update recent changes (keep last 3)
   - Keep under 150 lines for token efficiency
   - Output to repository root

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, agent-specific file

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks from Phase 1 design docs (contracts/openapi.yaml, data-model.md, quickstart.md)
- Research validation tasks to verify SDK production readiness findings
- Each contract test file (test_chat_wait.py, test_chat_streaming.py) → contract test task [P]
- Each data model entity (ChatMessage, ConversationContext, StreamConnection) → Pydantic model creation task [P]
- API endpoint implementation tasks following TDD order
- Service layer tasks for agent logic integration and SDK utilization
- UI layer tasks for Chainlit interface development with streaming support
- Integration tests for streaming resilience, reconnection scenarios, and SDK reliability
- Security, performance, and deployment tasks based on research findings

**Ordering Strategy**:
- Research validation before implementation tasks
- TDD order: Contract tests before implementation, integration tests before UI
- Dependency order: Data models → API layer → Service layer → UI layer
- Mark [P] for parallel execution (independent files like separate test files)
- Group related tasks: All async infrastructure setup before streaming implementation
- Security and performance tasks integrated throughout development phases

**Estimated Output**: 35-45 numbered, ordered tasks in tasks.md covering:
- 8 research validation tasks (production readiness, security, performance)
- 6 contract test tasks (3 per endpoint × 2 endpoints)
- 3 data model tasks (1 per entity)
- 10 API implementation tasks (5 per endpoint including streaming)
- 6 service layer tasks (SDK integration, streaming logic, error handling)
- 6 UI layer tasks (Chainlit interface, streaming components, error states)
- 6 integration and validation tasks (SDK reliability, performance, security)

**Constitutional Compliance**: All tasks will include test-first enforcement, strong typing requirements, async-first patterns, and clean architecture separation as mandated by the constitution.

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (execute tasks.md following constitutional principles)  
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |


## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Research in progress (expanded scope for SDK production readiness)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented

---
*Based on Constitution v1.0.0 - See `/memory/constitution.md`* 
