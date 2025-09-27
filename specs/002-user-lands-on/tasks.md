# Tasks: Responsive Chat Interface

**Input**: Design documents from `/specs/002-user-lands-on/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [x] T001 Create Next.js 15 project with TypeScript and Tailwind CSS
- [x] T002 [P] Initialize ShadCN/ui component library
- [x] T003 [P] Install Framer Motion and additional dependencies
- [x] T004 [P] Configure ESLint and TypeScript settings
- [x] T005 [P] Set up project directory structure

## Phase 3.2: Core Components (UX-First)
- [x] T006 Create main chat page layout in `app/chat/page.tsx`
- [x] T007 [P] Implement ChatContainer component with responsive design
- [x] T008 [P] Implement ChatInput component with ShadCN/ui Input and Button
- [x] T009 [P] Implement ChatMessage component with user/assistant variants
- [x] T010 [P] Implement TypingIndicator component with animated dots
- [x] T011 [P] Implement ErrorBanner component for inline error display

## Phase 3.3: Data Models and Types
- [x] T012 [P] Create TypeScript types in `lib/types.ts` for ChatMessage and ChatSession
- [x] T013 [P] Create utility functions in `lib/utils.ts` for message formatting
- [x] T014 [P] Create device detection utilities for responsive behavior

## Phase 3.4: Streaming and State Management
- [x] T015 [P] Implement useChatStream hook for SSE streaming in `hooks/useChatStream.ts`
- [x] T016 [P] Add auto-scroll behavior with pause-on-scroll functionality
- [x] T017 [P] Implement session management and persistence logic
- [x] T018 [P] Add message state management (sending, sent, failed, streaming)

## Phase 3.5: Animations and UX Polish
- [x] T019 [P] Add Framer Motion animations to ChatMessage bubbles
- [x] T020 [P] Implement smooth entry/exit animations for new messages
- [x] T021 [P] Add typing indicator animations with Framer Motion
- [x] T022 [P] Implement error banner slide-down animations
- [x] T023 [P] Add mobile-first responsive design optimizations

## Phase 3.6: Error Handling and Recovery
- [x] T024 [P] Implement automatic retry with exponential backoff
- [x] T025 [P] Add manual retry functionality for failed connections
- [x] T026 [P] Implement connection status indicators
- [x] T027 [P] Add graceful error recovery and user feedback

## Phase 3.7: Accessibility and Polish
- [x] T028 [P] Add ARIA labels and keyboard navigation support
- [x] T029 [P] Implement screen reader compatibility
- [x] T030 [P] Add high contrast mode support
- [x] T031 [P] Optimize for mobile touch interactions

## Phase 3.8: Integration and Testing
- [x] T032 [P] Create contract tests for chat API endpoints
- [x] T033 [P] Implement integration tests for chat flow
- [x] T034 [P] Add unit tests for components and hooks
- [x] T035 [P] Create E2E test for complete chat user journey

## Dependencies
- Setup (T001-T005) before all other tasks
- Core components (T006-T011) can run in parallel after setup
- Data models (T012-T014) can run in parallel with components
- Streaming (T015-T018) depends on data models and components
- Animations (T019-T023) depend on core components
- Error handling (T024-T027) depends on streaming implementation
- Accessibility (T028-T031) can run in parallel with animations
- Testing (T032-T035) depends on all implementation being complete

## Parallel Example
```
# Launch T007-T011 together (core components):
Task: "Implement ChatContainer component with responsive design"
Task: "Implement ChatInput component with ShadCN/ui Input and Button"
Task: "Implement ChatMessage component with user/assistant variants"
Task: "Implement TypingIndicator component with animated dots"
Task: "Implement ErrorBanner component for inline error display"
```

## Notes
- [P] tasks = different files, no dependencies
- UX-first approach: Components before tests, real functionality before test generation
- All tasks include specific file paths for immediate execution
- Mobile-first responsive design throughout
- ShadCN/ui components for consistent design system
- Framer Motion for smooth animations
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Components → Models → Streaming → Animations → Error Handling → Accessibility → Testing
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All components have implementation tasks
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
