import os
from dotenv import load_dotenv
from flask import Flask, jsonify

app = Flask(__name__)

# Load environment variables
load_dotenv()

@app.route('/env')
def show_env():
    return jsonify({
        'OPENROUTER_API_KEY': os.environ.get('OPENROUTER_API_KEY', 'Not found'),
        'DEFAULT_MODEL': os.environ.get('DEFAULT_MODEL', 'Not found')
    })

if __name__ == "__main__":
    print("Starting test server on http://localhost:5001")
    print(f"OPENROUTER_API_KEY: {'*' * 8 + os.environ.get('OPENROUTER_API_KEY', '')[-4:] if os.environ.get('OPENROUTER_API_KEY') else 'Not found'}")
    app.run(port=5001)
