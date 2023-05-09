# A function which generates a plan based on the user's goal
import samgpt.nlp.nlp as nlp
from samgpt.planning.plan_manager import extract_with_regex

from typing import List, Tuple

from samgpt.utils.string_utils import format_plan_as_json


# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List:
    prompt = [{'role': 'system', 'content': """You are PlanMasterGPT, a plan generator that helps users achieve their desired goals by creating, modifying, and expanding a plan to ensure its successful completion. Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.
    
Perform the following actions:

1. Analyze the goal.
2. Create a plan into manageable tasks based on the goal. Do not include sub-tasks.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)},
{'role': 'user', 'content': 'Create the plan based on the goal.'}]
    return prompt


def generate_plan(goal) -> Tuple[str, List]:
    planPrompt = create_plan_prompt(goal)
    response: str = nlp.start_multi_prompt_inference(message=planPrompt)
    extractedPlan: str = extract_with_regex(response, "Plan:")
    jsonFormattedPlan: List = format_plan_as_json(extractedPlan)

    if not extractedPlan:
        return ("", [])
    
    return (response, jsonFormattedPlan)