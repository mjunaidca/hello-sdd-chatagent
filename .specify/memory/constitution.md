<!-- Sync Impact Report
Version change: 1.0.0 → 1.1.0
Modified principles:
- I. Code Quality & Testing Standards → I. Code Quality & Testing Standards (NON-NEGOTIABLE)
- II. Async-First Architecture → II. Async-First Architecture
- III. Clean Architecture Separation → III. Clean Architecture Separation
- IV. Security & Reliability → IV. Security & Reliability
- V. Extensibility & Performance → V. Extensibility & Performance
Added sections:
- VI. CLI-First Development (NEW)
- VII. UX-First Design (NEW)
- Development Standards (Technology Stack Requirements, Code Organization)
- Quality Assurance (Testing Requirements, Code Review Standards)
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md (Constitution Check gates updated, version reference updated)
- ✅ .specify/templates/tasks-template.md (CLI setup tasks added, UX testing approach updated)
- ✅ .specify/templates/spec-template.md (UX requirements section added)
- ⚠ .specify/templates/commands/ (directory does not exist yet)
Follow-up TODOs: None - all placeholders resolved
-->

# SDD Chat Agent Constitution

## Core Principles

### I. Code Quality & Testing Standards (NON-NEGOTIABLE)
All code MUST maintain high quality standards with strong typing, comprehensive linting, and test-first development practices.

- **Strong Typing**: All code MUST use type hints (Python typing, TypeScript interfaces) with strict type checking enabled. No `any` types or untyped functions allowed.
- **Linting**: Code MUST pass all configured linters (ruff, mypy, eslint) with zero violations. Automated formatting MUST be enforced.
- **Test-First Development**: Tests MUST be written before implementation begins. Follow TDD principles: Red-Green-Refactor cycle strictly enforced. All tests MUST pass before code is considered complete.
- **Test Coverage**: Minimum 80% code coverage required for all modules. Mock external dependencies in unit tests for reliable offline CI execution.
- **Documentation**: All public APIs and complex logic MUST be documented with clear examples and usage patterns.

### II. Async-First Architecture
All FastAPI endpoints and I/O operations MUST be designed with async/await patterns for optimal performance and scalability.

- **FastAPI Endpoints**: All API endpoints MUST be implemented as async functions using async/await patterns for non-blocking I/O operations.
- **Database Operations**: All database interactions MUST use async drivers (asyncpg, motor) and be properly awaited.
- **External API Calls**: All external service calls MUST use async HTTP clients (httpx) with proper timeout and retry configurations.
- **Background Tasks**: Long-running operations MUST be handled as background tasks or queued jobs, never blocking the main request-response cycle.
- **Connection Pooling**: Async connection pools MUST be configured for database and external service connections to maximize throughput.

### III. Clean Architecture Separation
Clear separation of concerns between UI layer (Chainlit), Agent logic (OpenAI Agents SDK Framework), and API layer MUST be maintained.

- **Layer Isolation**: UI components (Chainlit), Agent logic (OpenAI Agents SDK), and API endpoints MUST be clearly separated with defined interfaces.
- **Dependency Injection**: Use dependency injection patterns to decouple layers and enable easy testing and mocking.
- **Interface Contracts**: Well-defined contracts between layers MUST be established and tested independently.
- **Single Responsibility**: Each module and class MUST have a single, clearly defined responsibility.
- **Data Flow**: Clear data flow patterns MUST be established from UI → Agent → API → external services.

### IV. Security & Reliability
System MUST maintain security best practices and provide resilient operation under various failure conditions.

- **API Key Protection**: API keys and sensitive credentials MUST NEVER be exposed in responses, logs, or error messages. Use environment variables and secure vaults.
- **Streaming Resilience**: WebSocket and streaming connections MUST be stable, resilient to disconnects, and implement retry logic with exponential backoff.
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes and user-friendly error messages without exposing internal details.
- **Input Validation**: All user inputs MUST be validated and sanitized before processing to prevent injection attacks.
- **Authentication**: Secure authentication mechanisms MUST be implemented for protected endpoints and agent capabilities.

### V. Extensibility & Performance
System MUST be designed for easy extension of new endpoints and agent capabilities while maintaining consistent user experience and performance standards.

- **Modular Design**: New endpoints or agent capabilities MUST be added with minimal changes to existing code through plugin or extension patterns.
- **Performance Requirements**: Response times MUST be under 200ms for 95th percentile, with proper caching strategies for frequently accessed data.
- **User Experience Consistency**: All new features MUST maintain consistent UI patterns, error handling, and interaction models.
- **Scalability**: Architecture MUST support horizontal scaling and handle increased load through efficient resource utilization.
- **Monitoring**: Comprehensive logging and metrics MUST be implemented for performance monitoring and debugging.

