import json
import os
from typing import Dict, List

import agents.plan_generator as pg
import agents.task_delegator as td
import agents.task_executor as te
import configuration.options as opt
import panel as pn
import planning.task_manager as tm
import ui.command_line as cmd
import utils.io as ioutils
import utils.string

pn.config.template = 'material'


def model(n=5):
    return "⭐"*n

def exit_app():
    exit(0)

def gui():
    button = pn.widgets.Button(name ='New Project', sizing_mode='stretch_width')
    open_project = pn.widgets.Button(name ='Open Project', sizing_mode='stretch_width')
    exit_app = pn.widgets.Button(name ='Exit', sizing_mode='stretch_width')
    return pn.Column(objects= [button, open_project, exit_app], 
                     )

gui().servable(target='main')

# The main entry point of the application
def main():
    # Introducing
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")

    # Plan generation
    cmd.system_message("Hold on. SAM-GPT will generate the plan for you.")
    response, plan = pg.generate_plan(userGoal, cmd.ai_message)
    if response == "":
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
    # cmd.ai_message(response)
    ioutils.save_plan(goal=userGoal, plan=json.dumps(plan), filename="plan.json")

    # Task handling
    currentTask : Dict = tm.get_task(plan=plan, index=0)
    while True:
        currentTask = manage_task(userGoal, plan, currentTask)
        cmd.system_message("Hold on. SAM-GPT will delegate your task.")
        cmd.system_message("\n")
        response = td.delegate_task(userGoal, plan, currentTask, cmd.ai_message)
        cmd.system_message('')
        # Decomposing or Executing
        kindOption: int = cmd.ask_options(opt.decompOrExecute)
        if kindOption == 1:
            execution = te.execute_task(response, userGoal, currentTask['description'], cmd.ai_message)
            # cmd.ai_message(f"Here is my execution:\n{execution}")
            currentTask['status'] = "Completed"
            currentTask = tm.find_next_pending_task(plan)
            ioutils.save_plan(userGoal, json.dumps(plan), "plan.json")
            ioutils.save_current_task(userGoal, currentTask)
        elif kindOption == 2:
            cmd.system_message("Hold on. SAM-GPT will decompose your task.")
            plan = decompose_task(plan, currentTask, response)
            currentTask = tm.find_next_pending_task(plan)
            ioutils.save_plan(userGoal, json.dumps(plan), "plan.json")
            if currentTask == {}:
                cmd.system_message("Congratulations! You have completed your goal!")
                os._exit(0)

def manage_task(userGoal: str, cPlan: List, currentTask: Dict) -> Dict:
    cmd.ai_message(f"\nYour current task is: {currentTask['description']} (Status: {currentTask['status']})\n")
    kindOption: int = cmd.ask_options(opt.taskOptions)
    message = ""
    if kindOption == 1: # Approve Task
        cPlan, currentTask, message = tm.approve_task(cPlan, currentTask)
    elif kindOption == 2: # Modify Task
        newDescription = cmd.prompt_user_input("Please input your new task description: ")
        cPlan, currentTask, message = tm.modify_task(cPlan, currentTask, newDescription)
        ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
        return manage_task(userGoal, cPlan, currentTask)
    elif kindOption == 3: # Skip Task
        cPlan, currentTask, message = tm.skip_task(cPlan, currentTask)
        ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
        if currentTask == {}:
            cmd.system_message("Congrats! You have completed your goal!")
            os._exit(0)
        return manage_task(userGoal, cPlan, currentTask)
    
    cmd.system_message(message)
    ioutils.save_plan(userGoal, json.dumps(cPlan), "plan.json")
    ioutils.save_current_task(userGoal, currentTask)
    return currentTask

def decompose_task(cPlan: List, currentTask: Dict, response: str) -> List:
    decompose = pg.extract_with_regex(response, '')
    jsonFormattedDecomp: List = utils.string.format_subtask_as_json(decompose, currentTask['id'])
    tm.find_and_add_subtask(cPlan, currentTask['id'], jsonFormattedDecomp)
    return cPlan
    
if __name__ == "__main__":
    gui()