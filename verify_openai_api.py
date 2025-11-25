"""
===================================================================================
OpenAI API Key Verification Tool - Production Grade
===================================================================================

This script provides comprehensive OpenAI API key testing with:
- Clear, actionable error messages
- Environment variable override handling
- Detailed diagnostics
- Windows console UTF-8 support
- Professional output formatting

Author: Automotive Analytics Team
Version: 2.0.0
Last Updated: 2024

Usage:
    python verify_openai_api.py
    
    Or from batch file:
    test_api.bat

===================================================================================
"""

import os
import sys
from pathlib import Path
from typing import Optional, Tuple


# ===================================================================================
# SECTION 1: Console Configuration
# ===================================================================================
# Configure UTF-8 encoding for Windows console to properly display emoji/unicode

def configure_console():
    """
    Configure console for UTF-8 output on Windows.
    
    Why: Windows PowerShell default encoding can cause issues with emoji and
    special characters. This ensures consistent output across platforms.
    """
    if sys.platform == 'win32':
        try:
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        except Exception:
            # If encoding setup fails, continue anyway
            pass


# ===================================================================================
# SECTION 2: Environment Variable Loading
# ===================================================================================

def load_environment_variables() -> Optional[str]:
    """
    Load OpenAI API key from .env file.
    
    CRITICAL: Uses override=True to ensure .env file takes precedence over
    existing PowerShell environment variables. This prevents confusion when
    testing with updated keys.
    
    Returns:
        str: API key if found, None otherwise
        
    Why override=True:
        - Without it: PowerShell env vars take precedence over .env
        - With it: .env always takes precedence (ensures latest key is tested)
        - This is the source of the "old key vs new key" confusion!
    """
    try:
        from dotenv import load_dotenv
        
        # CRITICAL: override=True ensures .env takes precedence
        # This was the missing piece causing your confusion!
        load_dotenv(override=True)
        
        return os.getenv("OPENAI_API_KEY")
        
    except ImportError:
        print("\n❌ ERROR: python-dotenv not installed")
        print("\nInstall it with:")
        print("   pip install python-dotenv")
        return None


# ===================================================================================
# SECTION 3: API Key Validation
# ===================================================================================

def validate_api_key_format(api_key: str) -> Tuple[bool, str]:
    """
    Validate OpenAI API key format.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    OpenAI Key Formats:
        - Legacy keys: sk-... (48 characters)
        - Project keys: sk-proj-... (164 characters)
    """
    if not api_key:
        return False, "API key is empty"
    
    if not api_key.startswith(("sk-", "sk-proj-")):
        return False, f"Key should start with 'sk-' or 'sk-proj-', got: {api_key[:10]}..."
    
    if len(api_key) < 20:
        return False, f"Key too short ({len(api_key)} chars). Should be 48+ for legacy or 164 for project keys"
    
    return True, "Format looks correct"


def mask_api_key(api_key: str) -> str:
    """
    Mask API key for safe display.
    
    Args:
        api_key: Full API key
        
    Returns:
        Masked version like "sk-proj-abc123...xyz789"
    """
    if len(api_key) <= 20:
        return api_key[:5] + "..." + api_key[-4:]
    return api_key[:15] + "..." + api_key[-4:]


# ===================================================================================
# SECTION 4: OpenAI API Connection Testing
# ===================================================================================

