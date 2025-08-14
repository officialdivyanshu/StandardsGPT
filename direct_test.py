import requests
import json

# Your OpenRouter API key
API_KEY = "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"

# API endpoint
url = "https://openrouter.ai/api/v1/chat/completions"

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:5000",
    "X-Title": "StandardsGPT-DirectTest"
}

# Request payload
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "Hello, this is a test"}
    ]
}

try:
    print("Sending request to OpenRouter API...")
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print("\n=== Response ===")
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print("\nResponse Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
        
except Exception as e:
    print("\n=== Error ===")
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    
    if hasattr(e, 'response') and e.response is not None:
        print(f"\nResponse Status Code: {e.response.status_code}")
        print("Response Headers:")
        for key, value in e.response.headers.items():
            print(f"  {key}: {value}")
        print("\nResponse Body:")
        try:
            print(json.dumps(e.response.json(), indent=2))
        except:
            print(e.response.text)
