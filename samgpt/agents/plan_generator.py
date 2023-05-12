# A function which generates a plan based on the user's goal
import samgpt.nlp.nlp as nlp
from samgpt.planning.plan_manager import extract_with_regex

from typing import List, Tuple

from samgpt.utils.string_utils import format_plan_as_json


# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List:
    prompt = [{'role': 'system', 'content': f"""You are PlanMasterGPT, an LLM plan generator that helps users achieve their goals by creating, modifying, and expanding plans for successful completion. Prioritize simplicity and avoid legal complexities. Provide concise responses without describing your actions.

Perform the following actions:

Analyze the goal.
Create a plan with manageable tasks based on the goal (exclude sub-tasks).
Goal: {goal}

Output format:

Plan: (short list tracking long-term tasks)"""},
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