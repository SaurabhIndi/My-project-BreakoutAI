# BreakoutAI Agent Dashboard

A Streamlit-based dashboard for automating data extraction and querying web information. This application enables users to upload a CSV file containing entities (e.g., names or organizations), generate customized queries, retrieve search results via SerpApi, and extract specific information (like email addresses) using Groq’s language model API. Results can be exported as a CSV file for easy further use.

## Table of Contents

- [Project Description](#project-description)
- [Setup Instructions](#setup-instructions)
- [Usage Guide](#usage-guide)
- [Connecting Google Sheets](#connecting-google-sheets)
- [API Keys and Environment Variables](#api-keys-and-environment-variables)
- [Optional Features](#optional-features)

## Project Description

The BreakoutAI Agent Dashboard streamlines the process of information extraction by:
- Allowing users to upload a CSV with entities to be queried.
- Enabling custom search query generation based on user-defined templates.
- Retrieving search results for each query using SerpApi.
- Extracting relevant details (like email addresses) from search snippets with Groq’s language model API.
- Displaying results in an interactive dashboard with options to download data as a CSV file.

## Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/breakoutai-agent-dashboard.git
   cd breakoutai-agent-dashboard
   ```

2. **Install Dependencies**  
   Ensure Python 3.8+ is installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**  
   Rename `.env.example` to `.env` and add your API keys for SerpApi and Groq (details below).

4. **Run the Application**  
   Launch the Streamlit dashboard with:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. **Upload a CSV File**  
   After launching the app, upload a CSV file containing a column with entities (e.g., names or organizations).

2. **Select the Entity Column**  
   Choose the column that contains the entities you want to query.

3. **Enter a Query Template**  
   Define a search query template. Use `{entity}` as a placeholder for entities in your selected column.  
   **Example:** `Retrieve the email address of {entity}`.

4. **Run Web Searches**  
   The app will create queries from your template, retrieve results via SerpApi, and display them with associated snippets.

5. **Information Extraction**  
   Using the Groq API, the app extracts specific details (e.g., email addresses) from search snippets and presents them in a table.

6. **Export Results**  
   Download the extracted information as a CSV file with the **Download** button.

### Connecting Google Sheets

Direct Google Sheets integration is not currently supported. However, you can export data from Google Sheets as a CSV and upload it to the dashboard. For further automation, consider using the Google Sheets API to download CSV data directly.

## API Keys and Environment Variables

To use this app, you will need API keys for both **SerpApi** and **Groq**:

1. **SerpApi**  
   - Sign up at [SerpApi](https://serpapi.com/) to obtain your API key.
   - In the `.env` file, set your key as `SERP_API_KEY`.

2. **Groq API**  
   - Register at [Groq](https://groq.com/) to acquire an API key.
   - Set this key as `GROQ_API_KEY` in the `.env` file.

   **Example `.env` File**:
   ```bash
   SERP_API_KEY=your_serpapi_key
   GROQ_API_KEY=your_groq_api_key
   ```

Ensure these keys are stored securely and are not hardcoded in the codebase.

## Optional Features

- **Downloadable CSV Output**: Allows downloading the extracted information as a CSV file for sharing or analysis.
- **Error Handling**: The app is equipped to handle missing or empty search results gracefully, providing users with a smooth experience.
- **Scalable Query Generation**: The query template with `{entity}` placeholders allows flexible adaptation to different use cases.

---
