import json
import os
from typing import Dict, List

import agents.plan_generator as pg
import agents.task_delegator as td
import agents.task_executor as te
import configuration.options as opt

import planning.task_manager as tm
import ui.command_line as cmd
import utils.io as ioutils
import utils.string
import os as timer

import panel as pn
pn.config.template = 'material'
pn.extension('floatpanel')

def create_project():
    return pn.Row(
        pn.widgets.StaticText(value="Project Name: "),
        pn.widgets.TextInput(placeholder="Type the project name here", sizing_mode='stretch_width'),
    )


def new_project(column: pn.Column):
    def on_click(event):
        column.objects.
        for child in column:
            if (
                isinstance(child, pn.FloatPanel)
                and child.id != 'new_project_modal'
            ):
                modal = pn.layout.FloatPanel(
                    pn.widgets.TextInput(name='Project Name'),
                    pn.widgets.Button(name='OK', button_type='primary'),
                    title='New Project',
                    width=400,
                    height=200,
                    contained = True,
                    id='new_project_modal'
                )
                column.append(modal)
    return on_click


def start_screen():
    coloumn = pn.WidgetBox()
    new_project_button = pn.widgets.Button(name ='New Project', sizing_mode='stretch_width')
    new_project_button.on_click(new_project(coloumn))
    open_project = pn.widgets.Button(name ='Open Project', sizing_mode='stretch_width')
    exit_app = pn.widgets.Button(name ='Exit', sizing_mode='stretch_width')
    coloumn.extend(objects= [new_project_button, open_project, exit_app])
    return coloumn

def gui():
    return start_screen()

gui().servable(target='main')
#pn.serve(gui, title="Sam-GPT", threaded=True, port=3333)
def introducing() -> str:
    cmd.system_message("Welcome to SAM-GPT!")
    userGoal: str = cmd.prompt_user_input("Please input your goal: ")
    cmd.system_message(f"Your goal: {userGoal}")
    return userGoal

def generate_plan(userGoal: str) -> List | None:
    # Plan generation
    cmd.system_message("Hold on. SAM-GPT will generate the plan for you.")
    response, plan = pg.generate_plan(userGoal, cmd.ai_message)
    if response == "":
        cmd.system_message("Sorry, SAM-GPT cannot generate a plan for you.")
        return None
    # cmd.ai_message(response)
    ioutils.save_plan(goal=userGoal, plan=json.dumps(plan), filename="plan.json")
    return plan

# The main entry point of the application
def main():
    userGoal = introducing()
    if plan := generate_plan(userGoal=userGoal):
        currentTask : Dict = tm.get_task(plan=plan, index=0)
        while True:
            currentTask = manage_task(userGoal, plan, currentTask)
            cmd.system_message("Hold on. SAM-GPT will delegate your task.")
            cmd.system_message("\n")
            response = td.delegate_task(userGoal, plan, currentTask, cmd.ai_message)
            cmd.system_message('')
            
            task_option: int = cmd.ask_options(opt.decompOrExecute)
            if task_option == 1:
                # Execute the current task
                execution = te.execute_task(response, userGoal, currentTask['description'], cmd.ai_message)
                # cmd.ai_message(f"Here is my execution:\n{execution}")
                currentTask['status'] = "Completed"
                currentTask = tm.find_next_pending_task(plan)
                ioutils.save_plan(userGoal, json.dumps(plan), "plan.json")
                ioutils.save_current_task(userGoal, currentTask)
            elif task_option == 2:
                # Decompose the current task
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
    pn.config.template = 'material'
    gui().show(target='main', port=3333)
    #pn.serve(gui, title="Sam-GPT", threaded=True, port=3333, kwargs={"autoreload": True})