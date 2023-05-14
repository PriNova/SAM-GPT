from samgpt.nlp.nlp import start_multi_prompt_inference
import samgpt.ui.command_line as cmd
from samgpt.nlp.nlp import start_multi_prompt_inference



from typing import List
import dotenv
import requests
import re
from bs4 import BeautifulSoup

def execute(userGoal: str, currentTaskDescription: str):
    cmd.ai_message(f"Determine web search query for task: {currentTaskDescription}")
    prompt = create_search_prompt(userGoal, currentTaskDescription)
    response = start_multi_prompt_inference(prompt)
    
    query = ""
    match response.split():
        case ["Query:", *_]:
            query = response[5:]
        case _:
            query = ""

    cmd.ai_message(f"Query{query}")
    contens = ""
    if query:
        contens = make_web_request2(query)
    cmd.system_message("SAM-GPT is collecting the response!")
    prompt = [{'role': 'assistant', 'content':  f"""Instructions:
1. Find the information's in the Text based on the Query.
2. If the Text contains the information for the query then reply with the exact answer.

Search Query: {query}

Text:
'''
{contens}
'''

Format your output as:
Answer: I found the answer to your query. The result is

"""}]
    response = start_multi_prompt_inference(prompt)
    cmd.ai_message(f"{response}")

def make_web_request2(query: str):
    results = []
    try:
        from googlesearch import search
        for j in search(query, tld="com", num=10, stop=5, pause=2):
            results.append(j)
    except ImportError:
        print("No module named 'google' found")
    #print(results)
    if results:
        contents = scrape_content(results)
        contents_flattened = ' '.join(contents).strip()
        return contents_flattened
    return ""

def scrape_content(results: List)-> List:
    contents = []
    for url in results:
        #try:
            response = requests.get(url)

            # parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # find all <p> tags
            paragraphs = soup.find_all('p')
            
            # extract the text from each <p> tag and add it to a new list
            page_content = ""
            char_count = 0
            for p in paragraphs:
                for char in p.text:
                    # consider spaces as visible characters
                    if not char.isspace() or char == ' ':
                        page_content += char
                        char_count += 1
                        # stop once we reach 1000 characters
                        if char_count == 2000:
                            break
                if char_count == 2000:
                    break
            page_content += "\n"

            # add the list of paragraphs to the contents list
            contents.append(page_content)
    return contents

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
    return search_results_list

def clean_text(text: str) -> str:
    cleaned_text = re.sub("<[^>]*>", "", text)  # Remove HTML tags
    cleaned_text = cleaned_text.replace(
        "\\n", " "
    )  # Replace newline characters with spaces
    return cleaned_text

def create_search_prompt(userGoal: str, currentTaskDescription: str) -> List:
    prompt = [{'role': 'assistant', 'content': f"""You are WebQueryGPT, a query generation engine, which helps to define the best search query with all relevant keywords to find the most accurate and efficiently search results from a google search.

Instructions:

1. Determine one perfect search query based on the goal and the task description delimited by triple backticks for a google search.

```
Goal: {userGoal}
Task: {currentTaskDescription}
```

Do not explain or start a conversation. Give a natural language search query. Reply only with the perfect search query as follows:

Query: (natural language search query)
"""},
{'role': 'user', 'content': 'Reply with the perfect fit search query for a google search. Only provide the output in the format given'}]
    return prompt