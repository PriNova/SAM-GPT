import os
import re
import samgpt.nlp.nlp as nlp
import samgpt.utils.io_utils as ioutils
from typing import List


# A function which generates a plan based on the user's goal
def generate_plan(goal) -> str:
    plan_prompt = create_plan_prompt(goal)
    response = nlp.start_multi_prompt_inference(message=plan_prompt)
    extracted_plan = extract_plan_with_regex(response)
    
    if not extracted_plan:
        return f"No plan generated with respone:\n{response}"
    
    ioutils.save_plan(goal, extracted_plan, f"plan.txt")
    return response
    

# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List[dict[str, str]]:
    prompt = [{'role': 'assistant', 'content': """You are PlanMasterGPT, a plan generator that helps users achieve their desired goals by creating, modifying, and expanding a plan to ensure its successful completion. Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.
    
Perform the following actions:

1. Analyze the goal.
2. Create a plan into manageable tasks based on the goal. Do not include sub-tasks.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)},
{'role': 'user', 'content': 'Create the plan based on the goal.'}]
    return prompt

# extract the plan from text
def extract_plan_with_regex(text) -> str:
    # Match numbered lists
    match = re.search(r'Plan:\n+((?:\d+.+\n?)+)', text)  # corrected regex pattern
    if match:
        plan = re.sub(r'\n?\d+\..', '\n', match.group(1)).strip()
        return plan.strip()

    # Match bulletted lists
    match = re.search(r'Plan:\n+((?:•\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(•\s*)', '', match.group(1)).strip()
        return plan.strip()

    # Match lined lists
    match = re.search(r'Plan:\n+((?:-\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(-\s*)', '', match.group(1)).strip()
        return plan.strip()
    
    match = re.search(r'Plan:\n+([\s\S]*?)', text)
    if match:
        plan = match.group(1).strip()
        return plan.strip()

    # No matching pattern found
    return 'No plan created'
    
# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")