def test_openai_connection(api_key: str) -> bool:
    """
    Test actual connection to OpenAI API with a minimal request.
    
    Args:
        api_key: OpenAI API key to test
        
    Returns:
        True if connection successful, False otherwise
        
    This makes a real API call using minimal tokens (~15 tokens ≈ $0.0001)
    to verify the key works end-to-end.
    """
    try:
        from openai import OpenAI
        
        print("   Creating OpenAI client...")
        client = OpenAI(api_key=api_key)
        
        print("   Sending test request to GPT-3.5-turbo...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Reply with exactly: API_TEST_OK"}
            ],
            max_tokens=5,
            temperature=0
        )
        
        # Extract response
        result = response.choices[0].message.content.strip()
        
        # Display results
        print("\n" + "="*75)
        print("  ✨ SUCCESS! YOUR API KEY WORKS! ✨")
        print("="*75)
        print(f"\n📊 Test Results:")
        print(f"   Model:        {response.model}")
        print(f"   Response:     {result}")
        print(f"   Tokens used:  {response.usage.total_tokens}")
        print(f"   Cost:         ~$0.0001 (about 1 cent per 100 tests)")
        
        return True
        
    except ImportError:
        print("\n❌ ERROR: OpenAI library not installed")
        print("\nInstall it with:")
        print("   pip install openai")
        return False
        
    except Exception as e:
        handle_api_error(e)
        return False


# ===================================================================================
# SECTION 5: Error Handling & Diagnostics
# ===================================================================================

def handle_api_error(error: Exception):
    """
    Provide detailed, actionable error messages based on the error type.
    
    Args:
        error: The exception that was raised
        
    Common Error Codes:
        401: Invalid API key
        429: Rate limit exceeded
        500: OpenAI server error
    """
    error_str = str(error).lower()
    error_type = type(error).__name__
    
    print("\n" + "="*75)
    print("  ❌ API CONNECTION FAILED")
    print("="*75)
    print(f"\nError Type: {error_type}")
    
    # Parse error for specific issues
    if "401" in error_str or "unauthorized" in error_str or "invalid" in error_str:
        print("\n🔍 DIAGNOSIS: Invalid API Key")
        print("\n💡 SOLUTIONS:")
        print("   1. Go to: https://platform.openai.com/api-keys")
        print("   2. Click '+ Create new secret key'")
        print("   3. Copy the ENTIRE key (it's shown only once!)")
        print("   4. Open your .env file")
        print("   5. Update: OPENAI_API_KEY=sk-proj-your-new-key")
        print("   6. Save and run this test again")
        print("\n⚠️  IMPORTANT:")
        print("   - Make sure there are NO spaces before/after the key")
        print("   - Make sure there are NO quotes around the key")
        print("   - The key should be 164 characters for project keys")
        
    elif "429" in error_str or "rate" in error_str:
        print("\n🔍 DIAGNOSIS: Rate Limit Exceeded")
        print("\n💡 SOLUTIONS:")
        print("   1. Wait 60 seconds and try again")
        print("   2. Check rate limits: https://platform.openai.com/account/limits")
        print("   3. Consider upgrading: https://platform.openai.com/account/billing")
        
    elif "quota" in error_str or "billing" in error_str or "insufficient" in error_str:
        print("\n🔍 DIAGNOSIS: No Credits / Billing Issue")
        print("\n💡 SOLUTIONS:")
        print("   1. Check billing: https://platform.openai.com/account/billing")
        print("   2. Add payment method (credit card)")
        print("   3. Add at least $5 to your account")
        print("   4. Wait 5 minutes for changes to take effect")
        
    elif "500" in error_str or "502" in error_str or "503" in error_str:
        print("\n🔍 DIAGNOSIS: OpenAI Server Issue")
        print("\n💡 SOLUTIONS:")
        print("   1. Check OpenAI status: https://status.openai.com/")
        print("   2. Wait a few minutes and try again")
        print("   3. The issue is on OpenAI's side, not yours")
        
    elif "connection" in error_str or "network" in error_str:
        print("\n🔍 DIAGNOSIS: Network/Connection Issue")
        print("\n💡 SOLUTIONS:")
        print("   1. Check your internet connection")
        print("   2. Check if firewall is blocking api.openai.com")
        print("   3. Try from a different network")
        print("   4. Check corporate proxy settings")
        
    else:
        print("\n🔍 DIAGNOSIS: Unknown Error")
        print(f"\nError Details: {str(error)[:300]}")
        print("\n💡 SOLUTIONS:")
        print("   1. Check OpenAI status: https://status.openai.com/")
        print("   2. Check your .env file formatting")
        print("   3. Contact support if issue persists")
    
    print("\n" + "="*75)


