"""ChatWait Frontend - Chainlit Application.

This is the main Chainlit application that provides a web-based chat interface
for the ChatWait service with real-time streaming responses.
"""

import logging
import os

import chainlit as cl
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
DEFAULT_CONTEXT_ID = "default"


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Set up the user session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("context_id", DEFAULT_CONTEXT_ID)

    # Test backend connectivity
    try:
        logger.info("Testing backend connectivity...")
        response = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Backend is reachable and healthy")
        else:
            logger.warning(f"⚠️ Backend returned status {response.status_code}")
    except Exception as e:
        logger.error(f"❌ Cannot reach backend at {BACKEND_URL}: {e}")

    await cl.Message(
        content="🤖 **Welcome to ChatWait!**\n\n"
        + "🎉 **Real-time AI Streaming Chat**\n\n"
        + "✨ See responses as they're generated\n"
        + "⚡ Token-by-token streaming\n"
        + "🌐 Powered by Gemini 2.5 Flash\n\n"
        + "Start chatting to experience the magic! 🚀",
        author="ChatWait",
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    user_message = message.content.strip()

    if not user_message:
        await cl.Message(
            content="Please enter a message to chat with me!", author="ChatWait"
        ).send()
        return

    try:
        logger.info(f"Processing message: {user_message[:50]}...")

        # Test synchronous endpoint first
        sync_response = requests.post(
            f"{BACKEND_URL}/api/v1/chat/wait",
            json={"message": user_message, "context_id": DEFAULT_CONTEXT_ID},
            timeout=30,
        )

        if sync_response.status_code == 200:
            sync_data = sync_response.json()
            response_message = sync_data.get("message", "No response")
            processing_time = sync_data.get("processing_time_ms", 0)
            token_count = sync_data.get("token_count", 0)

            logger.info(
                f"✅ Synchronous response received: {response_message[:100]}..."
            )
            logger.info(f"📊 Stats: {token_count} tokens in {processing_time:.2f}ms")

            # Send the response as a new message
            await cl.Message(content=response_message, author="ChatWait").send()

            # Add to chat history
            history = cl.user_session.get("chat_history") or []
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response_message})
            cl.user_session.set("chat_history", history)

            logger.info("✅ Message processed successfully via sync endpoint")

        else:
            logger.error(
                f"❌ Synchronous endpoint failed: {sync_response.status_code} - {sync_response.text}"
            )
            await cl.Message(
                content=f"❌ **Error:** Backend returned {sync_response.status_code}",
                author="System",
            ).send()

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await cl.Message(content=f"❌ **Error:** {str(e)}", author="System").send()
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    # This allows the file to be run directly for testing
    print("🤖 ChatWait Frontend - Real-time AI Streaming Chat")
    print(f"📡 Backend URL: {BACKEND_URL}")
    print("🚀 Powered by: Gemini 2.5 Flash via OpenAI Agents SDK")
    print("💡 Features: Real-time streaming, token-by-token generation")
    print("🎯 Usage: Run 'chainlit run app.py' to start the frontend server")
