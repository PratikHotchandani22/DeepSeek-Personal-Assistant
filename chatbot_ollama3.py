import streamlit as st
import ollama

# Set up Streamlit page configuration
st.set_page_config(page_title="💬 DeepSeek Chatbot", layout="wide")

# Initialize chat history and thinking process in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
if "thinking" not in st.session_state:
    st.session_state["thinking"] = []

# Function to extract thinking and content from response
def parse_response(response):
    message_content = response["message"]["content"]
    thinking_content = message_content.split("<think>")[1].split("</think>")[0].strip()
    response_content = message_content.split("</think>")[1].strip()
    return thinking_content, response_content

# Create two columns
chat_col, thinking_col = st.columns(2)

# Chat interface in the left column
with chat_col:
    st.title("DeepSeek Chatbot")
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        st.chat_message(role).write(content)

    # Input box for user prompts
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get response from DeepSeek model via Ollama
        response = ollama.chat(model="deepseek-r1:7b", messages=st.session_state.messages)
        
        # Extract thinking process and actual response
        thinking, content = parse_response(response)

        # Append assistant's response to chat history and display it
        st.session_state.messages.append({"role": "assistant", "content": content})
        st.chat_message("assistant").write(content)

        # Append thinking process to session state
        st.session_state.thinking.append(thinking)

# Thinking process display in the right column
with thinking_col:
    st.title("Model's Thinking Process")
    for i, thought in enumerate(st.session_state.thinking):
        with st.expander(f"Thought Process {i+1}"):
            st.write(thought)

# Display raw JSON response (optional, for debugging)
if st.checkbox("Show raw JSON response"):
    st.json(response)
