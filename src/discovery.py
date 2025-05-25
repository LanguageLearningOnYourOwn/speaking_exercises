"""
Discovery functionality for finding available prompt configurations.
"""

from pathlib import Path
from typing import List, Optional
import yaml

from .config import PromptInfo


class PromptDiscovery:
    """Discovers available prompt configurations in the archive."""
    
    def __init__(self, archive_path: Path):
        """Initialize discovery with the prompt archive path."""
        self.archive_path = archive_path
    
    def discover_prompts(self) -> List[PromptInfo]:
        """Find all prompt configurations in the archive."""
        prompts = []
        
        if not self.archive_path.exists():
            return prompts
        
        for config_file in self.archive_path.rglob("prompt-config.yaml"):
            prompt_info = self._create_prompt_info(config_file)
            if prompt_info:
                prompts.append(prompt_info)
        
        return sorted(prompts, key=lambda p: (p.category, p.name))
    
    def _create_prompt_info(self, config_path: Path) -> Optional[PromptInfo]:
        """Create PromptInfo from a configuration file."""
        try:
            # Determine category based on path structure
            relative_path = config_path.relative_to(self.archive_path)
            category = self._determine_category(relative_path)
            
            # Use directory name as prompt name
            name = config_path.parent.name
            
            # Try to get description from config
            description = self._extract_description(config_path)
            
            return PromptInfo(
                name=name,
                category=category,
                path=config_path,
                description=description
            )
        except Exception:
            # Skip malformed configurations during discovery
            return None
    
    def _determine_category(self, relative_path: Path) -> str:
        """Determine prompt category from its path."""
        parts = relative_path.parts
        category = parts[0] if len(parts) > 0 else 'unknown'
        return category
    
    def _extract_description(self, config_path: Path) -> Optional[str]:
        """Extract description from configuration file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            return config_data.get('description') if isinstance(config_data, dict) else None
        except Exception:
            return None