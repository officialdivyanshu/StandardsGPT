import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('OPENROUTER_API_KEY')

print(f"OpenRouter API Key: {'*' * 8 + api_key[-4:] if api_key else 'Not found'}")
print(f"Key length: {len(api_key) if api_key else 0} characters")

# Check if the key is the default placeholder
if not api_key or 'your_' in api_key:
    print("\nWARNING: The API key appears to be a placeholder or is missing!")
    print("Please update your .env file with a valid OpenRouter API key.")
else:
    print("\nAPI key appears to be properly set.")
