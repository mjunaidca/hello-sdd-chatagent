"""Chat agent service using OpenAI Agents SDK.

This module implements the ChatAgent using the OpenAI Agents SDK with
proper instructions and error handling for conversational AI responses.
"""

import asyncio
import logging
from typing import Any

from agents import Agent, Runner
from agents.result import RunResult

from chatwait_backend.models.chat_models import ChatMessage, MessageRole
from chatwait_backend.services.llm_service import llm_service

# Configure logger
logger = logging.getLogger(__name__)


# TODO: Add function tools when Pydantic schema issues are resolved
# @function_tool
def get_conversation_context(session_id: str) -> str:
    """Get conversation context for a session.

    This is a placeholder function that can be extended
    with actual context retrieval logic.

    Args:
        session_id: The session identifier

    Returns:
        str: Context information
    """
    return f"Context for session {session_id}"


# TODO: Add function tools when Pydantic schema issues are resolved
# @function_tool
def save_conversation_context(session_id: str, messages: list[dict[str, Any]]) -> str:
    """Save conversation context for a session.

    This is a placeholder function that can be extended
    with actual context persistence logic.

    Args:
        session_id: The session identifier
        messages: List of conversation messages

    Returns:
        str: Save confirmation
    """
    return f"Saved {len(messages)} messages for session {session_id}"


class ChatAgentService:
    """Service for managing chat agents and conversation execution."""

    def __init__(self):
        """Initialize ChatAgent service."""
        self.agent = self._create_chat_agent()
        logger.info("ChatAgent service initialized")

    def _create_chat_agent(self) -> Agent:
        """Create the main ChatAgent with proper instructions.

        Returns:
            Agent: Configured chat agent
        """
        try:
            # Get the configured model from LLM service
            llm_model = llm_service.get_model()

            # Create agent with conversational instructions
            agent = Agent(
                name="ChatWait Assistant",
                instructions="""
                You are ChatWait, a helpful and conversational AI assistant.

                Your role is to provide helpful, accurate, and engaging responses to user questions and requests.
                You should be friendly, informative, and maintain context across conversation turns.

                Guidelines:
                - Be helpful and provide accurate information
                - Keep responses clear and well-structured
                - Acknowledge context from previous messages when relevant
                - Be concise but comprehensive
                - If you're unsure about something, admit it rather than guessing
                - Maintain a friendly and professional tone

                Note: Function tools are currently disabled for compatibility. Context management will be handled by the application layer.
                """,
                model=llm_model,
                # TODO: Add tools when Pydantic schema issues are resolved
                # tools=[get_conversation_context, save_conversation_context]
            )

            logger.info("ChatAgent created successfully")
            return agent

        except Exception as e:
            logger.error(f"Failed to create ChatAgent: {e}")
            raise

    async def run_sync(
        self, message: str, context_id: str | None = None
    ) -> dict[str, Any]:
        """Run the chat agent synchronously for /chat/wait endpoint.

        Args:
            message: User input message
            context_id: Optional conversation context identifier

        Returns:
            Dict containing response data with message, context_id, token_count, etc.
        """
        try:
            start_time = asyncio.get_event_loop().time()

            # Get or create session for conversation persistence
            session = llm_service.get_or_create_session(context_id)

            # Run the agent synchronously with session
            result: RunResult = await Runner.run(
                starting_agent=self.agent, input=message, session=session
            )

            # Calculate processing time
            processing_time_ms = (asyncio.get_event_loop().time() - start_time) * 1000

            # Convert agent response to our format
            response = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=result.final_output,
                token_count=len(result.final_output.split()),  # Simple token estimation
            )

            # Log session usage
            if session:
                logger.info(
                    f"Used SQLiteSession for conversation persistence: {context_id}"
                )
            else:
                logger.info("Operated in stateless mode (no session)")

            logger.info(f"Agent execution completed in {processing_time_ms:.2f}ms")

            return {
                "message": response.content,
                "context_id": context_id or "default",
                "token_count": response.token_count,
                "processing_time_ms": processing_time_ms,
                "agent_output": result.final_output,
            }

        except Exception as e:
            logger.error(f"Error running chat agent: {e}")
            raise

    async def run_streaming(
        self, message: str, context_id: str | None = None, last_token_index: int = 0
    ):
        """Run the chat agent with streaming for /chat/streaming endpoint.

        Args:
            message: User input message
            context_id: Optional conversation context identifier
            last_token_index: Last token index for reconnection

        Yields:
            Dict containing streaming events (tokens, completion, errors)
        """
        try:
            # Get or create session for conversation persistence
            session = llm_service.get_or_create_session(context_id)

            # Run agent with streaming and session
            stream_result = Runner.run_streamed(
                starting_agent=self.agent, input=message, session=session
            )

            current_token_index = last_token_index

            async for event in stream_result.stream_events():
                try:
                    if hasattr(event, "type") and event.type == "raw_response_event":
                        if hasattr(event, "data") and hasattr(event.data, "delta"):
                            # This is a token delta event
                            token = event.data.delta
                            if token.strip():  # Only yield non-empty tokens
                                yield {
                                    "type": "token",
                                    "token": token,
                                    "token_index": current_token_index,
                                    "context_id": context_id or "default",
                                }
                                current_token_index += 1

                except Exception as event_error:
                    logger.warning(f"Error processing streaming event: {event_error}")
                    continue

            # Send completion event
            yield {
                "type": "end",
                "context_id": context_id or "default",
                "final_output": stream_result.final_output,
            }

            # Log session usage
            if session:
                logger.info(
                    f"Used SQLiteSession for streaming conversation persistence: {context_id}"
                )
            else:
                logger.info("Operated in stateless streaming mode (no session)")

        except Exception as e:
            logger.error(f"Error in streaming execution: {e}")
            yield {
                "type": "error",
                "context_id": context_id,
                "error_code": "STREAMING_ERROR",
                "message": str(e),
            }

    async def health_check(self) -> dict:
        """Check ChatAgent service health.

        Returns:
            dict: Health status information
        """
        try:
            return {
                "status": "healthy",
                "agent_configured": self.agent is not None,
                "llm_service_available": llm_service.get_model() is not None,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"ChatAgent health check failed: {str(e)}",
            }


# Global service instance
chat_agent_service = ChatAgentService()
