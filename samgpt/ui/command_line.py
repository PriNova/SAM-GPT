# ui/command_line.py

import sys
from colorama import init, Fore, Style

init(autoreset=True)  # Automatically reset colors after each print

def prompt_user_input(prompt):
    """
    Prompt the user for input.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        The input from the user.
    """
    return input(f"{Fore.GREEN}{Style.BRIGHT}{prompt}{Style.RESET_ALL} ")

def display_ai_output(message):
    """
    Display AI output.
    
    Args:
        message (str): Message to display.
    """
    print(f"{Fore.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}")

def main():
    print("Welcome to SAM-GPT!")
    user_goal = prompt_user_input("Please input your goal: ")
    display_ai_output(f"Your goal: {user_goal}")

if __name__ == "__main__":
    main()
