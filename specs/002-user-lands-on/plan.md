
# Implementation Plan: Responsive Chat Interface

**Branch**: `002-user-lands-on` | **Date**: 2025-01-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-user-lands-on/spec.md`

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
Build a responsive chat interface using Next.js 15, Tailwind CSS, ShadCN/ui, and Framer Motion. Users land on `/chat` to see a mobile-first chat window where they can send messages and receive real-time streaming responses with typing indicators, error handling, and smooth animations. The interface supports server-side session persistence and auto-scrolling with pause-on-scroll behavior.

## Technical Context
**Language/Version**: TypeScript 5.0+ with Next.js 15  
**Primary Dependencies**: Next.js 15, Tailwind CSS, ShadCN/ui, Framer Motion, Server-Sent Events (SSE)  
**Package Manager**: pnpm (JavaScript/TypeScript projects)  
**Storage**: Server-side session storage (Redis/PostgreSQL for chat sessions)  
**Testing**: Jest, Playwright (E2E), React Testing Library  
**Target Platform**: Web (mobile-first responsive design)  
**Project Type**: web (frontend-only with backend API integration)  
**Performance Goals**: <200ms response time, 60fps animations, smooth streaming  
**UX Requirements**: Mobile-first, WCAG 2.1 AA accessibility, shadcn/ui components, Framer Motion animations  
**Constraints**: Real-time streaming, auto-scroll with pause, typing indicators, error recovery  
**Scale/Scope**: Single chat interface, server-side session persistence, cross-device compatibility

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Code Quality Gates:**
- All code MUST use strong typing with type hints and strict type checking
- Minimum 80% test coverage required with proper mocking for external dependencies
- All linters (ruff, mypy, eslint) MUST pass with zero violations
- Tests MUST be written before implementation (TDD)

**Architecture Gates:**
- Clear separation between UI (Next.js), streaming logic (SSE), and backend API layers
- Async HTTP clients and streaming connections MUST be used
- Response times under 200ms for 95th percentile
- Server-Sent Events for real-time streaming

**CLI-First Gates:**
- All projects MUST be initialized using CLI tools (pnpm create, uv init --package)
- Use pnpm for JavaScript/TypeScript projects, uv for Python projects
- All setup instructions MUST be executable via CLI commands

**UX-First Gates:**
- Mobile-first responsive design MUST be implemented
- WCAG 2.1 AA accessibility standards MUST be met
- shadcn/ui components MUST be used for consistent design patterns
- Real UX flows MUST be established before placeholder test generation

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
```
chat-ui/                          # Next.js 15 frontend application
├── app/
│   ├── chat/
│   │   └── page.tsx             # Main chat page
│   ├── globals.css              # Global styles with Tailwind
│   └── layout.tsx               # Root layout
├── components/
│   ├── chat/
│   │   ├── ChatContainer.tsx    # Main chat container
│   │   ├── ChatInput.tsx        # Message input with send button
│   │   ├── ChatMessage.tsx      # Message bubble component
│   │   ├── TypingIndicator.tsx  # Animated typing indicator
│   │   └── ErrorBanner.tsx      # Error display component
│   └── ui/                      # ShadCN/ui components
│       ├── button.tsx
│       ├── input.tsx
│       ├── card.tsx
│       └── scroll-area.tsx
├── hooks/
│   └── useChatStream.ts         # SSE streaming hook
├── lib/
│   ├── utils.ts                 # Utility functions
│   └── types.ts                 # TypeScript type definitions
├── tests/
│   ├── e2e/                     # Playwright E2E tests
│   │   └── chat.spec.ts
│   └── unit/                    # Jest unit tests
│       ├── components/
│       └── hooks/
├── package.json
├── tailwind.config.js
├── next.config.js
└── components.json              # ShadCN/ui config
```

**Structure Decision**: Frontend-only Next.js application with component-based architecture. Uses ShadCN/ui for consistent design system and Framer Motion for animations. Separates concerns with dedicated hooks for streaming logic and organized component structure.

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
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
- Generate tasks from Phase 1 design docs (contracts, data model, quickstart)
- Each contract → contract test task [P]
- Each entity → model creation task [P] 
- Each user story → integration test task
- Implementation tasks to make tests pass

**CLI-First Implementation Strategy**:
- Bootstrap Next.js app with `pnpm create next-app@latest`
- Initialize ShadCN/ui with `pnpm dlx shadcn@latest init`
- Install dependencies with `pnpm add framer-motion`
- All setup steps executable via CLI commands

**UX-First Implementation Strategy**:
- Mobile-first responsive design with Tailwind breakpoints
- ShadCN/ui components for consistent design system
- Framer Motion animations for smooth transitions
- WCAG 2.1 AA accessibility compliance
- Real UX flows established before test generation

**Ordering Strategy**:
- TDD order: Tests before implementation 
- CLI setup → Components → Hooks → Integration → E2E
- Mark [P] for parallel execution (independent files)
- UX implementation after core functionality

**Estimated Output**: 30-35 numbered, ordered tasks in tasks.md covering:
- CLI project setup and ShadCN/ui initialization
- Component development with TypeScript and Tailwind
- SSE streaming hook implementation
- Framer Motion animation integration
- Mobile-first responsive design
- Accessibility implementation
- E2E testing with Playwright

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
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented

---
*Based on Constitution v1.1.0 - See `/memory/constitution.md`* 
