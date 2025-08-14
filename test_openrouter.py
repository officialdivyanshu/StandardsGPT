import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"Testing API key: {API_KEY[:10]}...")

# Test the key with a simple request
url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello, this is a test"}
    ]
}

try:
    print("Sending request to OpenRouter API...")
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())
    
except Exception as e:
    print(f"Error: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response Status: {e.response.status_code}")
        print(f"Response Text: {e.response.text}")
