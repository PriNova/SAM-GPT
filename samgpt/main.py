import samgpt.ui.command_line as cmd
import samgpt.planning.task_manager as tm
import samgpt.agents.task_delegator as td
import samgpt.agents.plan_generator as pg
import samgpt.utils.io_utils as ioutils

from typing import List, Optional, Dict
import json

# The main entry point of the application
def main() -> None:

    # Introducing
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")

    # Plan generation
    cmd.system_message(f"Hold on. SAM-GPT will generate the plan for you.")
    plan: Optional[List[str]|None] = pg.generate_plan(userGoal)
    cPlan: List[str] = []
    if plan is None:
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
    else:
        cPlan = plan
    cmd.ai_message(cPlan[0])
    ioutils.save_plan(goal=userGoal, plan=cPlan[1], filename="plan.json")

    # Task handling
    firstTask : Dict = tm.get_task(plan=cPlan[1], index=0)
    firstTask = manage_task(userGoal, cPlan, firstTask)
    cmd.system_message("Hold on. SAM-GPT will delegate your task.")
    response = td.delegate_task(userGoal, firstTask)
    cmd.ai_message(f"Here is my response:\n{response}")

def manage_task(userGoal: str, cPlan: List[str], currentTask: Dict) -> Dict:
    cmd.ai_message(f"\nYour current task is: {currentTask['description']} (Status: {currentTask['status']})")
    kindOption = cmd.ask_options()
    if kindOption == "1": # Approve Task
        currentTask['status'] = "In Progress"
        tm.update_task_by_id(cPlan, currentTask['id'], {'status': currentTask['status']})
        ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
        ioutils.save_current_task(userGoal, currentTask)
        return currentTask
    elif kindOption == "2": # Modify Task
        cmd.system_message("Modify the task description")
        currentTask['description'] = cmd.prompt_user_input("Please input your new task description: ")
        tm.update_task_by_id(cPlan, currentTask['id'], {'description': currentTask['description']})
        ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
        return manage_task(userGoal, cPlan, currentTask)
    elif kindOption == "3": # Skip Task
        index = currentTask['id']
        currentTask['status'] = "Skipped"
        tm.update_task_by_id(cPlan, currentTask['id'], {'status': currentTask['status']})
        ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
        currentTask = tm.get_task(plan=cPlan[1], index=index)
        return manage_task(userGoal, cPlan, currentTask)
    return currentTask
    
if __name__ == "__main__":
    main()
