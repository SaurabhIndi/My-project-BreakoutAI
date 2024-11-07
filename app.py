import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.title("AI Agent Project Dashboard")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data")
    st.dataframe(data)

if st.button("Connect to Google Sheets"):
    creds = service_account.Credentials.from_service_account_file('credentials.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    sheet_id = "your_google_sheet_id_here"  # Replace with your sheet ID

    # Example of reading data
    result = sheet.values().get(spreadsheetId=sheet_id, range="Sheet1").execute()
    values = result.get('values', [])
    st.write("Data from Google Sheet")
    st.write(values)

if uploaded_file:
    main_column = st.selectbox("Select main column for queries", data.columns)



# Prompt input box in Streamlit
query_template = st.text_input("Enter your query template (use {entity} as placeholder):", "Retrieve the email address of {entity}")

import gspread

# Authenticate and load the sheet
gc = gspread.service_account(filename='credentials.json')
sh = gc.open('Your Google Sheet Name')
worksheet = sh.sheet1

# Get the entities column as a list
entities = worksheet.col_values(2)  # Replace 2 with the column index for the entities

# Generate dynamic queries
queries = [query_template.replace("{entity}", entity) for entity in entities]

# Display or Use the Queries
st.write("Generated Queries:")
for query in queries:
    st.write(query)


# Define the Web Search Function
import requests

API_KEY = '99c1681eeabf270679f50b824989565e27ce704d93de372a47614a8059c1bf1d'

def web_search(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None


# Automate Searches for Each Query:
search_results = []

for query in queries:
    result = web_search(query)
    if result:
        # Extract relevant information, e.g., URLs and snippets
        search_data = {
            "query": query,
            "url": result.get("organic_results")[0]["link"] if result.get("organic_results") else None,
            "snippet": result.get("organic_results")[0]["snippet"] if result.get("organic_results") else None
        }
        search_results.append(search_data)


# Save or Display the Results:
# Convert results to a DataFrame
results_df = pd.DataFrame(search_results)

# Display in Streamlit
st.write("Search Results:")
st.dataframe(results_df)

# Optionally, save to CSV
results_df.to_csv("search_results.csv", index=False)


# Define a Function to Interact with the LLM:
import openai

openai.api_key = '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'

def extract_information_with_llm(entity, search_snippet):
    # Define your prompt with placeholders
    prompt = f"Extract the email address for {entity} from the following information:\n{search_snippet}\n"
    
    # Send request to OpenAI's GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Choose your preferred model
        messages=[{"role": "system", "content": "You are an assistant that extracts email addresses."},
                  {"role": "user", "content": prompt}],
        max_tokens=100  # Adjust token count as needed
    )
    
    # Extract the response content
    answer = response['choices'][0]['message']['content'].strip()
    return answer


# Loop Through Each Search Result to Extract Information:
extracted_data = []

for result in search_results:
    entity = result["query"].split("{entity}")[1]  # Adjust to parse entity name if needed
    snippet = result["snippet"]
    email = extract_information_with_llm(entity, snippet)
    
    extracted_data.append({
        "entity": entity,
        "snippet": snippet,
        "email": email
    })


# Handle API Errors
import time

def extract_with_retries(entity, snippet, retries=3):
    for attempt in range(retries):
        try:
            return extract_information_with_llm(entity, snippet)
        except openai.error.OpenAIError as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to retrieve information for {entity}: {e}")
                return "Error"


# Display and Download Results
# Display Results in a Table Format:
import pandas as pd
import streamlit as st

# Convert to DataFrame
results_df = pd.DataFrame(extracted_data)

# Display in Streamlit
st.write("Extracted Information:")
st.dataframe(results_df)

# Add a Download Button for CSV:
# Download as CSV
csv = results_df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="extracted_data.csv",
    mime="text/csv",
)

# Update Data Back to Google Sheets
# Authenticate and open the Google Sheet
gc = gspread.service_account(filename='credentials.json')
sh = gc.open('Your Google Sheet Name')
worksheet = sh.sheet1

# Clear existing data (optional, based on user preference)
worksheet.clear()

# Update with new data
worksheet.update([results_df.columns.values.tolist()] + results_df.values.tolist())
