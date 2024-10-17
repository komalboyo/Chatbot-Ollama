import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up the chatbot
template = """
You are a fashion chatbot designed to assist users in identifying their style preferences. Give quick and brief responses.
Here is the conversation history: {context}

Question: {question}

Answer:
"""

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768"
)

prompt = ChatPromptTemplate.from_template(template)
chain = LLMChain(llm=llm, prompt=prompt)

def initialize_session_state():
    if 'context' not in st.session_state:
        st.session_state.context = ""
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def handle_conversation():
    st.set_page_config(page_title="Fashion Chatbot", page_icon="👗", layout="wide")
    
    st.title("👗 Miranda - Your Fashion Assistant")
    st.subheader("Helping you discover your unique style!")
    
    # Sidebar Styling
    with st.sidebar:
        st.header("Fashion Preferences Assistant")
        st.write("Welcome! I'm Miranda, here to help you with all your fashion questions. Type your questions below!")
    
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about fashion!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            result = chain.run(context=st.session_state.context, question=prompt)
            st.markdown(result)
        
        st.session_state.messages.append({"role": "assistant", "content": result})
        st.session_state.context += f"\nUser: {prompt}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()