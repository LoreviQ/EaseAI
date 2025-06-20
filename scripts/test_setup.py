#!/usr/bin/env python3
"""
Test script to verify PresentAI setup and basic functionality
Run with: python -m scripts.test_setup
"""

import os
import sys


def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")

    try:
        import fastapi

        print("✓ FastAPI imported successfully")
    except ImportError as e:
        print(f"✗ FastAPI import failed: {e}")
        return False

    try:
        import langgraph

        print("✓ LangGraph imported successfully")
    except ImportError as e:
        print(f"✗ LangGraph import failed: {e}")
        return False

    try:
        import langchain

        print("✓ LangChain imported successfully")
    except ImportError as e:
        print(f"✗ LangChain import failed: {e}")
        return False

    try:
        import langchain_google_genai

        print("✓ LangChain Google GenAI imported successfully")
    except ImportError as e:
        print(f"✗ LangChain Google GenAI import failed: {e}")
        return False

    try:
        from src.presentation_agent import PresentationAgent

        print("✓ PresentationAgent imported successfully")
    except ImportError as e:
        print(f"✗ PresentationAgent import failed: {e}")
        return False

    return True


def test_environment():
    """Test environment setup"""
    print("\nTesting environment...")

    # Check if .env file exists or GOOGLE_API_KEY is set
    if os.path.exists(".env"):
        print("✓ .env file found")
    elif os.getenv("GOOGLE_API_KEY"):
        print("✓ GOOGLE_API_KEY environment variable found")
    else:
        print("⚠ No .env file or GOOGLE_API_KEY environment variable found")
        print("  Please create a .env file with your Google API key")
        return False

    # Check if src directory exists
    if os.path.exists("src"):
        print("✓ src directory found")
    else:
        print("✗ src directory missing")
        return False

    # Check if templates directory exists
    if os.path.exists("src/templates"):
        print("✓ Templates directory found")
        if os.path.exists("src/templates/index.html"):
            print("✓ index.html template found")
        else:
            print("✗ index.html template missing")
            return False
        if os.path.exists("src/templates/presentation.html"):
            print("✓ presentation.html template found")
        else:
            print("✗ presentation.html template missing")
            return False
    else:
        print("✗ Templates directory missing")
        return False

    # Check if scripts directory exists
    if os.path.exists("scripts"):
        print("✓ scripts directory found")
    else:
        print("✗ scripts directory missing")
        return False

    # Check pyproject.toml
    if os.path.exists("pyproject.toml"):
        print("✓ pyproject.toml found (uv project)")
    else:
        print("✗ pyproject.toml missing")
        return False

    return True


def test_agent_initialization():
    """Test if the presentation agent can be initialized"""
    print("\nTesting agent initialization...")

    try:
        # This will only work if GOOGLE_API_KEY is set
        if not os.getenv("GOOGLE_API_KEY"):
            print("⚠ Skipping agent test - no API key available")
            return True

        from src.presentation_agent import PresentationAgent

        agent = PresentationAgent()
        print("✓ PresentationAgent initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Agent initialization failed: {e}")
        return False


def test_project_structure():
    """Test if the project structure is correct"""
    print("\nTesting project structure...")

    required_files = [
        "src/main.py",
        "src/presentation_agent.py",
        "src/templates/index.html",
        "src/templates/presentation.html",
        "scripts/test_setup.py",
        "pyproject.toml",
        "README.md",
    ]

    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} found")
        else:
            print(f"✗ {file_path} missing")
            all_files_exist = False

    return all_files_exist


def main():
    """Run all tests"""
    print("🧪 PresentAI Setup Test")
    print("=" * 50)

    tests_passed = 0
    total_tests = 4

    if test_imports():
        tests_passed += 1

    if test_environment():
        tests_passed += 1

    if test_project_structure():
        tests_passed += 1

    if test_agent_initialization():
        tests_passed += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("🎉 All tests passed! Your PresentAI setup is ready.")
        print("\nTo start the application:")
        print("  cd src && uv run python main.py")
        print("  or")
        print("  uv run python src/main.py")
        print("\nThen open: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please check the setup instructions.")
        print("\nMake sure to:")
        print("  1. Set up your Google API key in .env file")
        print("  2. Run 'uv sync' to install dependencies")
        sys.exit(1)


if __name__ == "__main__":
    main()
