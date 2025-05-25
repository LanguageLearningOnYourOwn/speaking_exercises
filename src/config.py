"""
Data structures for prompt configurations and metadata.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional


@dataclass
class PromptInfo:
    """Information about a discovered prompt configuration."""
    name: str
    category: str  # 'task' or 'other'
    path: Path
    description: Optional[str] = None


@dataclass
class PromptConfig:
    """Parsed prompt configuration."""
    prompt_path: str
    prompt_input: Dict[str, str]
    name: Optional[str] = None
    description: Optional[str] = None