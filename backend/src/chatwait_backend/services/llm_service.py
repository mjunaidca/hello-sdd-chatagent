"""LLM service configuration using OpenAI Agents SDK with Gemini.

This module sets up the AsyncOpenAI client with Gemini's OpenAI-compatible endpoint
and configures the OpenAIChatCompletionsModel for agent interactions.
"""

import logging

from agents import AsyncOpenAI, OpenAIChatCompletionsModel, SQLiteSession

from chatwait_backend.config import settings

# Configure logger
logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM configuration and client management."""

    def __init__(self):
        """Initialize LLM service with Gemini configuration."""
        self.external_client: AsyncOpenAI | None = None
        self.llm_model: OpenAIChatCompletionsModel | None = None
        self._sessions: dict[str, SQLiteSession] = {}  # Cache for sessions
        self._initialize_client()

    def _initialize_client(self) -> None:
        """Initialize the AsyncOpenAI client with Gemini endpoint.

        This follows the pattern provided by the user for Gemini integration:
        - Uses AsyncOpenAI client with Gemini's OpenAI-compatible endpoint
        - Configures the client with the API key from environment
        - Sets up the OpenAIChatCompletionsModel with gemini-2.5-flash
        """
        try:
            # Initialize AsyncOpenAI client with Gemini endpoint
            self.external_client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url=settings.gemini_base_url,
            )

            logger.info(
                f"Initialized AsyncOpenAI client with base URL: {settings.gemini_base_url}"
            )

            # Configure OpenAIChatCompletionsModel with Gemini
            self.llm_model = OpenAIChatCompletionsModel(
                model=settings.gemini_model, openai_client=self.external_client
            )

            logger.info(
                f"Configured OpenAIChatCompletionsModel with model: {settings.gemini_model}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise

    def get_client(self) -> AsyncOpenAI:
        """Get the configured AsyncOpenAI client.

        Returns:
            AsyncOpenAI: The configured client

        Raises:
            RuntimeError: If client is not initialized
        """
        if self.external_client is None:
            raise RuntimeError(
                "LLM client not initialized. Call _initialize_client() first."
            )
        return self.external_client

    def get_model(self) -> OpenAIChatCompletionsModel:
        """Get the configured OpenAIChatCompletionsModel.

        Returns:
            OpenAIChatCompletionsModel: The configured model

        Raises:
            RuntimeError: If model is not initialized
        """
        if self.llm_model is None:
            raise RuntimeError(
                "LLM model not initialized. Call _initialize_client() first."
            )
        return self.llm_model

    def create_session(self, session_id: str) -> SQLiteSession:
        """Create a new SQLiteSession for conversation persistence.

        Args:
            session_id: Unique identifier for the conversation session

        Returns:
            SQLiteSession: Configured session for conversation memory
        """
        try:
            # Create session with session_id as database name
            session = SQLiteSession(session_id)
            logger.info(f"Created SQLiteSession for session_id: {session_id}")
            return session
        except Exception as e:
            logger.error(f"Failed to create SQLiteSession for {session_id}: {e}")
            raise

    def get_or_create_session(
        self, session_id: str | None = None
    ) -> SQLiteSession | None:
        """Get existing session or create new one if session_id provided.

        Args:
            session_id: Optional session identifier. If None, returns None (stateless mode)

        Returns:
            Optional[SQLiteSession]: Session if session_id provided, None for stateless mode
        """
        if session_id is None:
            logger.debug("No session_id provided, operating in stateless mode")
            return None

        # Check if session already exists in cache
        if session_id in self._sessions:
            logger.debug(f"Reusing existing SQLiteSession for: {session_id}")
            return self._sessions[session_id]

        # Create new session and cache it
        session = self.create_session(session_id)
        self._sessions[session_id] = session
        logger.info(f"Cached new SQLiteSession for: {session_id}")
        return session

    async def health_check(self) -> dict:
        """Check LLM service health.

        Returns:
            dict: Health status information
        """
        try:
            if self.external_client is None or self.llm_model is None:
                return {"status": "error", "message": "LLM service not initialized"}

            # Basic connectivity check
            return {
                "status": "healthy",
                "model": settings.gemini_model,
                "base_url": settings.gemini_base_url,
                "client_configured": True,
                "model_configured": True,
            }

        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            return {"status": "error", "message": f"Health check failed: {str(e)}"}


# Global service instance
llm_service = LLMService()