# ===================================================================================
# SECTION 6: Main Execution Flow
# ===================================================================================

def print_header():
    """Print formatted header."""
    print("\n" + "="*75)
    print("  🔑 OPENAI API KEY VERIFICATION")
    print("  Version 2.0.0 - Production Grade")
    print("="*75)


def print_section(title: str):
    """Print section header."""
    print(f"\n📋 {title}")
    print("-" * 75)


def main():
    """
    Main execution flow.
    
    Steps:
        1. Configure console
        2. Check .env file exists
        3. Load API key from .env (with override!)
        4. Validate key format
        5. Test API connection
        6. Display results
    """
    # Step 1: Configure console
    configure_console()
    
    # Step 2: Display header
    print_header()
    
    # Step 3: Check .env file
    print_section("Step 1: Checking .env File")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("\n❌ ERROR: .env file not found!")
        print(f"\nExpected location: {env_path.absolute()}")
        print("\n📝 Create .env file with:")
        print("   OPENAI_API_KEY=sk-proj-your-key-here")
        print("   DATABASE_URL=postgresql://user:pass@localhost:5432/db")
        return False
    
    print(f"   ✅ Found: {env_path.absolute()}")
    
    # Step 4: Load API key
    print_section("Step 2: Loading API Key from .env")
    
    api_key = load_environment_variables()
    
    if not api_key:
        print("\n❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("\n📝 Make sure your .env file contains:")
        print("   OPENAI_API_KEY=sk-proj-your-key-here")
        print("\n⚠️  Common mistakes:")
        print("   ❌ OPENAI_API_KEY = sk-...  (spaces around =)")
        print("   ❌ OPENAI_API_KEY='sk-...'  (quotes)")
        print("   ✅ OPENAI_API_KEY=sk-...    (correct)")
        return False
    
    print(f"   ✅ Loaded: {mask_api_key(api_key)}")
    print(f"   Length: {len(api_key)} characters")
    
    # Step 5: Validate format
    print_section("Step 3: Validating API Key Format")
    
    is_valid, message = validate_api_key_format(api_key)
    if is_valid:
        print(f"   ✅ {message}")
        if api_key.startswith("sk-proj-"):
            print("   Type: Project key (recommended)")
        else:
            print("   Type: Legacy key (consider upgrading)")
    else:
        print(f"   ❌ {message}")
        print("\n⚠️  Your key doesn't look right. Please:")
        print("   1. Check you copied the ENTIRE key")
        print("   2. Make sure there are no spaces or line breaks")
        print("   3. The key should be one continuous string")
        return False
    
    # Step 6: Test connection
    print_section("Step 4: Testing Connection to OpenAI API")
    
    success = test_openai_connection(api_key)
    
    # Step 7: Final message
    print("\n" + "="*75)
    if success:
        print("\n🎉 VERIFICATION COMPLETE - ALL SYSTEMS GO!")
        print("\nYou can now:")
        print("   • Start your services: start.bat")
        print("   • Access Dashboard: http://localhost:8501")
        print("   • Access API Docs: http://localhost:8000/docs")
        print("\n" + "="*75 + "\n")
        return True
    else:
        print("\n❌ VERIFICATION FAILED - Please fix the issues above")
        print("\nNeed help? Check: https://platform.openai.com/docs")
        print("=" * 75 + "\n")
        return False


# ===================================================================================
# SECTION 7: Entry Point
# ===================================================================================

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user (Ctrl+C)\n")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}")
        print(f"Message: {e}")
        print("\nPlease report this error if it persists.")
        
        # Show traceback in debug mode
        if os.getenv("DEBUG"):
            import traceback
            traceback.print_exc()
        
        sys.exit(1)

