from samgpt.nlp.nlp import start_multi_prompt_inference
import samgpt.ui.command_line as cmd

from typing import List

def execute(userGoal: str, currentTaskDescription: str) -> str:
    cmd.ai_message(f"Determine web search query for task: {currentTaskDescription}")
    prompt = create_search_prompt(userGoal, currentTaskDescription)
    response = start_multi_prompt_inference(prompt)
    return response

def create_search_prompt(userGoal: str, currentTaskDescription: str) -> List:
    prompt = [{'role': 'assistant', 'content': f"""You are WebQueryGPT, a query generation engine, which helps to define the best search query with all relevant keywords to find the most accurate and efficiently search results from a google search.

Perform the following actions:

1. Determine the perfect fit search query based on the goal and the task description delimited by triple backticks for a google search.

```
Goal: {userGoal}
Task: {currentTaskDescription}

Reply only with the perfect fit search query as follows:

Query: (qery)
"""},
{'role': 'user', 'content': 'Reply with the perfect fit search query for a google search. Only provide the output in the format given'}]
    return prompt