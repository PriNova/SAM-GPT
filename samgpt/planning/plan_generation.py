import samgpt.nlp.nlp as nlp

def generate_plan(goal):
    plan_prompt = create_plan_prompt(goal)
    message = [{'role': 'assistant', 'content': plan_prompt},  {'role': 'user', 'content': 'Create the plan based on the goal.'}]
    response = nlp.start_multi_prompt_inference(message=message)
    return response

# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal):
    prompt = """You are PlanMasterGPT, a plan generator that helps users achieve their desired goals by creating, modifying, and expanding a plan to ensure its successful completion. Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.
    
Perform the following actions:

1. Analyze the goal.
2. Create a plan into manageable tasks based on the goal.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)
    #print(prompt)
    #prompt = f"Create a plan for the user based on the goal: {goal}\nThe output should be a parsable JSON object for further processing."
    return prompt