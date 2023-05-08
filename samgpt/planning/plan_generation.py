import re
import json
import samgpt.nlp.nlp as nlp
import samgpt.utils.io_utils as ioutils
from typing import List, Optional, Dict


# A function which generates a plan based on the user's goal
def generate_plan(goal) -> Optional[List[str]|None]:
    planPrompt = create_plan_prompt(goal)
    response = nlp.start_multi_prompt_inference(message=planPrompt)
    extractedPlan = extract_plan_with_regex(response)
    jsonFormattedPlan = formatAsJson(extractedPlan)
    if not extractedPlan:
        return None

    return [response, jsonFormattedPlan]
    

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

# Format extracted plan as a JSON Object.
def formatAsJson(extractedPlan: str) -> str:
    # Split the output into tasks using newline character
    tasks = extractedPlan.strip().split("\n")

    # Create a list of dictionaries for each task
    plan = [
        {
            "id": i + 1,
            "description": task,
            "status": "pending",
            "subtasks": []
        }
        for i, task in enumerate(tasks)
    ]
    plan_json = json.dumps(plan, indent=4)
    return plan_json