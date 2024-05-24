import streamlit as st
import openai
from duckduckgo_search import ddg

# Function to search the web using DuckDuckGo
def search_web(query):
    results = ddg(query, max_results=5)
    return results

# Function to generate a response using OpenAI's GPT-4
def generate_response(prompt, api_key):
    openai.api_key = api_key
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use the appropriate model
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.9,
    )
    return response.choices[0].text.strip()

# Set up the Streamlit app
st.title('AI Search Assistant 🌐')
st.caption('This app allows you to search the web using AI')

# Get OpenAI API key from user
openai_access_token = st.text_input('OpenAI API Key', type='password')

# If OpenAI API key is provided, proceed
if openai_access_token:
    # Get the search query from the user
    query = st.text_input('Enter the Search Query', type='default')

    if query:
        st.write('Searching the web...')
        search_results = search_web(query)
        
        if search_results:
            st.write('Top search results:')
            for i, result in enumerate(search_results):
                st.write(f"{i+1}. [{result['title']}]({result['href']})")
            
            st.write('Generating response with GPT-4...')
            search_summary = "\n".join([f"{result['title']}: {result['body']}" for result in search_results])
            response = generate_response(f"Based on the following search results, provide a summary:\n{search_summary}", openai_access_token)
            st.write('Response:')
            st.write(response)
        else:
            st.write('No search results found.')
    else:
        st.write('Please enter a query.')
