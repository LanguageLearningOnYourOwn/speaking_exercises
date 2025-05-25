"""
Command-line interface for the prompt configuration system.
"""

import sys
from pathlib import Path
from typing import Optional
from collections import defaultdict

import click

from .constants import get_prompt_archive_path
from .discovery import PromptDiscovery
from .validator import PromptValidator
from .generator import PromptGenerator
from .exceptions import PromptConfigError


def find_prompt_config(prompt_name: str, archive_path: Path) -> Optional[Path]:
    """Find configuration file for a given prompt name."""
    discovery = PromptDiscovery(archive_path)
    prompts = discovery.discover_prompts()
    
    for prompt in prompts:
        if prompt.name == prompt_name:
            return prompt.path
    
    return None


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Prompt Configuration System - Manage and generate prompts from templates."""
    pass


@cli.command()
def list():
    """List all available prompt configurations."""
    archive_path = get_prompt_archive_path()
    discovery = PromptDiscovery(archive_path)
    prompts = discovery.discover_prompts()
    
    if not prompts:
        click.echo("No prompt configurations found.")
        return
    
    # Group by category
    by_category = defaultdict(list)
    for prompt in prompts:
        by_category[prompt.category].append(prompt)
    
    for category in sorted(by_category.keys()):
        click.echo(f"\n{category.upper()} PROMPTS:")
        click.echo("=" * (len(category) + 8))
        
        for prompt in by_category[category]:
            click.echo(f"  • {prompt.name}")
            if prompt.description:
                click.echo(f"    {prompt.description}")
            click.echo(f"    Path: {prompt.path.relative_to(archive_path)}")


@cli.command()
@click.argument('prompt_name')
def validate(prompt_name):
    """Validate a specific prompt configuration."""
    archive_path = get_prompt_archive_path()
    config_path = find_prompt_config(prompt_name, archive_path)
    
    if not config_path:
        click.echo(f"Error: Prompt '{prompt_name}' not found.", err=True)
        sys.exit(1)
    
    validator = PromptValidator(archive_path)
    
    try:
        config = validator.validate_config_file(config_path)
        click.echo(f"✓ Prompt '{prompt_name}' is valid")
        click.echo(f"  Template: {config.prompt_path}")
        click.echo(f"  Inputs: {len(config.prompt_input)} files")
        if config.description:
            click.echo(f"  Description: {config.description}")
    except PromptConfigError as e:
        click.echo(f"✗ Validation failed for '{prompt_name}': {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('prompt_name')
@click.option('--output', '-o', help='Output file (default: stdout)')
def generate(prompt_name, output):
    """Generate a prompt from its configuration."""
    archive_path = get_prompt_archive_path()
    config_path = find_prompt_config(prompt_name, archive_path)
    
    if not config_path:
        click.echo(f"Error: Prompt '{prompt_name}' not found.", err=True)
        sys.exit(1)
    
    generator = PromptGenerator(archive_path)
    
    try:
        prompt_content = generator.generate_prompt(config_path)
        
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(prompt_content)
            click.echo(f"Prompt generated and saved to: {output}")
        else:
            click.echo(prompt_content)
    
    except PromptConfigError as e:
        click.echo(f"Error generating prompt '{prompt_name}': {e}", err=True)
        sys.exit(1)


@cli.command()
def validate_all():
    """Validate all prompt configurations."""
    archive_path = get_prompt_archive_path()
    discovery = PromptDiscovery(archive_path)
    prompts = discovery.discover_prompts()
    
    if not prompts:
        click.echo("No prompt configurations found.")
        return
    
    validator = PromptValidator(archive_path)
    valid_count = 0
    
    for prompt in prompts:
        try:
            validator.validate_config_file(prompt.path)
            click.echo(f"✓ {prompt.name}")
            valid_count += 1
        except PromptConfigError as e:
            click.echo(f"✗ {prompt.name}: {e}", err=True)
    
    click.echo(f"\nValidation complete: {valid_count}/{len(prompts)} prompts are valid")
    
    if valid_count < len(prompts):
        sys.exit(1)


if __name__ == '__main__':
    cli()