# StandardsGPT - AI Assistant

A web-based AI assistant for GYM GOERS.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd StandardsGPT
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration**
   - Copy the example configuration file:
     ```bash
     cp config.example.py config.py
     ```
   - Edit `config.py` and add your OpenRouter API key:
     ```python
     OPENROUTER_API_KEY = "your_openrouter_api_key_here"
     ```
   - Get an API key from [OpenRouter](https://openrouter.ai/keys)
   - Adjust other settings like `DEFAULT_MODEL` if needed

5. **Run the application**
   ```bash
   python server.py
   ```
   The application will be available at `http://127.0.0.1:5000`

## Deployment

### Option 1: PythonAnywhere (Free tier available)
1. Create an account on [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your project files
3. Set up a web app with Flask
4. In the web app configuration, add your OpenRouter API key as an environment variable:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```
5. Reload your web app

### Option 2: Vercel (Serverless)
1. Install Vercel CLI: `npm install -g vercel`
2. Run `vercel` and follow the prompts
3. Set your environment variables in the Vercel dashboard

## Configuration

- Update `server.py` to change the AI model or response settings
- Customize the frontend in `index.html` and `styles.css`

## License

This project is open source and available under the MIT License.
