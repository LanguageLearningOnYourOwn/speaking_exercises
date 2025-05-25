"""
Validation functionality for prompt configurations and referenced files.
"""

from pathlib import Path
from typing import Dict, Any
import yaml

from .config import PromptConfig
from .exceptions import PromptConfigError


class PromptValidator:
    """Validates prompt configurations and referenced files."""
    
    def __init__(self, archive_path: Path):
        """Initialize validator with the prompt archive path."""
        self.archive_path = archive_path
    
    def validate_config_file(self, config_path: Path) -> PromptConfig:
        """Validate and parse a prompt configuration file."""
        if not config_path.exists():
            raise PromptConfigError(f"Config file does not exist: {config_path}")
        
        if config_path.stat().st_size == 0:
            raise PromptConfigError(f"Config file is empty: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise PromptConfigError(f"Invalid YAML in {config_path}: {e}")
        
        return self._parse_config_data(config_data, config_path.parent)
    
    def _parse_config_data(self, config_data: Dict[str, Any], config_dir: Path) -> PromptConfig:
        """Parse and validate configuration data structure."""
        if not isinstance(config_data, dict):
            raise PromptConfigError("Config must be a YAML object")
        
        if 'prompt' not in config_data:
            raise PromptConfigError("Config must contain 'prompt' field")
        
        prompt_path = config_data['prompt']
        prompt_input = config_data.get('prompt_input', {})
        
        if not isinstance(prompt_input, dict):
            raise PromptConfigError("'prompt_input' must be a dictionary")
        
        # Validate prompt template file
        self._validate_file_exists(self.archive_path / prompt_path)
        
        # Validate all input files
        for key, file_path in prompt_input.items():
            self._validate_file_exists(self.archive_path / file_path)
        
        return PromptConfig(
            prompt_path=prompt_path,
            prompt_input=prompt_input,
            name=config_data.get('name'),
            description=config_data.get('description')
        )
    
    def _validate_file_exists(self, file_path: Path) -> None:
        """Validate that a file exists and is not empty."""
        if not file_path.exists():
            raise PromptConfigError(f"Referenced file does not exist: {file_path}")
        
        if file_path.stat().st_size == 0:
            raise PromptConfigError(f"Referenced file is empty: {file_path}")