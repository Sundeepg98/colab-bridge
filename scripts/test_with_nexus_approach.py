#!/usr/bin/env python3
"""
Test Claude Tools using the Nexus/Colab Secrets approach
This uses API keys stored in Colab secrets instead of service accounts
"""

import os
import sys
from pathlib import Path

print("🔍 Checking Nexus Project Colab Integration Approach")
print("=" * 50)

# Check if we have any credentials from nexus project
nexus_path = Path("/var/projects/nexus-creative-studio/colab-integration")

if nexus_path.exists():
    print("✅ Found nexus-creative-studio project")
    print(f"📁 Location: {nexus_path}")
    
    # Check for Colab notebook
    colab_notebook = nexus_path / "colab_notebooks" / "sun_colab_integration.ipynb"
    if colab_notebook.exists():
        print(f"✅ Found Colab notebook: {colab_notebook.name}")
        print("📝 This notebook uses Colab Secrets approach")
    
    # Show the approach they use
    print("\n📋 Nexus Integration Method:")
    print("1. Uses Colab Secrets (not service accounts)")
    print("2. Stores API key as 'sun_colab' secret in Colab")
    print("3. Uses ngrok for public endpoint")
    print("4. Runs FastAPI server in Colab")
    
    print("\n🔗 Their Colab Notebook:")
    print("https://colab.research.google.com/drive/1EwfBj0nC9St-2hB1bv2zGWWDTcS4slsx")
    
else:
    print("❌ Nexus project not found")

print("\n" + "=" * 50)
print("📊 Comparison of Approaches:")
print("=" * 50)

print("\n1️⃣ Claude Tools Approach (Google Drive API):")
print("   - Uses service account JSON file")
print("   - Communicates via Google Drive files")
print("   - More secure for production")
print("   - Works with multiple instances")

print("\n2️⃣ Nexus Approach (Colab Secrets + ngrok):")
print("   - Uses Colab secrets for API keys")
print("   - Direct HTTP communication via ngrok")
print("   - Simpler setup")
print("   - Good for single-user scenarios")

print("\n💡 To use your existing Nexus credentials with Claude Tools:")
print("1. Export the Colab secret value")
print("2. Create a service account for Drive API")
print("3. Or adapt Claude Tools to use the ngrok approach")

# Check if user wants to copy nexus configuration
print("\n🤔 Would you like to:")
print("1. Use Claude Tools with Google Drive (recommended)")
print("2. Adapt Claude Tools to use Nexus's ngrok approach")
print("3. View Nexus's integration code")

print("\n📝 For now, let's check what credentials are available...")

# Check for any .env files
env_files = list(Path("/var/projects").rglob(".env"))
print(f"\n🔍 Found {len(env_files)} .env files in projects")

# Check for service account files (safely)
sa_files = []
for ext in ["*.json"]:
    for f in Path("/var/projects").rglob(ext):
        if "service" in f.name.lower() and "account" in f.name.lower() and "template" not in f.name.lower():
            sa_files.append(f)

print(f"🔍 Found {len(sa_files)} potential service account files")

print("\n✅ Next Steps:")
print("1. Decide which approach to use")
print("2. Set up appropriate credentials")
print("3. Test the integration")