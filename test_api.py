import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('OPENROUTER_API_KEY')

if not api_key:
    print("Error: OPENROUTER_API_KEY not found in environment variables")
    exit(1)

print(f"Testing connection to OpenRouter API with key: {'*' * 8 + api_key[-4:]}")

try:
    response = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'http://localhost:5000',
            'X-Title': 'StandardsGPT-Test'
        },
        json={
            'model': 'openai/gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': 'Hello, this is a test'}
            ]
        },
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print("Response:")
    print(response.json())
    
except Exception as e:
    print(f"\nError making request to OpenRouter API: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Status Code: {e.response.status_code}")
        print("Response:", e.response.text)
