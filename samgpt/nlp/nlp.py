"""This module contains the functions used to interact with the NLP model"""

from typing import List, Dict, Optional
import requests
import json
import dotenv

defaultChatConfig: Dict[str, any] = { # type: ignore
    "model": 'gpt-3.5-turbo',
    "max_tokens": 1000,
    "temperature": 1,
    "presence_penalty": 0.0,
    "top_p": 1,
    "frequency_penalty": 0,
    "stream": True
}

OPENAI_API_KEY : str|None = dotenv.get_key('.env', 'OPENAI_API_KEY')

openaiModel: list = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
freeModel: list = ['https://free.churchless.tech/v1/chat/completions', '']

# define the Model enum
Model: Dict = {
    'openai': openaiModel,
    'free': freeModel
    }

# Get the model from the Model enu
model: enumerate = Model['free']

# Get the chat completion from the model
def get_chat_completion(model, messages: List[Dict[str, str]], config: Dict[str, str], callback) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {model[1]}'
    }

    body = {
        'messages': messages,
        **config
    }

    response = requests.post(model[0], headers=headers, data=json.dumps(body))
    repeat = 5
    while response.status_code != 200 and repeat > 0:
        response = requests.post(model[0], headers=headers, data=json.dumps(body))
        repeat -= 1
        
    buffer = ""
    text = ""
    for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
        buffer += chunk
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            if line.startswith('data: '):
                line = line[6:] # strip "data: " from the start of the line
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue  # skip this line if it's not valid JSON
            content = data['choices'][0]['delta'].get('content', '')
            text += content
            callback(content)
            finish_reason = data['choices'][0]['finish_reason']
            if finish_reason is not None:
                #print(f"\nStream ended due to: {finish_reason}")
                break
    return text
    #response.raise_for_status()
    data = response.json()
    #To start content_without_first_linebreaks = content[2:]
    return data['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')

# Start the inference
def start__simple_inference(role, prompt, callback) -> str:
    response = get_chat_completion(model=model, messages=[{'role': role, 'content': prompt}], config=defaultChatConfig, callback=callback)
    return response

def start_multi_prompt_inference(message, callback) -> str:
    response = get_chat_completion(model=model, messages= message, config=defaultChatConfig, callback=callback)
    return response