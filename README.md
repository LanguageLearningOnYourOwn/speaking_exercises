# Prompt Configuration System

A CLI tool for managing and generating prompts from template files with YAML configurations.

## Features

- **Prompt Discovery**: Automatically finds all prompt configurations in your archive
- **Validation**: Ensures all configurations are valid and referenced files exist
- **Generation**: Creates prompts by filling templates with content from input files
- **User-friendly CLI**: Easy-to-use command-line interface with helpful commands

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run directly using the main script:
```bash
python main.py --help
```

3. Or install as a package:
```bash
pip install -e .
```

## Project Structure

```
.
├── main.py              # Main entry point
├── src/                 # Source code
│   ├── __init__.py     # Package initialization
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration data structures
│   ├── constants.py    # System constants
│   ├── discovery.py    # Prompt discovery functionality
│   ├── exceptions.py   # Custom exceptions
│   ├── generator.py    # Prompt generation
│   └── validator.py    # Configuration validation
├── tests/              # Test files
├── prompts/            # Prompt templates and configurations
├── requirements.txt    # Python dependencies
├── setup.py           # Package setup
└── README.md          # This file
```

## Usage

### List Available Prompts
```bash
python main.py list
# or if installed as package:
prompt-cli list
```

### Validate a Specific Prompt
```bash
python main.py validate taboo_reformulate
```

### Validate All Prompts
```bash
python main.py validate-all
```

### Generate a Prompt
```bash
# Output to stdout
python main.py generate taboo_reformulate

# Save to file
python main.py generate taboo_reformulate -o output.txt
```

### Get Help
```bash
python main.py --help
python main.py generate --help
```

## Configuration Format

Prompt configurations are YAML files named `prompt-config.yaml` with the following structure:

```yaml
# Required: Path to the template file (relative to prompts directory)
prompt: components/prompt/feedback_only.md

# Optional: Mapping of template variables to input files
prompt_input:
  instruction: task/taboo_reformulate/instruction.md
  feedback: components/feedback/default.md

# Optional: Metadata
name: taboo_reformulate
description: |
  Reformulate the given text to avoid using any of the words in the provided taboo list.
  The reformulated text should maintain the original meaning while adhering to the taboo restrictions.
```

## Directory Structure

The system expects a `prompts/` directory with the following structure:

```
prompts/
├── components/          # Reusable prompt components
│   ├── feedback/
│   └── prompt/
├── task/               # Task-specific prompts
│   └── taboo_reformulate/
│       └── prompt-config.yaml
└── other/              # Other prompt types
    └── taboo_reformulate_generator/
        └── prompt-config.yaml
```

## Template Format

Templates use Python's string formatting syntax:

```markdown
# Instruction

## Your Task
{instruction}

## Feedback
{feedback}
```

Variables in `{}` are replaced with content from files specified in the `prompt_input` configuration.

## Error Handling

The tool provides clear error messages for common issues:
- Missing or empty configuration files
- Invalid YAML syntax
- Missing template or input files
- Template variables without corresponding inputs

## Architecture

The code follows SOLID principles with a modular structure:

### Core Modules:
- **`src/config.py`**: Data structures (`PromptInfo`, `PromptConfig`)
- **`src/validator.py`**: Validates configurations and files
- **`src/discovery.py`**: Finds available prompt configurations  
- **`src/generator.py`**: Generates prompts from templates
- **`src/cli.py`**: Command-line interface
- **`src/exceptions.py`**: Custom exception classes
- **`src/constants.py`**: System constants and configuration

### Key Features:
- **Single Responsibility**: Each module has a clear, focused purpose
- **Dependency Injection**: Components accept dependencies rather than creating them
- **Error Handling**: Comprehensive validation with clear error messages
- **Extensibility**: Easy to add new functionality or modify existing behavior

Each class can be used independently or extended for custom functionality.