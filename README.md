# BreakoutAI Agent Dashboard

## Project Description
The BreakoutAI Agent Dashboard is a Streamlit-based web application designed to automate information extraction from a CSV file. Users can upload a CSV, generate queries based on selected entity columns, and perform web searches using the SerpApi API. Additionally, the application can extract relevant information using Groq's language models and outputs the results in a downloadable CSV format.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd BreakoutAI-Agent-Dashboard
```

### 2. Install Dependencies
Ensure you have Python installed (preferably 3.7 or higher). Install the required packages by running:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
To launch the Streamlit dashboard, use:
```bash
streamlit run app.py
```

### 4. API Keys Setup
- **SerpApi Key**: Sign up at [SerpApi](https://serpapi.com/) and retrieve your API key. Replace `SERP_API_KEY` in `app.py` with your actual API key.
- **Groq API Key**: Sign up at [Groq](https://console.groq.com/keys) and get an API key for access to their models. Replace `GROQ_API_KEY` in `app.py` with your actual API key.

Alternatively, you can store these keys in environment variables for better security:
```bash
export SERP_API_KEY='your_serpapi_key'
export GROQ_API_KEY='your_groq_key'
```

## Usage Guide

### Step 1: Upload a CSV File
1. Use the **Upload CSV file** button to upload your dataset.
2. The dashboard will display a preview of the uploaded data.

### Step 2: Select the Entity Column
1. Choose the main column that contains the entities for your queries. This column will be used in query templates.

### Step 3: Enter Query Template
1. In the **Query Template** input, define a template (e.g., `Retrieve the email address of {entity}`), where `{entity}` will be replaced with the data from your chosen column.
2. The application generates queries using this template, and displays them on the dashboard.

### Step 4: Perform Web Searches
1. Each generated query is used to perform a Google search using SerpApi, and results are displayed as URLs and snippets.

### Step 5: Extract Information with Groq
1. Choose a model from the **Groq model selection** dropdown (e.g., "gemma2-9b-it").
2. The application will attempt to extract relevant information from each search result snippet using the selected Groq model.

### Step 6: Download Extracted Data
Once the extraction is complete, download the results as a CSV file by clicking **Download data as CSV**.

## API Keys and Environment Variables
API keys for SerpApi and Groq should be entered directly in `app.py` or stored as environment variables for security. The application will access these keys during web searches and information extraction.

- **SerpApi Key**: `SERP_API_KEY`
- **Groq API Key**: `GROQ_API_KEY`

## Optional Features
- **Model Selection**: Users can choose from available Groq models to tailor the extraction process.
- **Loading Indicators**: Real-time progress indicators provide a user-friendly experience when performing web searches and extractions. 

This tool simplifies automated entity-specific information retrieval and extraction for efficient data analysis. Enjoy using the BreakoutAI Agent Dashboard!

## Video Walkthrough (Loom)
Check out a [video walkthrough](https://www.loom.com/share/9190d2ab244f4d408f840c9ad40c5183?sid=398388f8-1018-484e-a8a8-0db821b9288d) of the project for an overview and demo!