from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import re
import logging
import traceback
import requests
import json

# Import configuration
from config import OPENROUTER_API_KEY, DEFAULT_MODEL, HOST, PORT, DEBUG

# Debug: Print configuration
print("\n=== Configuration ===")
print(f"Using model: {DEFAULT_MODEL}")
print(f"Server running on: http://{HOST}:{PORT}")
print("===================\n")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'openai/gpt-3.5-turbo')

# Debug: Print environment variables
print("\n=== Environment Variables ===")
print(f"OPENROUTER_API_KEY: {'*' * 8 + OPENROUTER_API_KEY[-4:] if OPENROUTER_API_KEY else 'Not set'}")
print(f"DEFAULT_MODEL: {DEFAULT_MODEL}")
print("==========================\n")

if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_openrouter_api_key_here':
    print("\n!!! WARNING: OpenRouter API key is not properly configured in .env file !!!\n")
    error_msg = "OpenRouter API key not found in environment variables"
    logger.error(error_msg)
    raise ValueError(error_msg)


# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers for OpenRouter API
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-site.com",  # Optional, for analytics
    "X-Title": "StandardsGPT"  # Optional, for analytics
}

app = Flask(__name__, static_folder='.', static_url_path='')

# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Set configuration from config.py
app.config['OPENROUTER_API_KEY'] = OPENROUTER_API_KEY
app.config['DEFAULT_MODEL'] = DEFAULT_MODEL

def generate_structured_prompt(user_input):
    """
    Generate a prompt that encourages structured, point-wise responses.
    """
    return f"""You are a helpful AI assistant. Please provide a clear, structured, and concise response to the following query.
    Format your response in a point-wise manner if possible, using bullet points (-) for each point.
    Keep each point brief and to the point. If providing steps, number them.
    
    Query: {user_input}
    
    Response:"""

@app.route('/env')
def show_env():
    import os
    return {
        'OPENROUTER_API_KEY': f"{os.environ.get('OPENROUTER_API_KEY', 'Not found')[:10]}...",
        'DEFAULT_MODEL': os.environ.get('DEFAULT_MODEL', 'Not found'),
        'FLASK_ENV': os.environ.get('FLASK_ENV', 'Not set')
    }

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Add a catch-all route to serve the index.html for all other routes
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Log the incoming request
        logger.info(f"Incoming request: {request.json}")
        
        # Get user input from request
        data = request.get_json()
        if not data or 'message' not in data:
            logger.error("Invalid request: No message in request")
            return jsonify({"error": "No message provided"}), 400
            
        user_input = data['message'].strip()
        if not user_input:
            logger.error("Invalid request: Empty message")
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Generate a prompt that encourages structured responses
        system_prompt = """You are a helpful AI assistant. Provide clear, structured, and concise responses.
        Use bullet points (-) for each main point and number steps when providing instructions.
        Keep responses brief and to the point."""
        
        logger.info("Calling OpenRouter API...")
        
        try:
            logger.info("Sending request to OpenRouter API...")
            logger.info(f"Using model: {DEFAULT_MODEL}")
            logger.info(f"User input: {user_input[:200]}...")  # Log first 200 chars of input
            
            # Prepare request data
            request_headers = {
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'http://localhost:5000',
                'X-Title': 'StandardsGPT'
            }
            
            request_data = {
                'model': DEFAULT_MODEL,
                'messages': [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_input}
                ],
                'temperature': 0.7
            }
            
            logger.info(f"Request headers: {request_headers}")
            logger.info(f"Request data: {request_data}")
            
            # Call OpenRouter API
            response = requests.post(
                'https://openrouter.ai/api/v1/chat/completions',
                headers=request_headers,
                json=request_data,
                timeout=30
            )
            
            logger.info(f"OpenRouter API response status: {response.status_code}")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            # Log the raw response for debugging
            logger.info(f"Raw response content: {response.text}")
            
            try:
                result = response.json()
                logger.info(f"Parsed response: {json.dumps(result, indent=2)[:500]}...")
                
                # Check for errors in the response
                if 'error' in result:
                    error_msg = f"OpenRouter API error: {result.get('error', {}).get('message', 'Unknown error')}"
                    logger.error(error_msg)
                    return jsonify({"error": error_msg}), 500
                
                # Extract the response content
                if 'choices' in result and result['choices'] and 'message' in result['choices'][0]:
                    reply = result['choices'][0]['message']['content']
                    return jsonify({"reply": reply})
                else:
                    error_msg = f"Unexpected response format: {json.dumps(result, indent=2)[:1000]}"
                    logger.error(error_msg)
                    return jsonify({"error": "Unexpected response format from AI service"}), 500
                    
            except json.JSONDecodeError as e:
                error_msg = f"Failed to parse API response: {str(e)}\nResponse: {response.text}"
                logger.error(error_msg)
                return jsonify({"error": "Failed to parse AI service response"}), 500
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP Error: {str(http_err)}")
            logger.error(f"Response content: {http_err.response.text if hasattr(http_err, 'response') else 'No response'}")
            logger.error(f"Status code: {http_err.response.status_code if hasattr(http_err, 'response') else 'N/A'}")
            logger.error(f"Response headers: {dict(http_err.response.headers) if hasattr(http_err, 'response') and hasattr(http_err.response, 'headers') else 'N/A'}")
            error_msg = f"OpenRouter API HTTP Error: {str(http_err)}"
            if hasattr(http_err, 'response') and http_err.response is not None:
                error_msg += f"\nStatus Code: {http_err.response.status_code}"
                error_msg += f"\nResponse Text: {http_err.response.text}"
                error_msg += f"\nHeaders: {dict(http_err.response.headers)}"
            logger.error(error_msg)
            return jsonify({"error": f"AI service error: {str(http_err)}"}), 500
            
        except Exception as e:
            error_msg = f"Error processing request: {str(e)}"
            logger.error(error_msg)
        
    except Exception as e:
        logger.exception("Unexpected error in chat endpoint")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        logger.info("Starting StandardsGPT server with OpenRouter integration")
        logger.info(f"Using model: {DEFAULT_MODEL}")
        
        app.run(debug=DEBUG, port=PORT, host=HOST)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
        raise
