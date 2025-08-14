import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('OPENROUTER_API_KEY')

print(f"Testing API key: {API_KEY[:10]}...")

# Test the key with a simple request
url = "https://openrouter.ai/api/v1/auth/key"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

try:
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(response.json())
except Exception as e:
    print(f"Error: {str(e)}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"Response Status: {e.response.status_code}")
        print(f"Response Text: {e.response.text}")
