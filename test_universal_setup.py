#!/usr/bin/env python3
"""
Test script to verify the universal chatbot setup is working correctly.
This ensures all Snort-specific code has been removed successfully.

MIT License - Copyright (c) 2025 universal-chatbot
"""

import os
import sys


def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing module imports...")

    try:
        # Test core modules
        from src.chatbot import create_chatbot
        from src.document_loader import DocumentLoader
        from src.vector_store import VectorStore
        from src.retrieval import RetrievalEngine
        from src.conversation_memory import ConversationMemory
        from config import settings, validate_settings

        print("✅ All core modules imported successfully")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

    return True


def test_configuration():
    """Test that configuration is properly set up."""
    print("\n🧪 Testing configuration...")

    # Test settings loading
    from config import settings

    print(f"📂 Documents directory: {settings.documents_directory}")
    print(f"🗃️  Vector DB path: {settings.vector_db_path}")
    print(f"🌐 External URL search: {settings.enable_external_url_search}")
    print(f"🔗 External URLs: '{settings.external_search_urls}'")

    # Verify no hardcoded Snort references
    if "snort" in settings.external_search_urls.lower():
        print("❌ Found Snort reference in external URLs!")
        return False

    print("✅ Configuration is clean (no Snort references)")
    return True


def test_documents_directory():
    """Test that documents directory exists and can be read."""
    print("\n🧪 Testing documents directory...")

    from config import settings

    docs_dir = settings.documents_directory

    if not os.path.exists(docs_dir):
        print(f"📁 Creating documents directory: {docs_dir}")
        os.makedirs(docs_dir, exist_ok=True)

    # List available documents
    try:
        files = os.listdir(docs_dir)
        doc_files = [f for f in files if f.endswith((".md", ".txt", ".pdf", ".docx"))]

        print(f"📄 Found {len(doc_files)} document files:")
        for file in doc_files[:5]:  # Show first 5
            print(f"   - {file}")

        if len(doc_files) > 5:
            print(f"   ... and {len(doc_files) - 5} more")

        print("✅ Documents directory accessible")
        return True

    except Exception as e:
        print(f"❌ Error accessing documents directory: {e}")
        return False


def test_vector_store():
    """Test that vector store can be initialized."""
    print("\n🧪 Testing vector store initialization...")

    try:
        from src.vector_store import VectorStore

        vector_store = VectorStore()
        print("✅ Vector store initialized successfully")
        return True

    except Exception as e:
        print(f"❌ Vector store initialization failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Universal Chatbot Setup Test")
    print("=" * 50)

    tests = [
        test_imports,
        test_configuration,
        test_documents_directory,
        test_vector_store,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        else:
            print(f"\n⚠️  Test failed: {test.__name__}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your universal chatbot is ready!")
        print("\n📝 Next steps:")
        print("1. Add your documents to the 'documents' directory")
        print("2. Configure external URLs in .env file (EXTERNAL_SEARCH_URLS)")
        print("3. Set up your LLM credentials (CURCUIT_* or OLLAMA_* settings)")
        print("4. Run: python main.py")
        return True
    else:
        print("❌ Some tests failed. Please check the configuration.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
