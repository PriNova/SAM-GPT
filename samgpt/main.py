import samgpt.ui.command_line as cmd
import samgpt.planning.task_manager as tm
import samgpt.agents.task_delegator as td
import samgpt.agents.plan_generator as pg
import samgpt.utils.io_utils as ioutils

from typing import List, Dict, Tuple
import json
import os

import samgpt.utils.string_utils

# The main entry point of the application
def main() -> None:

    # Introducing
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")

    # Plan generation
    cmd.system_message(f"Hold on. SAM-GPT will generate the plan for you.")
    response, plan = pg.generate_plan(userGoal)
    if response == "":
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
    cmd.ai_message(response)
    ioutils.save_plan(goal=userGoal, plan=json.dumps(plan), filename="plan.json")

    # Task handling
    currentTask : Dict = tm.get_task(plan=plan, index=0)
    while True:
        currentTask = manage_task(userGoal, plan, currentTask)
        cmd.system_message("Hold on. SAM-GPT will delegate your task.")
        response = td.delegate_task(userGoal, currentTask)
        cmd.ai_message(f"Here is my response:\n{response}")

        # Decomposing or Executing
        kindOption: int = cmd.ask_options(cmd.decompOrExecute)
        if kindOption == 1: # Decompose
            cmd.system_message("Hold on. SAM-GPT will decompose your task.")
            plan = decompose_task(plan, currentTask, response)
            currentTask = tm.find_next_pending_task(plan)
            ioutils.save_plan(userGoal, json.dumps(plan), "plan.json")
            if currentTask == {}:
                cmd.system_message("Congratulations! You have completed your goal!")
                os._exit(0)
        if kindOption == 2: # Execute
            currentTask['status'] = "Completed"
            tm.find_and_update_task(plan, currentTask['id'], {'status': currentTask['status']})
            currentTask = tm.find_next_pending_task(plan)
            ioutils.save_plan(userGoal, json.dumps(plan), "plan.json")
            ioutils.save_current_task(userGoal, currentTask)

def manage_task(userGoal: str, cPlan: List, currentTask: Dict) -> Dict:
    cmd.ai_message(f"\nYour current task is: {currentTask['description']} (Status: {currentTask['status']})\n")
    kindOption: int = cmd.ask_options(cmd.taskOptions)
    message = ""
    if kindOption == 1: # Approve Task
        cPlan, currentTask, message = tm.approve_task(cPlan, currentTask)
    elif kindOption == 2: # Modify Task
        newDescription = cmd.prompt_user_input("Please input your new task description: ")
        cPlan, currentTask, message = tm.modify_task(cPlan, currentTask, newDescription)
        return manage_task(userGoal, cPlan, currentTask)
    elif kindOption == 3: # Skip Task
        cPlan, currentTask, message = tm.skip_task(cPlan, currentTask)
        if currentTask == {}:
            cmd.system_message("Congratulations! You have completed your goal!")
            os._exit(0)
        return manage_task(userGoal, cPlan, currentTask)
    
    cmd.system_message(message)
    ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
    ioutils.save_current_task(userGoal, currentTask)
    return currentTask

def decompose_task(cPlan: List, currentTask: Dict, response: str) -> List:
    print(currentTask['id'])
    decompose = pg.extract_with_regex(response, '')
    print(decompose)
    jsonFormattedDecomp: List = samgpt.utils.string_utils.format_subtask_as_json(decompose, currentTask['id'])
    print(jsonFormattedDecomp)
    tm.find_and_add_subtask(cPlan, currentTask['id'], jsonFormattedDecomp)
    return cPlan
    
if __name__ == "__main__":
    main()
