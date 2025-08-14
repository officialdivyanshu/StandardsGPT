import os
from dotenv import load_dotenv

print("Loading environment variables...")
load_dotenv()

print(f"OPENROUTER_API_KEY: {os.environ.get('OPENROUTER_API_KEY', 'Not found')}")
print(f"DEFAULT_MODEL: {os.environ.get('DEFAULT_MODEL', 'Not found')}")

# Try to load the key directly from the .env file
from dotenv import dotenv_values
env_vars = dotenv_values()
print("\nDirectly from .env file:")
print(f"OPENROUTER_API_KEY: {env_vars.get('OPENROUTER_API_KEY', 'Not found')}")
print(f"DEFAULT_MODEL: {env_vars.get('DEFAULT_MODEL', 'Not found')}")
