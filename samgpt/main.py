import samgpt.ui.command_line as cmd
import samgpt.planning.task_manager as tm
import samgpt.agents.task_delegator as td
import samgpt.agents.plan_generator as pg
import samgpt.utils.io_utils as ioutils

from typing import List, Optional, Dict

# The main entry point of the application
def main() -> None:
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")
    cmd.system_message(f"Hold on. SAM-GPT will generate the plan for you.")
    plan: Optional[List[str]|None] = pg.generate_plan(userGoal)
    cPlan = []
    if plan is None:
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
    else:
        cPlan = plan
    cmd.ai_message(cPlan[0])
    ioutils.save_plan(goal=userGoal, plan=cPlan[1], filename="plan.json")

    firstTask : Dict = tm.get_task(plan=cPlan[1], index=0)
    firstTask = manage_task(userGoal, cPlan, firstTask)
    cmd.system_message("Hold on. SAM-GPT will delegate your task.")
    response = td.delegate_task(userGoal, firstTask)
    cmd.ai_message(f"Here is my response:\n{response}")

def manage_task(userGoal, cPlan, firstTask) -> Dict:
    cmd.ai_message(f"\nYour current task is: {firstTask['description']} (Status: {firstTask['status']})")
    kindOption = cmd.ask_options()
    if kindOption == 1: # Approve Task
        firstTask["status"] = "In Progress"
        ioutils.save_current_task(userGoal, firstTask)
        return firstTask
    elif kindOption == 2: # Modify Task
        cmd.system_message("Modify the task description")
        firstTask["description"] = cmd.prompt_user_input("Please input your new task description: ")
        ioutils.save_current_task(userGoal, firstTask)
        return manage_task(userGoal, cPlan, firstTask)
    elif kindOption == 3: # Skip Task
        index = firstTask["id"]
        firstTask["status"] = "Skipped"
        firstTask = tm.get_task(plan=cPlan[1], index=index)
        return manage_task(userGoal, cPlan, firstTask)
    return firstTask
    
if __name__ == "__main__":
    main()
