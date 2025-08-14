from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Test server is working!"

if __name__ == '__main__':
    print("Starting test server on http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
