# Responsive Chat Interface

A modern, responsive chat interface built with Next.js 15, Tailwind CSS, ShadCN/ui, and Framer Motion. Features real-time streaming, mobile-first design, and comprehensive accessibility support.

## Features

- 🎨 **Modern UI**: Built with ShadCN/ui components and Tailwind CSS
- 📱 **Mobile-First**: Responsive design that works on all devices
- ⚡ **Real-Time Streaming**: Server-Sent Events (SSE) for live message streaming
- 🎭 **Smooth Animations**: Framer Motion animations for enhanced UX
- ♿ **Accessible**: WCAG 2.1 AA compliant with screen reader support
- 🔄 **Auto-Scroll**: Smart scrolling with pause-on-user-scroll behavior
- 🛡️ **Error Handling**: Automatic retry with exponential backoff
- 🧪 **Well-Tested**: Comprehensive test suite with Jest and Playwright

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Styling**: Tailwind CSS
- **Components**: ShadCN/ui
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Testing**: Jest, React Testing Library, Playwright
- **TypeScript**: Full type safety

## Getting Started

### Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd chat-ui
   ```

2. **Install dependencies**:
   ```bash
   pnpm install
   ```

3. **Start the development server**:
   ```bash
   pnpm dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Backend Integration

This frontend is designed to work with the ChatWait backend API. Make sure the backend is running on `http://localhost:8000` for full functionality.

## Project Structure

```
chat-ui/
├── app/                    # Next.js App Router
│   ├── chat/              # Chat page
│   ├── globals.css        # Global styles
│   └── layout.tsx         # Root layout
├── components/
│   ├── chat/              # Chat-specific components
│   │   ├── ChatContainer.tsx
│   │   ├── ChatInput.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── TypingIndicator.tsx
│   │   └── ErrorBanner.tsx
│   └── ui/                # ShadCN/ui components
├── hooks/
│   └── useChatStream.ts   # SSE streaming hook
├── lib/
│   ├── types.ts           # TypeScript types
│   ├── utils.ts           # Utility functions
│   ├── device.ts          # Device detection
│   └── session.ts         # Session management
├── tests/
│   ├── contract/          # API contract tests
│   ├── integration/       # Integration tests
│   ├── unit/              # Unit tests
│   └── e2e/               # E2E tests
└── ...
```

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint
- `pnpm test` - Run unit tests
- `pnpm test:watch` - Run tests in watch mode
- `pnpm test:coverage` - Run tests with coverage
- `pnpm test:e2e` - Run E2E tests
- `pnpm test:e2e:ui` - Run E2E tests with UI

## Key Components

### ChatContainer
Main chat interface container that manages state and coordinates all chat components.

### ChatInput
Message input field with send button, keyboard shortcuts, and validation.

### ChatMessage
Message bubble component with user/assistant variants and status indicators.

### TypingIndicator
Animated typing indicator that shows when the assistant is responding.

### ErrorBanner
Inline error display with retry functionality and user-friendly messages.

### useChatStream Hook
Custom hook that handles SSE streaming, reconnection, and error recovery.

## API Integration

The interface integrates with the ChatWait backend API:

- `GET /api/v1/chat/streaming` - Stream assistant response with Server-Sent Events
  - Parameters: `message` (required), `context_id` (optional), `last_token_index` (optional)
  - Returns: SSE stream with incremental tokens

## Accessibility Features

- **ARIA Labels**: Comprehensive labeling for screen readers
- **Keyboard Navigation**: Full keyboard support
- **High Contrast**: Support for high contrast mode
- **Reduced Motion**: Respects user motion preferences
- **Touch-Friendly**: Optimized for mobile touch interactions

## Testing

The project includes comprehensive testing:

- **Unit Tests**: Component and hook testing with Jest
- **Integration Tests**: Full chat flow testing
- **Contract Tests**: API contract validation
- **E2E Tests**: Complete user journey testing with Playwright

## Performance

- **Bundle Optimization**: Tree shaking and code splitting
- **Image Optimization**: Next.js Image component
- **CSS Purging**: Tailwind CSS purging
- **Lazy Loading**: Dynamic imports for heavy components

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

ISC License - see LICENSE file for details.
