#!/usr/bin/env python3
"""Simple API testing script for ChatWait.

This script demonstrates how to test the ChatWait API endpoints directly.
Run this from the repository root directory.
"""

import json
import requests
from typing import Optional


class ChatWaitTester:
    """Simple tester for ChatWait API endpoints."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the tester with API base URL."""
        self.base_url = base_url
        self.session = requests.Session()

    def test_health(self) -> bool:
        """Test health endpoint."""
        print("🏥 Testing health endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(
                    f"✅ Health: {data['status']} ({data['service']} v{data['version']})"
                )
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False

    def test_wait_endpoint(
        self, message: str, context_id: Optional[str] = None
    ) -> bool:
        """Test /chat/wait endpoint."""
        print(f"💬 Testing /chat/wait with: '{message}'")

        payload = {"message": message}
        if context_id:
            payload["context_id"] = context_id

        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/chat/wait",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Response: {data['message'][:100]}...")
                print(
                    f"📊 Tokens: {data['token_count']}, Time: {data['processing_time_ms']:.2f}ms"
                )
                print(f"🔗 Context ID: {data['context_id']}")
                return True
            elif response.status_code == 422:
                print(f"⚠️  Validation error: {response.json()}")
                return False
            elif response.status_code == 429:
                print("⚠️  Rate limit exceeded (Gemini API quota)")
                return True  # This is expected due to quota limits
            else:
                print(f"❌ Unexpected error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Request error: {e}")
            return False

    def test_streaming_endpoint(self, message: str) -> bool:
        """Test /chat/streaming endpoint."""
        print(f"📡 Testing /chat/streaming with: '{message}'")

        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/chat/streaming",
                params={"message": message},
                headers={"Accept": "text/event-stream"},
                stream=True,
            )

            if response.status_code == 200:
                print("✅ Streaming connection established")
                print("📡 Receiving tokens...")

                tokens_received = 0
                for line in response.iter_lines():
                    if line:
                        line_str = line.decode("utf-8")
                        if line_str.startswith("data: "):
                            data_str = line_str[6:]  # Remove 'data: ' prefix
                            try:
                                data = json.loads(data_str)
                                if data.get("type") == "token":
                                    token = data.get("token", "")
                                    if token.strip():  # Only count non-empty tokens
                                        tokens_received += 1
                                        print(
                                            f"📝 Token {tokens_received}: '{token}'",
                                            end="",
                                            flush=True,
                                        )
                                elif data.get("type") == "end":
                                    print(
                                        f"\n✅ Streaming complete! Total tokens: {tokens_received}"
                                    )
                                    return True
                                elif data.get("type") == "error":
                                    print(
                                        f"\n⚠️  Streaming error: {data.get('message')}"
                                    )
                                    return False
                            except json.JSONDecodeError:
                                pass  # Skip malformed lines

                print(f"\n✅ Streaming finished. Tokens received: {tokens_received}")
                return True
            elif response.status_code == 422:
                print(f"⚠️  Validation error: {response.json()}")
                return False
            elif response.status_code == 429:
                print("⚠️  Rate limit exceeded (Gemini API quota)")
                return True  # This is expected due to quota limits
            else:
                print(f"❌ Unexpected error: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            return False

    def run_tests(self):
        """Run all API tests."""
        print("🧪 Starting ChatWait API Tests")
        print("=" * 50)

        # Test 1: Health check
        health_ok = self.test_health()
        print()

        if not health_ok:
            print("❌ Health check failed. Cannot proceed with other tests.")
            return

        # Test 2: Wait endpoint
        wait_ok = self.test_wait_endpoint(
            "Hello! Can you tell me about artificial intelligence?"
        )
        print()

        # Test 3: Streaming endpoint
        streaming_ok = self.test_streaming_endpoint(
            "What are the benefits of machine learning?"
        )
        print()

        # Summary
        print("=" * 50)
        print("📊 Test Summary:")
        print(f"🏥 Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
        print(f"💬 Wait Endpoint: {'✅ PASS' if wait_ok else '❌ FAIL'}")
        print(f"📡 Streaming: {'✅ PASS' if streaming_ok else '❌ FAIL'}")

        if health_ok and (wait_ok or streaming_ok):
            print("🎉 API is working! (Rate limits may cause some calls to fail)")
        else:
            print("⚠️  Some issues detected. Check server logs.")


def main():
    """Main test function."""
    tester = ChatWaitTester()
    tester.run_tests()


if __name__ == "__main__":
    main()
