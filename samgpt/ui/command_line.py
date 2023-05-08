# ui/command_line.py

import sys
from colorama import init, Fore, Style

init(autoreset=True)  # Automatically reset colors after each print

# Prompt the user for input and returns the input from the user
# If input is empty, prompt again
def prompt_user_input(prompt, style = Fore.BLUE) -> str:
    while True:
        user_input = input(f"{style}{Style.BRIGHT}{prompt}{Style.RESET_ALL}")
        if user_input:
            return user_input
        else:
            system_message("No Goal defined!", style = Fore.RED)

# Display AI output
# input message to display and color style
def ai_message(message, style = Fore.YELLOW) -> None:
    print(f"{style}{Style.BRIGHT}{message}{Style.RESET_ALL}")

# Display system message
# input: message to display and color style
def system_message(message, style = Fore.GREEN) -> None:
    print(f"{style}{message}{Style.RESET_ALL}")

# Display debug message
# input: message to display and color style
def debug_message(message, style = Fore.RED) -> None:
    print(f"{style}{message}{Style.RESET_ALL}")