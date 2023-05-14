# ui/command_line.py

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
            system_message("No input given!", style = Fore.RED)

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

# Dictionary of options to display
taskOptions = {
    1: "Approve Task",
    2: "Modify Task",
    3: "Skip Task"
}

decompOrExecute = {
    1: "Decompose Task",
    2: "Execute Task",
    3: "Retry"
}

# Ask user for options to input
# Tests these options for validity
def ask_options(options) -> int:
    while True:
        try:
            system_message(f"Please select how to proceed further.")
            system_message(f"Options: ")
            for i, option in enumerate(options.values()):
                system_message(f"{i+1}. {option}")

            option = int(prompt_user_input("Please select an option: "))
            if option in options.keys():
                return option
            else:
                system_message("Invalid option.")
        except ValueError:
            system_message("Invalid option.")

# Ask user Yes or No question
# Tests for valid input
def ask_yes_no(prompt) -> bool:
    while True:
        try:
            system_message(f"{Fore.GREEN}{prompt} (Y/N): {Style.RESET_ALL}")
            user_input = input().lower()
            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            else:
                system_message("Invalid input.")
        except ValueError:
            system_message("Invalid input.")

# Ask user to press any key to continue

def press_any_key_to_continue() -> None:
    system_message("Press any key to continue...")
    input()

def main() -> None:
    result = ask_options(taskOptions)
    print(result)

if __name__ == "__main__":
    main()

