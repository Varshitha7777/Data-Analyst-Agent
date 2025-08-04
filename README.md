🤖 Universal Data Analyst Agent
This project implements a web-based Universal Data Analyst Agent that allows users to analyze data from any public CSV URL by providing natural language tasks. The agent leverages a large language model (LLM) through the OpenRouter API to perform data analysis and generate structured results, including numerical answers, textual summaries, correlations, and even plotting data for client-side visualization.

✨ Features
Dynamic Data Input: Analyze datasets directly from any public CSV URL.

Natural Language Tasks: Ask complex data analysis questions in plain English.

LLM-Powered Analysis: Utilizes a powerful LLM (via OpenRouter) to interpret tasks and process data.

Structured Output: Receives results in a consistent 4-element JSON array:

Numerical Answer

String Summary/Textual Answer

Correlation/Relevant Numerical Value

Plotting Data (for client-side visualization)

Client-Side Visualization: Renders interactive scatter plots using Chart.js based on data provided by the LLM.

Responsive Web Interface: A clean and user-friendly interface that adapts to different screen sizes.

Robust Error Handling: Provides clear feedback for API errors, network issues, and LLM response parsing problems.

🛠️ Technologies Used
Backend:

FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.

Uvicorn: An ASGI server for running FastAPI applications.

Requests: HTTP library for making API calls (to OpenRouter) and fetching datasets.

Pandas: Data manipulation and analysis library, used for reading CSVs and generating data previews.

python-dotenv: For loading environment variables (like API keys) from a .env file.

FastAPI-CORS: CORS (Cross-Origin Resource Sharing) middleware for FastAPI.

Frontend:

HTML5

CSS3

JavaScript

Chart.js: A simple yet flexible JavaScript charting library for rendering visualizations.

Language Model API:

OpenRouter.ai: A unified API for accessing various large language models (e.g., openai/gpt-3.5-turbo).

🚀 Getting Started
Follow these steps to set up and run the Universal Data Analyst Agent on your local machine.

Prerequisites
Python 3.8+ installed on your system.

Git installed on your system.

A GitHub account (if you plan to clone/fork).

An OpenRouter API Key. You can get one by signing up at OpenRouter.ai.

1. Clone the Repository (or download files)
If you're starting fresh or want to clone the project:

git clone https://github.com/varshitha7777/Data-Analyst-Agent.git
cd Data-Analyst-Agent

If you've been working locally, ensure all your files (main.py, index.html, requirements.txt, .env) are in the same project directory.

2. Set up Python Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

python -m venv venv

Activate the virtual environment:

On Windows (PowerShell):

.\venv\Scripts\Activate.ps1

On macOS/Linux (Bash/Zsh):

source venv/bin/activate

3. Install Dependencies
With your virtual environment activated, install the required Python packages:

pip install -r requirements.txt
# Or manually:
# pip install fastapi uvicorn requests pandas python-dotenv fastapi-cors

4. Configure OpenRouter API Key
Create a file named .env in the root of your project directory (the same folder as main.py) and add your OpenRouter API key:

OPENROUTER_API_KEY="your_openrouter_api_key_here"

Replace "your_openrouter_api_key_here" with your actual API key.

5. Run the Backend (FastAPI)
Open your first terminal window and ensure your virtual environment is activated.

uvicorn main:app --reload --port 8000

This will start the FastAPI server, typically accessible at http://127.0.0.1:8000. Keep this terminal running.

6. Run the Frontend (Static File Server)
Open a second, new terminal window and ensure your virtual environment is activated. Navigate to the same project directory.

python -m http.server 8001

This will start a simple HTTP server to serve your index.html file, typically accessible at http://127.0.0.1:8001. Keep this terminal running.

🚀 How to Use the Application
Open your web browser and navigate to http://localhost:8001/index.html.

You will see the "Universal Data Analyst Agent" interface.

Dataset URL: Enter the URL of a public CSV dataset. A default Iris dataset URL is provided for convenience.

Analysis Tasks:

Type your analysis questions in natural language.

Click "+ Add Task" to add more questions.

Click "Remove" to delete a task.

Important for Plotting: If you want a visualization, explicitly ask for plotting data in the format [{x: val1, y: val2}, ...]. The LLM will try to extract this data, and the frontend will render it.

Click the "📊 Analyze" button.

The application will display the numerical answer, string summary, correlation/value, and a scatter plot if plotting data was successfully provided by the LLM.

Example Usage
Dataset URL: https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv

Analysis Tasks:

What is the average 'sepal length' for all flowers?

Provide the data points for a scatter plot of 'petal length' (x-axis) vs 'petal width' (y-axis) as an array of objects like [{x: val1, y: val2}, ...].

What is the Pearson correlation between 'petal length' and 'petal width'?

Dataset URL: https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv

Analysis Tasks:

What is the average life expectancy globally in the year 2007?

What is the country with the highest GDP per capita in 2007?

Provide the data points for a scatter plot of 'gdpPercap' (x-axis) vs 'lifeExp' (y-axis) for the year 2007 as an array of objects like [{x: val1, y: val2}, ...].

troubleshooting
404 Not Found for /api/url/: Ensure your FastAPI server (main.py) is running on http://localhost:8000 and has the @app.post("/api/url/") endpoint defined. Restart FastAPI after any main.py changes.

500 Internal Server Error with "Failed to parse model response as valid JSON": This usually means the LLM's response was truncated or malformed.

Ensure your main.py is using the latest code that requests plotting data (JSON array/object) instead of base64 images.

Try simplifying your plotting request in the "Analysis Tasks" (e.g., ask for "simple data points" for a plot).

This can sometimes be an intermittent issue with the LLM API; try again.

NameResolutionError or Max retries exceeded: This is a network/DNS issue on your local machine.

Check your internet connection.

Try ping raw.githubusercontent.com in your terminal.

Flush your DNS cache (ipconfig /flushdns on Windows).

Temporarily disable firewalls/antivirus for testing.

Chart not rendering:

Check the "Plotting Data" output in the results. Is it an empty array [] or null? If so, the LLM didn't provide the data. Refine your plotting task to be more explicit.

Open your browser's developer console (F12) for JavaScript errors related to Chart.js.

🤝 Contributing
Feel free to fork this repository, open issues, or submit pull requests to improve the Universal Data Analyst Agent!

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
