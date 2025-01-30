import streamlit as st
import ollama
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io

# Set up Streamlit page configuration
st.set_page_config(page_title="💬 DeepSeek Chatbot", layout="wide")

# Initialize chat history and thinking process in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]
if "thinking" not in st.session_state:
    st.session_state["thinking"] = []

# Function to extract text from PDF and image files
def extract_text(file):
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'pdf':
        text = ""
        pdf_file = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf_file:
            text += page.get_text()
        return text
    
    elif file_extension in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
        return pytesseract.image_to_string(Image.open(file))
    
    else:
        raise ValueError("Unsupported file format")

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

    # File uploader for PDF and image files
    uploaded_file = st.file_uploader("Upload a PDF or image file", type=['pdf', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'])
    
    if uploaded_file is not None:
        try:
            file_content = extract_text(uploaded_file)
            st.success("File uploaded and text extracted successfully!")
            st.session_state.messages.append({"role": "user", "content": f"Here's the content of the uploaded file: {file_content}"})
            st.chat_message("user").write(f"File uploaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

    # Input box for user prompts
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

    # Process the last message (whether from file upload or text input)
    if st.session_state.messages[-1]["role"] == "user":
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
