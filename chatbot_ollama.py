import streamlit as st
import ollama

# Set up Streamlit page configuration
st.set_page_config(page_title="💬 Llama 3.1 Chatbot", layout="centered")

# Sidebar for user input
with st.sidebar:
    st.title("Llama 3.1 Chatbot")
    user_name = st.text_input("Enter your name:", "")

# Display chatbot title
if user_name:
    st.title(f"Welcome, {user_name}!")
else:
    st.title("Welcome to the Llama 3.1 Chatbot!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    if role == "assistant":
        st.chat_message(role).write(content)
    else:
        st.chat_message(role).write(content)

# Input box for user prompts
if prompt := st.chat_input("Type your message here..."):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get response from Llama 3.1 model via Ollama
    response = ollama.chat(model="deepseek-r1:7b", messages=st.session_state.messages)["message"]["content"]

    # Append assistant's response to chat history and display it
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
