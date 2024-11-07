BreakoutAI Agent Dashboard
A powerful Streamlit-based dashboard for automating data extraction and querying web information. This application allows users to upload a CSV file with entities (e.g., names or organizations), generate customized queries, and retrieve search results using the SerpApi. Extract specific information (such as email addresses) using the Groq API, with the ability to export results as a CSV file for further use.

Project Description
The BreakoutAI Agent Dashboard is designed to streamline information extraction by:

Enabling users to upload a CSV with entities to be queried.
Generating custom search queries based on user-defined templates.
Retrieving web search results for each query via SerpApi.
Extracting specific details (like email addresses) from search snippets using Groq’s language model API.
Displaying results within the dashboard and offering CSV downloads.
Setup Instructions
Clone the Repository

bash
Copy code
git clone https://github.com/yourusername/breakoutai-agent-dashboard.git
cd breakoutai-agent-dashboard
Install Dependencies
Ensure you have Python 3.8+ installed, then install the required packages:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables
Rename .env.example to .env and add your API keys for SerpApi and Groq (details below).

Run the Application
Launch the Streamlit dashboard with:

bash
Copy code
streamlit run app.py
Usage Guide
Upload a CSV File
After launching the app, upload a CSV file with a column containing entities (e.g., names or organizations).

Select the Entity Column
Choose the column from your CSV that contains the entities you want to search for.

Enter a Query Template
Define a template for your search queries. Use {entity} as a placeholder for the entities in your selected column.
Example: Retrieve the email address of {entity}.

Run Web Searches
The dashboard generates queries based on your template, retrieves results using SerpApi, and displays them with snippets.

Information Extraction
Using the Groq API, it extracts relevant information (e.g., email addresses) from each snippet. The extracted data is displayed in a table format.

Export Results
Download the extracted information as a CSV file using the Download button.

Connecting Google Sheets
Currently, the app doesn’t directly support Google Sheets integration. However, if your data is in Google Sheets, export it as a CSV file and then upload it to the dashboard. You can automate this process with the Google Sheets API if you’re interested in further customization.

API Keys and Environment Variables
To use this app, you need API keys for both SerpApi and Groq:

SerpApi

Sign up at SerpApi and obtain your API key.
In your .env file, set your key as SERP_API_KEY.
Groq API

Register at Groq and get an API key.
In your .env file, set this key as GROQ_API_KEY.
Example of .env File:

bash
Copy code
SERP_API_KEY=your_serpapi_key
GROQ_API_KEY=your_groq_api_key
Make sure to keep these keys secure and avoid hardcoding them in the codebase.

Optional Features
Downloadable CSV Output: Download the extracted information in a CSV format for easy sharing or further analysis.
Error Handling: Handles issues with missing or empty search results, providing a user-friendly experience.
Scalable Query Generation: Easily adapt the query template for different use cases by modifying {entity} placeholders.
