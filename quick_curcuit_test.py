#!/usr/bin/env python3
"""
Quick CURCUIT API test without dependencies.
Tests CURCUIT API directly using just requests.
"""

import os
import base64
import requests
import json

# Read credentials from .env
def load_env():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found")
        return None
    return env_vars

def test_curcuit_direct():
    print("🧪 Testing CURCUIT API directly...")
    
    # Load environment
    env = load_env()
    if not env:
        return False
    
    client_id = env.get('CURCUIT_CLIENT_ID')
    client_secret = env.get('CURCUIT_CLIENT_SECRET')
    app_key = env.get('CURCUIT_APP_KEY')
    model = env.get('CURCUIT_MODEL', 'gpt-4o-mini')
    
    if not all([client_id, client_secret, app_key]):
        print("❌ Missing CURCUIT credentials")
        return False
    
    print(f"✅ Credentials loaded")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   App Key: {app_key[:20]}...")
    print(f"   Model: {model}")
    
    # Step 1: Get access token
    print("\n🔑 Getting access token...")
    try:
        credentials = f"{client_id}:{client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        token_headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {encoded_credentials}"
        }
        
        token_response = requests.post(
            "https://id.cisco.com/oauth2/default/v1/token",
            headers=token_headers,
            data="grant_type=client_credentials",
            timeout=10
        )
        
        if token_response.status_code == 200:
            token_data = token_response.json()
            access_token = token_data.get('access_token')
            print(f"✅ Token obtained: {access_token[:20]}...")
        else:
            print(f"❌ Token request failed: {token_response.status_code}")
            print(f"Response: {token_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Token request error: {str(e)}")
        return False
    
    # Step 2: Test API call
    print("\n💬 Testing chat completion...")
    try:
        api_url = f"https://chat-ai.cisco.com/openai/deployments/{model}/chat/completions"
        
        api_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "api-key": access_token
        }
        
        payload = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'CURCUIT API is working' if you can respond."}
            ],
            "user": f'{{"appkey": "{app_key}"}}',
            "stop": ["<|im_end|>"]
        }
        
        api_response = requests.post(
            api_url,
            json=payload,
            headers=api_headers,
            timeout=30
        )
        
        if api_response.status_code == 200:
            response_data = api_response.json()
            choices = response_data.get("choices", [])
            if choices:
                message = choices[0].get("message", {}).get("content", "")
                print(f"✅ CURCUIT API Response: {message}")
                return True
            else:
                print("❌ No response content in API response")
                print(f"Full response: {response_data}")
        else:
            print(f"❌ API request failed: {api_response.status_code}")
            print(f"Response: {api_response.text}")
            
    except Exception as e:
        print(f"❌ API request error: {str(e)}")
        return False
    
    return False

if __name__ == "__main__":
    print("🚀 CURCUIT Direct API Test")
    print("=" * 40)
    
    success = test_curcuit_direct()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 CURCUIT API is working properly!")
        print("💡 Check your application logs for specific errors.")
    else:
        print("❌ CURCUIT API test failed.")
        print("💡 This explains why your chatbot fell back to Ollama.")