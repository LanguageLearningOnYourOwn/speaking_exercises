"""
Prompt generation functionality from templates and configurations.
"""

from pathlib import Path

from .validator import PromptValidator
from .exceptions import PromptConfigError


class PromptGenerator:
    """Generates prompts from templates and configurations."""
    
    def __init__(self, archive_path: Path):
        """Initialize generator with the prompt archive path."""
        self.archive_path = archive_path
        self.validator = PromptValidator(archive_path)
    
    def generate_prompt(self, config_path: Path) -> str:
        """Generate a prompt from a configuration file."""
        config = self.validator.validate_config_file(config_path)
        
        # Read template file
        template_path = self.archive_path / config.prompt_path
        template_content = self._read_file_content(template_path)
        
        # Read input files and create format dictionary
        format_dict = {}
        for key, file_path in config.prompt_input.items():
            input_path = self.archive_path / file_path
            format_dict[key] = self._read_file_content(input_path)
        
        # Format template with inputs
        try:
            return template_content.format(**format_dict)
        except KeyError as e:
            raise PromptConfigError(f"Template references undefined key: {e}")
    
    def _read_file_content(self, file_path: Path) -> str:
        """Read content from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            raise PromptConfigError(f"Cannot read file (encoding issue): {file_path}")
        except IOError as e:
            raise PromptConfigError(f"Cannot read file: {file_path}: {e}")