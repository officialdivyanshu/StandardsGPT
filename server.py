from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
import re
import logging
import traceback
import requests
import json
from dotenv import load_dotenv

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

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_openrouter_api_key_here':
    error_msg = "OpenRouter API key not found in environment variables"
    logger.error(error_msg)
    raise ValueError(error_msg)

# Default model to use (can be overridden per request)
DEFAULT_MODEL = "openai/gpt-3.5-turbo"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers for OpenRouter API
OPENROUTER_HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-site.com",  # Optional, for analytics
    "X-Title": "StandardsGPT"  # Optional, for analytics
}

app = Flask(__name__, static_folder='.', static_url_path='')

# Simple CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

def generate_structured_prompt(user_input):
    """
    Generate a prompt that encourages structured, point-wise responses.
    """
    return f"""You are a helpful AI assistant. Please provide a clear, structured, and concise response to the following query.
    Format your response in a point-wise manner if possible, using bullet points (-) for each point.
    Keep each point brief and to the point. If providing steps, number them.
    
    Query: {user_input}
    
    Response:"""

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
        logger.info("Received request with data: %s", request.get_data())
        
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({"error": "No data provided"}), 400
            
        user_input = data.get("message", "").strip()
        if not user_input:
            logger.error("Empty message received")
            return jsonify({"error": "Please provide a valid message."}), 400
        
        logger.info("Processing message: %s", user_input)
        
        # Generate a prompt that encourages structured responses
        system_prompt = """You are a helpful AI assistant. Provide clear, structured, and concise responses.
        Use bullet points (-) for each main point and number steps when providing instructions.
        Keep responses brief and to the point."""
        
        # Call OpenRouter API
        logger.info("Calling OpenRouter API...")
        try:
            payload = {
                "model": DEFAULT_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                OPENROUTER_API_URL,
                headers=OPENROUTER_HEADERS,
                json=payload
            )
            response.raise_for_status()
            
            response_data = response.json()
            reply = response_data['choices'][0]['message']['content'].strip()
            logger.info("Successfully got response from OpenRouter")
            
            return jsonify({"reply": reply})
            
        except requests.exceptions.HTTPError as http_err:
            error_msg = f"OpenRouter API HTTP Error: {str(http_err)}"
            if hasattr(http_err, 'response') and http_err.response.text:
                error_msg += f"\nResponse: {http_err.response.text}"
            logger.error(error_msg)
            return jsonify({"error": "Error processing your request with the AI service"}), 500
            
        except Exception as e:
            error_msg = f"OpenRouter API Error: {str(e)}"
            logger.error(error_msg)
        
    except Exception as e:
        logger.exception("Unexpected error in chat endpoint")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    try:
        # Verify OpenRouter API key is set
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == 'your_openrouter_api_key_here':
            raise RuntimeError("OpenRouter API key not properly configured")
            
        logger.info("Starting StandardsGPT server with OpenRouter integration")
        logger.info(f"Using model: {DEFAULT_MODEL}")
        
        app.run(debug=True, port=5000, host='0.0.0.0')
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
        raise
