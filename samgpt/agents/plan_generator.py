# A function which generates a plan based on the user's goal
import samgpt.nlp.nlp as nlp
from samgpt.planning.plan_manager import extract_plan_with_regex, format_as_json

from typing import List, Optional


# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List[dict[str, str]]:
    prompt = [{'role': 'system', 'content': """You are PlanMasterGPT, a plan generator that helps users achieve their desired goals by creating, modifying, and expanding a plan to ensure its successful completion. Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.
    
Perform the following actions:

1. Analyze the goal.
2. Create a plan into manageable tasks based on the goal. Do not include sub-tasks.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)},
{'role': 'user', 'content': 'Create the plan based on the goal.'}]
    return prompt


def generate_plan(goal) -> Optional[List[str]|None]:
    planPrompt = create_plan_prompt(goal)
    response = nlp.start_multi_prompt_inference(message=planPrompt)
    extractedPlan = extract_plan_with_regex(response)
    jsonFormattedPlan = format_as_json(extractedPlan)
    
    if not extractedPlan:
        return None

    return [response, jsonFormattedPlan]