### VI. CLI-First Development
All projects MUST be initialized and managed through command-line interfaces to ensure consistent, reproducible development environments.

- **Project Initialization**: All new projects MUST be created using CLI tools (`pnpm create next-app@latest`, `pnpm dlx shadcn@latest init`, `uv init --package`).
- **Package Management**: Use **pnpm** package manager for all JavaScript/TypeScript projects (not npm or yarn).
- **Python Projects**: Use **uv** package manager for all Python projects with `uv init --package` for packaged applications.
- **CLI Tools**: Prefer CLI-based tooling over GUI alternatives for consistency and automation.
- **Reproducible Setup**: All setup instructions MUST be executable via CLI commands with no manual steps.

### VII. UX-First Design
All user interfaces MUST prioritize exceptional user experience with mobile-first, accessible, and animated designs.

- **Mobile-First Layouts**: All UI components MUST be designed mobile-first with responsive breakpoints for larger screens.
- **Accessibility**: All interfaces MUST meet WCAG 2.1 AA standards with proper ARIA labels, keyboard navigation, and screen reader support.
- **Animations**: Smooth, purposeful animations MUST be implemented for state transitions and user feedback.
- **Design System**: Use **shadcn/ui** components to minimize boilerplate and ensure consistent design patterns.
- **User Testing**: Real UX flows MUST be established before generating placeholder tests - avoid test generation until actual user interactions are defined.

## Development Standards

### Technology Stack Requirements
- **Python 3.12+** with uv package manager for dependency management
- **JavaScript/TypeScript** with pnpm package manager for frontend projects
- **FastAPI** with async support for API layer
- **Next.js** with shadcn/ui for modern web interfaces
- **Chainlit** for user interface components
- **OpenAI Agents SDK** for agent logic framework
- **PostgreSQL** with async drivers for data persistence
- **Redis** for caching and session management
- **Docker** for containerized deployment

### Code Organization
- **Small, Focused Modules**: Large files (>500 lines) or functions (>50 lines) MUST be split into smaller, composable units
- **Consistent Structure**: Follow established patterns for imports, error handling, and data validation
- **Environment Configuration**: Use .env files with proper validation for all configuration values

## Quality Assurance

### Testing Requirements
- **Unit Tests**: Every function and class MUST have corresponding unit tests with proper mocking
- **Integration Tests**: Critical user flows MUST have integration tests covering end-to-end scenarios
- **Contract Tests**: API contracts MUST be tested independently of implementation details
- **Performance Tests**: Load testing MUST be performed for critical endpoints under expected traffic

### Code Review Standards
- **Mandatory Reviews**: All code changes MUST be reviewed by at least one other developer
- **Testing Requirements**: Code reviews MUST verify test coverage and test quality
- **Constitutional Compliance**: Reviews MUST ensure adherence to all constitutional principles

## Governance

This constitution establishes the foundational principles and standards for the SDD Chat Agent project. These principles guide all technical decisions, architecture choices, and implementation approaches.

### Amendment Process
- **Proposal**: Any team member may propose amendments by creating a detailed change request with rationale and impact analysis
- **Review**: Proposed changes MUST be reviewed by the entire development team for constitutional compliance
- **Approval**: Amendments require unanimous approval from all active maintainers
- **Implementation**: Approved changes MUST include migration guides and backward compatibility considerations
- **Documentation**: All amendments MUST be documented with rationale and impact analysis

### Compliance Verification
- **Automated Checks**: CI/CD pipelines MUST verify constitutional compliance through linting, type checking, and test execution
- **Manual Reviews**: Code reviews MUST explicitly verify adherence to constitutional principles
- **Quality Gates**: No code violating constitutional principles may be merged or deployed
- **Exception Process**: Complexity requiring deviation from principles MUST be justified and documented

### Versioning Policy
- **Semantic Versioning**: Constitution version follows MAJOR.MINOR.PATCH format
- **Major Version**: Breaking changes to core principles or fundamental architectural decisions
- **Minor Version**: Addition of new principles or significant expansions to existing guidance
- **Patch Version**: Clarifications, typo fixes, and non-semantic refinements

### Development Guidance
- **Runtime Reference**: Use `/memory/constitution.md` for ongoing development guidance and decision-making
- **Template Alignment**: All project templates and tooling MUST remain synchronized with constitutional principles
- **Training**: New team members MUST be trained on constitutional principles before contributing

**Version**: 1.1.0 | **Ratified**: 2025-09-26 | **Last Amended**: 2025-01-27