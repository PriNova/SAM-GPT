from samgpt.nlp.nlp import start_multi_prompt_inference
import samgpt.ui.command_line as cmd

from typing import List
import dotenv
import requests
import re
import json

def execute(userGoal: str, currentTaskDescription: str) -> str:
    cmd.ai_message(f"Determine web search query for task: {currentTaskDescription}")
    prompt = create_search_prompt(userGoal, currentTaskDescription)
    response = start_multi_prompt_inference(prompt)
    print(response)
    
    query = ""
    match response.split():
        case ["Query:", *_]:
            query = response[5:-1]
        case _:
            query = ""

    print(f"Query: {query}")
    if query:
        make_web_request(query)
    return query

def make_web_request(query: str):
    bing_api = dotenv.get_key(".env", "BING_API")
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers:  dict = {"Ocp-Apim-Subscription-Key": bing_api}
    params = {"q": query, "count": 6, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Extract the search result items from the response
    web_pages = search_results.get("webPages", {})
    search_results = web_pages.get("value", [])

    # Create a list of search result dictionaries with 'title', 'href', and 'body' keys
    search_results_list = [
        {
            "title": clean_text(item["name"]),
            "href": item["url"],
            "body": clean_text(item["snippet"]),
        }
        for item in search_results
    ]
    return json.dumps(search_results_list, ensure_ascii=False, indent=4)

def clean_text(text: str) -> str:
    cleaned_text = re.sub("<[^>]*>", "", text)  # Remove HTML tags
    cleaned_text = cleaned_text.replace(
        "\\n", " "
    )  # Replace newline characters with spaces
    return cleaned_text

def create_search_prompt(userGoal: str, currentTaskDescription: str) -> List:
    prompt = [{'role': 'assistant', 'content': f"""You are WebQueryGPT, a query generation engine, which helps to define the best search query with all relevant keywords to find the most accurate and efficiently search results from a google search.

Perform the following actions:

1. Determine the perfect fit search query based on the goal and the task description delimited by triple backticks for a google search.

```
Goal: {userGoal}
Task: {currentTaskDescription}
```

Do not explain or start a conversation. Reply only with the perfect fit search query as follows:

Query: (qery)
"""},
{'role': 'user', 'content': 'Reply with the perfect fit search query for a google search. Only provide the output in the format given'}]
    return prompt