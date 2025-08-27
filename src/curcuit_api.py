"""
CURCUIT API client module.
Handles Cisco CURCUIT API authentication and chat completions.

MIT License - Copyright (c) 2025 talos-chatbot
"""

import logging
import base64
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
from langchain.schema import BaseMessage, HumanMessage, SystemMessage, AIMessage

from config import get_settings

# Set up logging
logger = logging.getLogger(__name__)


class CurcuitTokenManager:
    """
    Manages CURCUIT API OAuth2 token authentication and refresh.
    Tokens expire every hour and need to be refreshed automatically.
    """

    def __init__(self, client_id: str, client_secret: str, token_url: str):
        """
        Initialize token manager with OAuth2 credentials.

        Args:
            client_id: Cisco OAuth2 client ID
            client_secret: Cisco OAuth2 client secret
            token_url: OAuth2 token endpoint URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url

        # Token storage
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

        logger.info("Initialized CURCUIT token manager")

    def _refresh_token(self) -> bool:
        """
        Refresh the access token using client credentials.

        Returns:
            True if token refresh successful, False otherwise
        """
        try:
            # Encode client credentials
            credentials = f"{self.client_id}:{self.client_secret}"
            encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode(
                "utf-8"
            )

            # Prepare request
            headers = {
                "Accept": "*/*",
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encoded_credentials}",
            }

            payload = "grant_type=client_credentials"

            # Request new token
            response = requests.post(
                self.token_url, headers=headers, data=payload, timeout=10
            )

            if response.status_code == 200:
                token_data = response.json()
                self._access_token = token_data.get("access_token")

                # Tokens expire in 1 hour, refresh 5 minutes early to be safe
                self._token_expiry = datetime.now() + timedelta(minutes=55)

                logger.info("✅ CURCUIT access token refreshed successfully")
                return True
            else:
                logger.error(
                    f"❌ Token refresh failed: {response.status_code} - {response.text}"
                )
                return False

        except Exception as e:
            logger.error(f"❌ Error refreshing CURCUIT token: {str(e)}")
            return False

    def get_valid_token(self) -> Optional[str]:
        """
        Get a valid access token, refreshing if necessary.

        Returns:
            Valid access token or None if refresh fails
        """
        # Check if we need to refresh the token
        if (
            self._access_token is None
            or self._token_expiry is None
            or datetime.now() >= self._token_expiry
        ):
            logger.info("Token expired or missing, refreshing...")
            if not self._refresh_token():
                return None

        return self._access_token


class CurcuitAPIClient:
    """
    CURCUIT API client for chat completions.
    Handles token management and API requests with automatic fallback.
    """

    def __init__(self):
        """Initialize CURCUIT API client with settings from config."""
        self.settings = get_settings()

        # Initialize token manager
        self.token_manager = CurcuitTokenManager(
            client_id=self.settings.curcuit_client_id,
            client_secret=self.settings.curcuit_client_secret,
            token_url=self.settings.curcuit_token_url,
        )

        # API configuration
        self.base_url = self.settings.curcuit_api_endpoint
        self.model = self.settings.curcuit_model
        self.app_key = self.settings.curcuit_app_key

        logger.info(f"Initialized CURCUIT API client for model: {self.model}")

    def _format_messages(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        """
        Convert LangChain messages to CURCUIT API format.

        Args:
            messages: List of LangChain BaseMessage objects

        Returns:
            List of message dictionaries for API
        """
        formatted_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, SystemMessage):
                role = "system"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                role = "user"  # Default fallback

            formatted_messages.append({"role": role, "content": message.content})

        return formatted_messages

    def chat_completion(self, messages: List[BaseMessage], **kwargs) -> Optional[str]:
        """
        Send chat completion request to CURCUIT API.

        Args:
            messages: List of conversation messages
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Generated response text or None if request fails
        """
        try:
            # Get valid access token
            access_token = self.token_manager.get_valid_token()
            if not access_token:
                logger.error("❌ Could not obtain valid CURCUIT access token")
                return None

            # Format messages for API
            formatted_messages = self._format_messages(messages)

            # Prepare API request
            url = f"{self.base_url}/openai/deployments/{self.model}/chat/completions"

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "api-key": access_token,
            }

            # Prepare request payload
            payload = {
                "messages": formatted_messages,
                "user": f'{{"appkey": "{self.app_key}"}}',
                "stop": ["<|im_end|>"],
            }

            # Add optional parameters
            if "temperature" in kwargs:
                payload["temperature"] = kwargs["temperature"]
            if "max_tokens" in kwargs:
                payload["max_tokens"] = kwargs["max_tokens"]

            # Send request
            response = requests.post(url, json=payload, headers=headers, timeout=30)

            if response.status_code == 200:
                response_data = response.json()

                # Extract response content
                choices = response_data.get("choices", [])
                if choices and len(choices) > 0:
                    message_content = choices[0].get("message", {}).get("content", "")
                    logger.info("✅ CURCUIT API response received successfully")
                    return message_content
                else:
                    logger.error("❌ No response content in CURCUIT API response")
                    return None

            else:
                # Enhanced error handling with specific rate limit detection
                if response.status_code == 429:
                    logger.error(
                        f"🚨 CURCUIT API rate limit exceeded: {response.status_code}"
                    )
                    logger.error(f"   Rate limit headers: {dict(response.headers)}")
                    logger.error(
                        "   💡 Try reducing request frequency or upgrading your CURCUIT tier"
                    )
                elif response.status_code == 401:
                    logger.error(
                        f"🔑 CURCUIT API authentication failed: {response.status_code}"
                    )
                    logger.error(
                        "   💡 Check your CLIENT_ID and CLIENT_SECRET credentials"
                    )
                elif response.status_code == 403:
                    logger.error(
                        f"🚫 CURCUIT API access forbidden: {response.status_code}"
                    )
                    logger.error("   💡 Check your APP_KEY and API permissions")
                else:
                    logger.error(
                        f"❌ CURCUIT API request failed: {response.status_code} - {response.text}"
                    )
                return None

        except Exception as e:
            logger.error(f"❌ Error in CURCUIT API request: {str(e)}")
            return None

    def test_connection(self) -> bool:
        """
        Test CURCUIT API connectivity and authentication.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Test token generation
            access_token = self.token_manager.get_valid_token()
            if not access_token:
                logger.error("❌ CURCUIT API token test failed")
                return False

            # Test simple API call
            test_messages = [
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content="Say 'Hello' to test the connection."),
            ]

            response = self.chat_completion(test_messages, max_tokens=10)

            if response:
                logger.info("✅ CURCUIT API connection test successful")
                return True
            else:
                logger.error("❌ CURCUIT API connection test failed")
                return False

        except Exception as e:
            logger.error(f"❌ CURCUIT API connection test error: {str(e)}")
            return False


def create_curcuit_client() -> CurcuitAPIClient:
    """
    Factory function to create CURCUIT API client.

    Returns:
        CurcuitAPIClient instance
    """
    return CurcuitAPIClient()
