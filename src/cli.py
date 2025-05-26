"""
Interactive command-line interface for the prompt configuration system.
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional
from collections import defaultdict

from .constants import get_prompt_archive_path
from .discovery import PromptDiscovery
from .generator import PromptGenerator
from .validator import PromptValidator
from .exceptions import PromptConfigError


class InteractiveCLI:
    def __init__(self):
        self.archive_path = get_prompt_archive_path()
        self.discovery = PromptDiscovery(self.archive_path)
        self.generator = PromptGenerator(self.archive_path)
        self.validator = PromptValidator(self.archive_path)
        self.prompts = []
        self.prompts_by_category = defaultdict(list)
        
    def load_prompts(self):
        """Load and organize all available prompts."""
        try:
            self.prompts = self.discovery.discover_prompts()
            self.prompts_by_category.clear()
            
            for prompt in self.prompts:
                self.prompts_by_category[prompt.category].append(prompt)
                
        except Exception as e:
            print(f"Error loading prompts: {e}")
            return False
        return True
    
    def get_user_choice(self, options: List[str], prompt_text: str = "Your choice") -> int:
        """Get user's menu choice with validation."""
        while True:
            try:
                choice = input(f"{prompt_text} (1-{len(options)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num - 1  # Convert to 0-based index
                else:
                    print(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit(0)
    
    def display_menu(self, title: str, options: List[str]) -> int:
        """Display a menu and get user's choice."""
        print(f"\n=== {title} ===\n")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print()
        return self.get_user_choice(options)
    
    def show_main_menu(self):
        """Display and handle the main menu."""
        options = ["List prompts", "Generate prompt", "Exit"]
        choice = self.display_menu("Prompt Configuration System", options)
        
        if choice == 0:
            self.handle_list_prompts()
        elif choice == 1:
            self.handle_generate_prompt()
        elif choice == 2:
            print("Goodbye!")
            sys.exit(0)
    
    def handle_list_prompts(self):
        """Handle the list prompts workflow."""
        if not self.prompts:
            print("No prompt configurations found.")
            input("Press Enter to continue...")
            return
        
        categories = sorted(self.prompts_by_category.keys())
        options = categories + ["All categories"]
        
        choice = self.display_menu("List Prompts - Select Category", options)
        
        if choice < len(categories):
            # Show specific category
            selected_category = categories[choice]
            self.show_category_prompts(selected_category)
        else:
            # Show all categories
            self.show_all_prompts()
        
        input("Press Enter to return to main menu...")
    
    def show_category_prompts(self, category: str):
        """Show prompts for a specific category."""
        print(f"\n=== {category.upper()} PROMPTS ===")
        print("=" * (len(category) + 8))
        
        prompts = self.prompts_by_category[category]
        for prompt in prompts:
            print(f"\n• {prompt.name}")
            if prompt.description:
                print(f"  Description: {prompt.description}")
            print(f"  Path: {prompt.path.relative_to(self.archive_path)}")
    
    def show_all_prompts(self):
        """Show all prompts grouped by category."""
        for category in sorted(self.prompts_by_category.keys()):
            self.show_category_prompts(category)
    
    def handle_generate_prompt(self):
        """Handle the generate prompt workflow."""
        if not self.prompts:
            print("No prompt configurations found.")
            input("Press Enter to continue...")
            return
        
        categories = sorted(self.prompts_by_category.keys())
        options = categories + ["All categories"]
        
        choice = self.display_menu("Generate Prompt - Select Category", options)
        
        if choice < len(categories):
            # Show prompts from specific category
            selected_category = categories[choice]
            available_prompts = self.prompts_by_category[selected_category]
        else:
            # Show all prompts
            available_prompts = self.prompts
        
        if not available_prompts:
            print("No prompts available in selected category.")
            input("Press Enter to continue...")
            return
        
        # Let user select specific prompt
        prompt_names = [f"{prompt.name} - {prompt.description or 'No description'}" 
                       for prompt in available_prompts]
        
        selected_category_name = categories[choice] if choice < len(categories) else "All Categories"
        prompt_choice = self.display_menu(f"Select Prompt from {selected_category_name}", prompt_names)
        
        selected_prompt = available_prompts[prompt_choice]
        self.generate_selected_prompt(selected_prompt)
        
        input("Press Enter to return to main menu...")
    
    def generate_selected_prompt(self, prompt):
        """Generate the selected prompt."""
        print(f"\nGenerating prompt '{prompt.name}'...")
        print("-" * 50)
        
        try:
            prompt_content = self.generator.generate_prompt(prompt.path)
            print(prompt_content)
        except PromptConfigError as e:
            print(f"Error generating prompt: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    def run(self):
        """Main application loop."""
        print("Welcome to the Prompt Configuration System!")
        
        # Load prompts at startup
        if not self.load_prompts():
            print("Failed to load prompts. Exiting.")
            sys.exit(1)
        
        # Main interaction loop
        while True:
            try:
                self.show_main_menu()
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")
