# LoadWise AI – Smart Building Load Balancing Advisor

A multi-agent AI application powered by **IBM watsonx.ai** (Llama 3.3 70B) that helps building managers monitor, analyze, and optimize electricity consumption.

## Features

- **Agent 1 – Load Monitoring & Analysis**: Analyze consumption patterns and load distribution across all building systems.
- **Agent 2 – Peak Load Detection**: Identify demand spikes, classify risk levels, and detect abnormal consumption.
- **Agent 3 – Smart Load Balancing**: Generate intelligent load scheduling and demand response strategies.
- **Agent 4 – Energy Optimization**: Produce long-term cost-saving and sustainability roadmaps.

## Project Structure

```
LoadWise-AI/
├── app.py                  # Flask backend – routes & AI agent logic
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── templates/
│   └── index.html          # Main HTML frontend template
└── static/
    ├── css/
    │   └── styles.css      # Application stylesheet
    └── js/
        └── main.js         # Frontend JavaScript (API calls, UI logic)
```

## Setup

### 1. Clone & install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your IBM watsonx.ai credentials:

```bash
cp .env.example .env
```

```env
IBM_API_KEY=your_ibm_api_key_here
IBM_PROJECT_ID=your_project_id_here
IBM_URL=https://us-south.ml.cloud.ibm.com
```

### 3. Run the application

```bash
python app.py
```

Open your browser at [http://localhost:5000](http://localhost:5000).

## API Endpoints

| Method | Endpoint      | Description                        |
|--------|---------------|------------------------------------|
| GET    | `/`           | Serves the main UI                 |
| POST   | `/api/agent1` | Load Monitoring & Analysis         |
| POST   | `/api/agent2` | Peak Load Detection                |
| POST   | `/api/agent3` | Smart Load Balancing               |
| POST   | `/api/agent4` | Energy Optimization Insights       |

All POST endpoints accept JSON and return `{ "result": "<AI response>" }`.

## Tech Stack

- **Backend**: Python, Flask, ibm-watsonx-ai SDK
- **AI Model**: `meta-llama/llama-3-3-70b-instruct` via IBM watsonx.ai
- **Frontend**: HTML5, Bootstrap 5, Bootstrap Icons, vanilla JavaScript
