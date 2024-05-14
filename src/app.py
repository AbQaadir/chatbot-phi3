import requests
import json
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage




# chatbot using streamlit, ollama and local model phi3


# gerate response from the model
def generate_response(prompt):
    """
    This function sends a POST request to the local API to generate a response to the user's input.
    """
    url = "http://localhost:11434/api/generate"
    data = {"prompt": prompt, "model": "phi3", "stream": False}
    response = requests.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return "An error occurred."

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage("Hello! I'm a chatbot. How can I help you today?")
    ] 


# set up the streamlit app
st.header("ChatBot with Ollama and Phi3")


# get user input
user_input = st.chat_input("Type your message here ...")

if user_input is not None and user_input != "":
    
    # add user message to chat history
    st.session_state.chat_history.append(HumanMessage(user_input))
    
    # generate response
    response = generate_response(user_input)
    
    # add bot message to chat history
    st.session_state.chat_history.append(AIMessage(response))



# coversation history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(f"{message.content}")
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(f"{message.content}")