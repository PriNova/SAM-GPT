import samgpt.ui.command_line as cmd
import samgpt.agents.task_generator as tg
import samgpt.agents.task_delegator as td
import samgpt.planning.plan_generation as pg
import samgpt.utils.io_utils as ioutils

from typing import List, Optional, Dict

# The main entry point of the application
def main() -> None:
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")
    cmd.system_message(f"Hold on. SAM-GPT will generate the plan for you.")
    plan: Optional[List[str]|None] = pg.generate_plan(userGoal)
    if plan is None:
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
    else:
        cmd.ai_message(plan[0])
        ioutils.save_plan(goal=userGoal, plan=plan[1], filename="plan.json")
        firstTask : Dict = tg.task_tracking(goal=userGoal, plan=plan[1])
        ioutils.save_current_task(userGoal, firstTask)
        cmd.ai_message(f"Your first task is: {firstTask['description']} (Status: {firstTask['status']})")
        cmd.system_message("Hold on. SAM-GPT will delegate your first task.")
        response = td.delegate_task(userGoal,firstTask)
        cmd.ai_message(f"Here is my response:\n{response}")
    
if __name__ == "__main__":
    main()
