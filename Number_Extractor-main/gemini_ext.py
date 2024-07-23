import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st

# Load environment variables
load_dotenv()

# Function to get response from Google Gemini
def get_response(question):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
    # Default prompt for extracting numerical strings from a sentence
    prompt_template = PromptTemplate.from_template("Extract all numerical strings from the following sentence and correct any typos or spelling errors: {input}")
    tweet_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    response = tweet_chain.run(input=question)
    return response

# Streamlit UI setup
st.set_page_config(page_title="Number String Extractor")
st.header("Langchain Application: Extract Number Strings")

input_text = st.text_input("Enter a sentence: ")

submit_button = st.button("Extract Number Strings")

if submit_button:
    response = get_response(input_text)
    st.subheader("Extracted Number Strings:")
    st.write(response)
