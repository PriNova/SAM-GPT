# A function which generates a plan based on the user's goal
import samgpt.nlp.nlp as nlp
from samgpt.planning.plan_manager import extract_with_regex

from typing import List, Tuple

from samgpt.utils.string_utils import format_plan_as_json


# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List:
    prompt = [{'role': 'system', 'content': f"""You are PlanMasterGPT, an LLM plan generator that helps users achieve their goals by creating, modifying, and expanding plans for successful completion. Prioritize simplicity and avoid legal complexities. Provide concise responses without describing your actions.

--- Instructions:
1. Analyze the goal in a step by step way to be sure we understand the goal.
2. Create a plan into manageable tasks based on the goal and the available commands in a step by step way to be sure we apply the best task to the available commands.

--- Commands:
$webSearch: Search the web for any query or topic if you are unsure.
$createCode: Write programs in various programming languages for website creation, calculations, math tasks, applications, etc.
$editCode: Modify an existing codebase by opening and editing the source files.
$evaluateCode: Evaluate code for pure functions or augmentable outputs.
$decomposeTask: Break down a complex task into smaller, more manageable subtasks if the main task is unclear, ambiguous, too vague or an available command in this list is not sufficient.
$executeCode: Execute code.
$searchTwitter: Search for tweets on Twitter based on specific keywords, hashtags, and mentions.
$tweet: Post a message (up to 280 characters) on Twitter.
$fileCRUD: Perform file operations to create, read, update, and delete files on your local machine.
$git: Manage code repositories, track changes, and collaborate with others using Git.
$llm: Perform natural language processing tasks like text generation, translation, sentiment analysis, question answering or for generative actions.
$newCommand: Create a new customized command for specific tasks or goals if the availabe commands are not sufficient.
$humanFeedback: Ask for human feedback or input if the task is unclear, ambiguous or too vague.

--- Start Example

Goal: Open a pet shop.
Plan:
1. Research and select a suitable location for the pet shop.
2. Obtain necessary licenses and permits to operate a pet shop.
3. Develop a business plan and secure funding for the pet shop.
4. Purchase or lease equipment and supplies needed to run the pet shop.
5. Hire and train staff to assist with the daily operations of the pet shop.
6. Establish relationships with suppliers to ensure a steady supply of pet products.
7. Use an application for inventory tracking.
8. Create and deploy a website.
9. Advertise and market the pet shop to attract customers.
10. Open the pet shop and maintain a high level of customer service to ensure repeat business.

--- End Example

Explicitly format the output as follows:
Plan: (short list that tracks long-term tasks)

Goal: {goal}"""},
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