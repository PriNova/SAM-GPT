import os
import re
import samgpt.nlp.nlp as nlp
import samgpt.utils.io_utils as ioutils
from typing import List

# A function which generates a plan based on the user's goal
def generate_plan(goal):
    plan_prompt = create_plan_prompt(goal)
    message = [{'role': 'assistant', 'content': plan_prompt},  {'role': 'user', 'content': 'Create the plan based on the goal.'}]
    response = nlp.start_multi_prompt_inference(message=message)
    extracted_plan = extract_plan_with_regex(response)
    folder = 'plans'
    if not extracted_plan:
        return response
    if not os.path.exists(folder):
        ioutils.create_folder(folder)
    save_plan(extracted_plan, folder, f"plan.txt")
    return response
    

# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal):
    prompt = """You are PlanMasterGPT, a plan generator that helps users achieve their desired goals by creating, modifying, and expanding a plan to ensure its successful completion. Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.
    
Perform the following actions:

1. Analyze the goal.
2. Create a plan into manageable tasks based on the goal. Do not include sub-tasks.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)
    #print(prompt)
    #prompt = f"Create a plan for the user based on the goal: {goal}\nThe output should be a parsable JSON object for further processing."
    return prompt

# extract the plan from text
def extract_plan_with_regex(text):
    # Match numbered lists
    match = re.search(r'Plan:\n((?:\d+\..+\n)+)', text)  # corrected regex pattern
    if match:
        plan = re.sub(r'\n?\d+\..', '\n', match.group(1)).strip()
        return plan.strip()

    # Match bulletted lists
    match = re.search(r'Plan:\n((?:•\s*.+\n)+)', text)
    if match:
        plan = re.sub(r'(•\s*)', '', match.group(1)).strip()
        return plan.strip()

    # Match lined lists
    match = re.search(r'Plan:\n((?:-\s*.+\n)+)', text)
    if match:
        plan = re.sub(r'(-\s*)', '', match.group(1)).strip()
        return plan.strip()
    
    match = re.search(r'Plan:\n([\s\S]*?)', text)
    if match:
        plan = match.group(1).strip()
        return plan.strip()

    # No matching pattern found
    return 'No plan created'
    
# Function to save the plan to a file in a specified order. If file already exists, it will be overwritten.
def save_plan(plan, folder, filename):
    with open(f"{folder}/{filename}", "w") as f:
        f.write(plan)
    return f"{folder}/{filename}"

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")