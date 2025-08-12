from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # allow frontend to talk to backend

OLLAMA_URL = "http://localhost:11434/api/generate"

def format_response(raw_response):
    """
    Format the AI's response into a structured, point-wise format.
    Handles different response styles and converts them to a consistent format.
    """
    if not raw_response:
        return "I'm sorry, I couldn't generate a response. Please try again."
    
    # Clean up the response
    response = raw_response.strip()
    
    # If response is already in point form, clean it up
    if '\n- ' in response or '\n* ' in response or '\n1. ' in response:
        # Normalize different bullet points to -
        response = re.sub(r'\n\s*[\*•]\s+', '\n- ', response)
        # Normalize numbered lists to point form
        response = re.sub(r'\n\s*\d+\.\s+', '\n- ', response)
        # Ensure proper line breaks
        response = '\n'.join(line.strip() for line in response.split('\n'))
        return response
    
    # If response contains colons that might indicate a list
    if ':' in response and '\n' in response:
        # Split by lines and format each line
        lines = response.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # If line contains a colon, format as a point
            if ':' in line and len(line.split(':', 1)[0].split()) < 5:
                formatted_lines.append(f"- {line}")
            else:
                # Otherwise, add as a regular line
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    # For very short responses, return as is
    if len(response.split()) < 20:
        return response
    
    # For longer responses, split into sentences and format as points
    sentences = re.split(r'(?<=[.!?])\s+', response)
    formatted_sentences = [f"- {sentence.strip()}" for sentence in sentences if sentence.strip()]
    
    return '\n'.join(formatted_sentences)

def generate_structured_prompt(user_input):
    """
    Generate a prompt that encourages structured, point-wise responses.
    """
    return f"""Please provide a clear, structured, and concise response to the following query.
    Format your response in a point-wise manner if possible, using bullet points (-) for each point.
    Keep each point brief and to the point. If providing steps, number them.
    
    Query: {user_input}
    
    Response:"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        
        if not user_input:
            return jsonify({"reply": "Please provide a valid message."})
        
        # Generate a prompt that encourages structured responses
        structured_prompt = generate_structured_prompt(user_input)
        
        payload = {
            "model": "phi3",
            "prompt": structured_prompt,
            "stream": False
        }

        # Make the request to the AI model
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        # Get and format the response
        raw_reply = response.json().get("response", "")
        formatted_reply = format_response(raw_reply)
        
        return jsonify({"reply": formatted_reply})
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            "reply": "I'm having trouble connecting to the AI service. Please try again later."
        }), 500
    except Exception as e:
        return jsonify({
            "reply": "An error occurred while processing your request. Please try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
