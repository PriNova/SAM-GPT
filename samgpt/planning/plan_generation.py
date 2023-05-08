import samgpt.nlp.nlp as nlp

def generate_plan(goal):
    plan_prompt = create_plan_prompt(goal)
    response = nlp.start_inference(role = "assistant", prompt = plan_prompt)
    return response

# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal):
    prompt = """Perform the following actions:

1. Analyze the goal.
2. Create a plan into managable tasks based on the goal.

Goal: {}

Explicitly format the output as follows:

Plan: (short list that tracks long-term tasks)""".format(goal)
    #print(prompt)
    #prompt = f"Create a plan for the user based on the goal: {goal}\nThe output should be a parsable JSON object for further processing."
    return prompt