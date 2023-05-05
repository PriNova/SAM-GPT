# ui/command_line.py

import sys
from colorama import init, Fore, Style

init(autoreset=True)  # Automatically reset colors after each print

# Prompt the user for input and returns the input from the user
def prompt_user_input(prompt, style = Fore.GREEN ):
    return input(f"{style}{Style.BRIGHT}{prompt}{Style.RESET_ALL} ")

# Display AI output
# input message to display and color style
def ai_message(message, style = Fore.YELLOW):
    print(f"{style}{Style.BRIGHT}{message}{Style.RESET_ALL}")

# Display system message
# input: message to display and color style
def system_message(message, style = Fore.GREEN):
    print(f"{style}{message}{Style.RESET_ALL}")

# Display debug message
# input: message to display and color style
def debug_message(message, style = Fore.RED):
    print(f"{style}{message}{Style.RESET_ALL}")


def main():
    system_message("Welcome to SAM-GPT!", Fore.GREEN)
    user_goal = prompt_user_input("Please input your goal:")
    ai_message(f"Your goal: {user_goal}", Fore.YELLOW)

if __name__ == "__main__":
    main()
