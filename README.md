
# 🤖 Universal Data Analyst Agent

This project implements a web-based Universal Data Analyst Agent that allows users to analyze data from any public CSV URL by providing natural language tasks. The agent leverages a large language model (LLM) through the OpenRouter API to perform data analysis and generate structured results, including numerical answers, textual summaries, correlations, and even plotting data for client-side visualization.

## ✨ Features

- **Dynamic Data Input:** Analyze datasets directly from any public CSV URL.
- **Natural Language Tasks:** Ask complex data analysis questions in plain English.
- **LLM-Powered Analysis:** Utilizes a powerful LLM (via OpenRouter) to interpret tasks and process data.
- **Structured Output:** Receives results in a consistent 4-element JSON array:
  1. Numerical Answer
  2. String Summary/Textual Answer
  3. Correlation/Relevant Numerical Value
  4. Plotting Data (for client-side visualization)
- **Client-Side Visualization:** Renders interactive scatter plots using Chart.js based on data provided by the LLM.
- **Responsive Web Interface:** A clean and user-friendly interface that adapts to different screen sizes.
- **Robust Error Handling:** Provides clear feedback for API errors, network issues, and LLM response parsing problems.

## 🛠️ Technologies Used

**Backend:**
- FastAPI
- Uvicorn
- Requests
- Pandas
- python-dotenv
- FastAPI-CORS

**Frontend:**
- HTML5
- CSS3
- JavaScript
- Chart.js

**LLM API:**
- OpenRouter.ai

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- OpenRouter API Key

### 1. Clone the Repository

```bash
git clone https://github.com/varshitha7777/Data-Analyst-Agent.git
cd Data-Analyst-Agent
```

### 2. Set up Python Virtual Environment

```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure .env

Create a `.env` file and add your API key:

```env
OPENROUTER_API_KEY="your_openrouter_api_key_here"
```

### 5. Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

### 6. Run the Frontend

In a new terminal:

```bash
python -m http.server 8001
```

Then go to: `http://localhost:8001/index.html`

## 🧪 Example Usage

**Dataset URL:** `https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv`  
**Tasks:**
- What is the average 'sepal length'?
- Plot 'petal length' vs 'petal width' as array [{x:..., y:...}]
- Correlation between 'petal length' and 'petal width'

## 🐞 Troubleshooting

- **404 `/api/url/`** → Ensure FastAPI is running with the correct endpoint.
- **500 errors** → Try simplifying your questions or restart the server.
- **No plots** → Refine your prompt for clearer plot data.
- **DNS errors** → Check internet, firewall, or flush DNS.

## 🤝 Contributing

Fork, clone, and submit PRs to improve the agent!

## 📄 License

MIT License. See LICENSE file.
