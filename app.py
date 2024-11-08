import streamlit as st
import pandas as pd
import requests
import time

# Streamlit UI Setup
st.title("BreakoutAI Agent Dashboard")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("Preview of Uploaded Data")
    st.dataframe(data)

# Select main column for queries
if uploaded_file:
    main_column = st.selectbox("Select the entity-column for queries", data.columns)

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
SERP_API_KEY = 'a1320db86a46c2881a8241f8eb795e7b58e1434d42b2b45b66dd5df2197a1180'  # Replace with your SerpApi key

def web_search(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# Perform web searches with loading indicator
search_results = []
try:
    with st.spinner("Performing web searches..."):
        for query in queries:
            result = web_search(query)
            if result and result.get("organic_results"):
                search_data = {
                    "query": query,
                    "url": result["organic_results"][0].get("link"),
                    "snippet": result["organic_results"][0].get("snippet")
                }
                search_results.append(search_data)
except NameError:
    st.error("Please upload a file to see the results.")
except Exception as e:
    st.error("An unexpected error occurred while performing web searches.")

# Convert search results to DataFrame and display
if search_results:
    results_df = pd.DataFrame(search_results)
    st.write("Search Results:")
    st.dataframe(results_df)
else:
    st.warning("No search results available.")

# Groq model selection dropdown
groq_model = st.selectbox("Select Groq model for extraction", ["gemma2-9b-it", "groq-base-1", "groq-medium-2"])

# Groq API setup for language model processing
GROQ_API_KEY = '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'  # Replace with your Groq API key

def extract_information_with_groq(entity, search_snippet, model):
    url = "https://api.groq.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": model,  # Use selected Groq model
        "prompt": f"Extract the email address for {entity} from the following information:\n{search_snippet}\n",
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("choices", [{}])[0].get("text", "").strip()
    return "Error"

# Loop through each search result to extract information with Groq and loading indicator
extracted_data = []
with st.spinner("Extracting information with Groq..."):
    for result in search_results:
        try:
            # Use the entity name stored in the original query by splitting on the first occurrence
            entity = result["query"].replace(query_template.split("{entity}")[0], "").strip()
            snippet = result.get("snippet", "")
            email = extract_information_with_groq(entity, snippet, groq_model)
            
            extracted_data.append({
                "entity": entity,
                "snippet": snippet,
                "email": email
            })
            
        except IndexError:
            pass
        except Exception as e:
            st.error("An error occurred while extracting information.")

# Convert extracted data to DataFrame and display
if extracted_data:
    extracted_df = pd.DataFrame(extracted_data)
    st.write("Extracted Information:")
    st.dataframe(extracted_df)

    # Add a Download button for CSV
    csv = extracted_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="extracted_data.csv",
        mime="text/csv",
    )
else:
    st.warning("No extracted information available.")
