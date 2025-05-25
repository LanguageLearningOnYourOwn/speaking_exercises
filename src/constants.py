"""
Constants and configuration for the prompt system.
"""

from pathlib import Path

# Global prompt archive path - set relative to the main script location
def get_prompt_archive_path() -> Path:
    """Get the absolute path to the prompts directory."""
    # This will be called from the main script, so we need to go up one level
    main_script_dir = Path(__file__).parent.parent.absolute()
    return main_script_dir / "prompts"

# Default configuration
DEFAULT_CONFIG_FILENAME = "prompt-config.yaml"