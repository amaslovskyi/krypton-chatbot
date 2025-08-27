#!/usr/bin/env python3
"""
Quick script to verify .env file loading for CURCUIT API configuration.
"""

import os
from pathlib import Path

# Check if .env file exists
env_file = Path(".env")
if not env_file.exists():
    print("❌ .env file not found")
    print("💡 Run './install.sh' to create .env template")
    exit(1)

print("🔍 Checking .env file for CURCUIT configuration...")

# Read .env file
with open(".env", "r") as f:
    content = f.read()

# Check for CURCUIT variables
curcuit_vars = [
    "USE_CURCUIT_API",
    "CURCUIT_CLIENT_ID",
    "CURCUIT_CLIENT_SECRET",
    "CURCUIT_APP_KEY",
    "CURCUIT_MODEL",
]

found_vars = []
missing_vars = []

for var in curcuit_vars:
    if var in content:
        # Extract value
        lines = [line for line in content.split("\n") if line.startswith(f"{var}=")]
        if lines:
            value = lines[0].split("=", 1)[1]
            if value and not value.startswith("your_"):
                found_vars.append(f"✅ {var}={value}")
            else:
                found_vars.append(f"⚠️  {var}={value} (needs configuration)")
        else:
            found_vars.append(f"⚠️  {var} (found but no value)")
    else:
        missing_vars.append(f"❌ {var}")

print("\n📋 CURCUIT Configuration Status:")
for var in found_vars:
    print(f"  {var}")
for var in missing_vars:
    print(f"  {var}")

if missing_vars:
    print(f"\n❌ Missing {len(missing_vars)} CURCUIT variables")
    print("💡 Update your .env file with the missing variables")
else:
    print(f"\n✅ All {len(curcuit_vars)} CURCUIT variables found in .env")

# Test loading with pydantic if available
try:
    import sys

    sys.path.append(".")

    from config import get_settings

    settings = get_settings()

    print(f"\n🧪 Testing configuration loading:")
    print(f"  use_curcuit_api: {settings.use_curcuit_api}")
    print(f"  curcuit_model: {settings.curcuit_model}")

    if settings.curcuit_client_id and not settings.curcuit_client_id.startswith(
        "your_"
    ):
        print(f"  curcuit_client_id: {settings.curcuit_client_id[:10]}...")
    else:
        print(
            f"  curcuit_client_id: {settings.curcuit_client_id} (needs configuration)"
        )

    if settings.curcuit_client_secret and not settings.curcuit_client_secret.startswith(
        "your_"
    ):
        print(f"  curcuit_client_secret: {settings.curcuit_client_secret[:10]}...")
    else:
        print(
            f"  curcuit_client_secret: {settings.curcuit_client_secret} (needs configuration)"
        )

    if settings.curcuit_app_key and not settings.curcuit_app_key.startswith("your_"):
        print(f"  curcuit_app_key: {settings.curcuit_app_key[:10]}...")
    else:
        print(f"  curcuit_app_key: {settings.curcuit_app_key} (needs configuration)")

    print("\n✅ Configuration loading successful!")

except ImportError as e:
    print(f"\n⚠️  Cannot test configuration loading: {e}")
    print("💡 Install dependencies: pip install -r requirements.txt")
except Exception as e:
    print(f"\n❌ Configuration loading failed: {e}")
