# StandardsGPT - AI Assistant

A web-based AI assistant that provides structured, point-wise responses to user queries.

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

4. **Set up environment variables**
   - Rename `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```
   - Get an API key from [OpenAI](https://platform.openai.com/api-keys)

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
4. Add your environment variables in the web app configuration
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
