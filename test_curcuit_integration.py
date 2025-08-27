#!/usr/bin/env python3
"""
Test script for CURCUIT API integration.
Tests the new LLM fallback system with CURCUIT as primary and Ollama as backup.

Usage:
    python test_curcuit_integration.py
"""

import os
import sys
import logging

# Add src to path for imports
sys.path.append("src")

from config import get_settings, validate_settings
from src.curcuit_api import create_curcuit_client
from src.chatbot import RAGChatbot

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_curcuit_api_client():
    """Test CURCUIT API client initialization and connection."""
    print("\n🧪 Testing CURCUIT API Client...")

    settings = get_settings()

    # Check if CURCUIT credentials are configured
    if not settings.curcuit_client_id or not settings.curcuit_client_secret:
        print("❌ CURCUIT API credentials not configured")
        print(
            "   Please set CURCUIT_CLIENT_ID and CURCUIT_CLIENT_SECRET in your .env file"
        )
        return False

    try:
        # Create CURCUIT client
        client = create_curcuit_client()
        print(f"✅ CURCUIT client created successfully")

        # Test connection
        connection_ok = client.test_connection()
        if connection_ok:
            print("✅ CURCUIT API connection test passed")
            return True
        else:
            print("❌ CURCUIT API connection test failed")
            return False

    except Exception as e:
        print(f"❌ Error testing CURCUIT API: {str(e)}")
        return False


def test_chatbot_initialization():
    """Test chatbot initialization with new LLM fallback system."""
    print("\n🤖 Testing Chatbot Initialization...")

    try:
        # Initialize chatbot
        chatbot = RAGChatbot()
        print("✅ Chatbot initialized successfully")

        # Get statistics
        stats = chatbot.get_stats()
        print(f"📊 Model Type: {stats['model_type']}")
        print(f"📊 Current Model: {stats['model']}")

        # Print LLM status
        llm_status = stats.get("llm_status", {})
        print(f"📊 CURCUIT Available: {llm_status.get('curcuit_available', False)}")
        print(f"📊 Backup Available: {llm_status.get('backup_available', False)}")
        print(f"📊 Primary Model: {llm_status.get('primary_model', 'none')}")
        print(f"📊 Backup Model: {llm_status.get('backup_model', 'none')}")

        return chatbot

    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        return None


def test_chatbot_response():
    """Test chatbot response generation with the new system."""
    print("\n💬 Testing Chatbot Response Generation...")

    chatbot = test_chatbot_initialization()
    if not chatbot:
        return False

    try:
        # Simple test question
        test_question = "Hello, how are you?"
        print(f"❓ Test Question: {test_question}")

        # Generate response
        response = chatbot.chat(test_question)

        print(f"🤖 Response: {response.answer[:200]}...")
        print(f"📊 Confidence: {response.confidence:.2f}")
        print(f"🎯 Model Used: {response.model_used}")
        print(f"📄 Sources: {len(response.sources)}")

        return True

    except Exception as e:
        print(f"❌ Error generating response: {str(e)}")
        return False


def main():
    """Main test function."""
    print("🚀 Starting CURCUIT Integration Tests")
    print("=" * 50)

    # Check settings validation
    print("\n⚙️  Validating Settings...")
    if not validate_settings():
        print("❌ Settings validation failed")
        return

    # Test CURCUIT API client
    curcuit_ok = test_curcuit_api_client()

    # Test chatbot initialization
    chatbot_ok = test_chatbot_initialization()

    # Test response generation
    if chatbot_ok:
        response_ok = test_chatbot_response()
    else:
        response_ok = False

    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   CURCUIT API: {'✅' if curcuit_ok else '❌'}")
    print(f"   Chatbot Init: {'✅' if chatbot_ok else '❌'}")
    print(f"   Response Gen: {'✅' if response_ok else '❌'}")

    if curcuit_ok and chatbot_ok and response_ok:
        print("\n🎉 All tests passed! CURCUIT integration is working.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")

    print("\n💡 Tips:")
    print(
        "   - Make sure your .env file has CURCUIT_CLIENT_ID, CURCUIT_CLIENT_SECRET, and CURCUIT_APP_KEY"
    )
    print("   - Ensure Ollama is running for backup LLM: ollama serve")
    print("   - Check that your CURCUIT credentials are valid and not expired")


if __name__ == "__main__":
    main()
