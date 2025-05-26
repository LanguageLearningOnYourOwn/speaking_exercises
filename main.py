#!/usr/bin/env python3
"""
Main entry point for the Prompt Configuration System.

This script serves as the primary entry point for the CLI tool.
It imports and runs the CLI interface from the src package.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path so we can import our modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.cli import InteractiveCLI

def main():
    """Entry point for the interactive CLI."""
    cli = InteractiveCLI()
    cli.run()


if __name__ == '__main__':
    main()