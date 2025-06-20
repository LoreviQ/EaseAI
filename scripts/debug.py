#!/usr/bin/env python3
"""
Debug helper script for PresentAI development
Run with: python -m scripts.debug
"""

import sys


def run_debug_server():
    """Run the server in debug mode"""
    print("🔧 Starting PresentAI in debug mode...")

    # Import and run the main module
    try:
        import src.main

        print("✓ Successfully imported src.main")
        print("   Server should be starting...")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print(
            "Make sure you're running from the project root with: python -m scripts.debug"
        )
        sys.exit(1)


if __name__ == "__main__":
    run_debug_server()
