"""This module contains the functions used to interact with the NLP model"""

from typing import List, Dict, Optional, Any
import requests
import json
import dotenv

defaultChatConfig: Dict[str, Any] = { # type: ignore
    "model": 'gpt-3.5-turbo',
    "max_tokens": 1000,
    "temperature": 1,
    "presence_penalty": 0.0,
    "top_p": 1,
    "frequency_penalty": 0,
    "stream": True
}

OPENAI_API_KEY : Optional[str] = dotenv.get_key('.env', 'OPENAI_API_KEY')

openaiModel: List[Any] = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
freeModel: List[Any] = ['https://free.churchless.tech/v1/chat/completions', '']

# define the Model enum
Model: Dict[str, List[Any]] = {
    'openai': openaiModel,
    'free': freeModel
    }

# Get the model from the Model enu
model: List[Any] = Model['free']

# Get the chat completion from the model
import requests
import json
from typing import List, Dict, Any, Callable

def get_chat_completion(model: List[Any], messages: List[Dict[str, str]], config: Dict[str, Any], callback: Callable[[str], None]) -> str:
    headers = get_headers(model[1])
    body = get_body(messages, config)

    
    response = send_request(model[0], headers, body)
    #response.raise_for_status()

    text = ""
    for line in response.iter_lines(chunk_size=1, decode_unicode=True):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            content = get_content(data)
            text += content
            callback(content)
            if is_stream_ended(data):
                break

    return text

def get_headers(token: str) -> Dict[str, str]:
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

def get_body(messages: List[Dict[str, str]], config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'messages': messages,
        **config
    }

def send_request(url: str, headers: Dict[str, str], body: Dict[str, Any]) -> requests.Response:
    repeat = 5
    while repeat > 0:
        try:
            response = requests.post(url, headers=headers, data=json.dumps(body))
            if response.status_code == 200:
                return response
        except requests.exceptions.RequestException:
            pass
        repeat -= 1
    return requests.Response()

def get_content(data: Dict[str, Any]) -> str:
    return data['choices'][0]['delta'].get('content', '')

def is_stream_ended(data: Dict[str, Any]) -> bool:
    return data['choices'][0]['finish_reason'] is not None

# Start the inference
def start__simple_inference(role, prompt, callback) -> str:
    response = get_chat_completion(model=model, messages=[{'role': role, 'content': prompt}], config=defaultChatConfig, callback=callback)
    return response

def start_multi_prompt_inference(message, callback) -> str:
    response = get_chat_completion(model=model, messages= message, config=defaultChatConfig, callback=callback)
    return response