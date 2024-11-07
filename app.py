import streamlit as st
import pandas as pd
import requests
import time

# Streamlit UI Setup
st.title("AI Agent Project Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data")
    st.dataframe(data)

# Select main column for queries
if uploaded_file:
    main_column = st.selectbox("Select main column for queries", data.columns)

# Query template input
query_template = st.text_input("Enter your query template (use {entity} as placeholder):", "Retrieve the email address of {entity}")

# Generate queries based on main column
if uploaded_file and main_column:
    entities = data[main_column].tolist()
    queries = [query_template.replace("{entity}", str(entity)) for entity in entities]
    st.write("Generated Queries:")
    for query in queries:
        st.write(query)

# SerpApi web search function
SERP_API_KEY = '1fea1f5c1703fb9f23b9c18656ff12f79dc6d1fcf2144916ac53f546627fca03'  # Replace with your SerpApi key

def web_search(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# Perform web searches for each query
search_results = []
for query in queries:
    result = web_search(query)
    if result:
        search_data = {
            "query": query,
            "url": result.get("organic_results")[0]["link"] if result.get("organic_results") else None,
            "snippet": result.get("organic_results")[0]["snippet"] if result.get("organic_results") else None
        }
        search_results.append(search_data)

# Convert search results to DataFrame and display
results_df = pd.DataFrame(search_results)
st.write("Search Results:")
st.dataframe(results_df)

# Optionally, save search results to CSV
results_df.to_csv("search_results.csv", index=False)

# Groq API setup for language model processing
GROQ_API_KEY = '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'  # Replace with your Groq API key

def extract_information_with_groq(entity, search_snippet):
    url = "https://api.groq.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "groq-base-1",  # Replace with your preferred Groq model
        "prompt": f"Extract the email address for {entity} from the following information:\n{search_snippet}\n",
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    return "Error"

# Loop through each search result to extract information with Groq
extracted_data = []
for result in search_results:
    entity = result["query"].split("{entity}")[1]  # Adjust to parse entity name if needed
    snippet = result["snippet"]
    email = extract_information_with_groq(entity, snippet)
    
    extracted_data.append({
        "entity": entity,
        "snippet": snippet,
        "email": email
    })

# Handle retries for Groq API calls
def extract_with_retries(entity, snippet, retries=3):
    for attempt in range(retries):
        try:
            return extract_information_with_groq(entity, snippet)
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"Failed to retrieve information for {entity}: {e}")
                return "Error"

# Convert extracted data to DataFrame and display
results_df = pd.DataFrame(extracted_data)
st.write("Extracted Information:")
st.dataframe(results_df)

# Add a Download button for CSV
csv = results_df.to_csv(index=False)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="extracted_data.csv",
    mime="text/csv",
)

# Error Handling:
import streamlit as st

try:
    # Your existing code where the error might occur
    query = result["query"]
    parts = query.split("{entity}")
    
    if len(parts) > 1:
        entity = parts[1]  # Safely access the second part after splitting by "{entity}"
    else:
        entity = None  # Handle the case where "{entity}" is not found
    
    # Do something with 'entity'
    st.write(f"Entity: {entity}")

except IndexError as e:
    # Catch the IndexError and display a custom message without stopping the app
    st.error("There was an issue with processing the query. Please check the format.")
    
except Exception as e:
    # This catches other exceptions, so nothing breaks the app
    st.error(f"An unexpected error occurred: {str(e)}")
