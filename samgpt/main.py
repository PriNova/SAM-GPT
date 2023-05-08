import samgpt.ui.command_line as cmd
import samgpt.agents.task_generator as tg

# The main entry point of the application
def main():
    cmd.system_message("Welcome to SAM-GPT!", cmd.Fore.GREEN)
    user_goal = cmd.prompt_user_input("Please input your goal:")
    cmd.system_message(f"Your goal: {user_goal}", cmd.Fore.YELLOW)
    cmd.ai_message(f"Hold on. I will generate the plan for you")
    plan = tg.generate_plan(user_goal)
    cmd.ai_message(f"Here is your plan: {plan}")

if __name__ == "__main__":
    main()
