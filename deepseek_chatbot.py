import os
import glob
from PIL import Image
import PyPDF2
import streamlit as st

def upload_file():
    file_types = ["image", "pdf"]
    for file_type in file_types:
        if file_type == "image":
            uploaded_file = st.file_uploader("Upload an image...", type="png|jpg|jpeg")
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Uploaded {file_type} file", use_column_width=True)
                return image
        elif file_type == "pdf":
            uploaded_file = st.file_uploader("Upload a PDF...", type="pdf")
            if uploaded_file:
                reader = PyPDF2.PdfReader(uploaded_file)
                page_count = len(reader.pages)
                st.write(f"Uploaded PDF: {page_count} pages")
                for page in reader.pages:
                    st.write(page.extract_text())
                return reader
    return None

def process_image(image):
    if image is not None:
        st.write("Image Preview:")
        st.image(image, use_column_width=True)

def process_pdf(reader):
    if reader is not None:
        with st.expander("View PDF"):
            for page in reader.pages:
                st.write(page.extract_text())

def generate_response(prompt, bot_thinks):
    # Simulated thinking and response
    if prompt:
        bot_thinks.append(f"User: {prompt}")
        response = "This is a simulated response to your message."
        bot_thinks.append(f"AiResponse: {response}")
    return response

def main():
    st.title("AI Chat Bot")
    
    with st.sidebar:
        st.header("Bot Options")
        file_type = ["Upload File", "Enter Message"]
        selected_option = st.selectbox("Choose an option:", file_type)
        
        if selected_option == "Upload File":
            uploaded_image = st.file_uploader("Upload an image...", type="png|jpg|jpeg")
            if uploaded_image:
                image = Image.open(uploaded_image)
                st.image(image, caption=f"Uploaded {file_type[0]} file", use_column_width=True)
        
        if selected_option == "Enter Message":
            user_message = st.text_area("Type your message here...")
    
    main_column, right_column = st.columns([3, 1])
    
    with main_column:
        # Add a check for image upload
        if "image" in [f.type for f in st.file_uploader("Upload an image...", type="png|jpg|jpeg").files]:
            uploaded_image = st.file_uploader("Upload an image...", type="png|jpg|jpeg")
            if uploaded_image:
                process_image(uploaded_image)
        
        # Add a check for PDF upload
        if "pdf" in [f.type for f in st.file_uploader("Upload a PDF...", type="pdf").files]:
            uploaded_pdf = st.file_uploader("Upload a PDF...", type="pdf")
            if uploaded_pdf:
                process_pdf(uploaded_pdf.pages)
    
    with right_column:
        if user_message:
            col1, col2, col3 = st.columns([0.5, 0.8, 0.5])
            with col2:
                bot_thinks = ["User Query:", user_message]
                for i in range(len(bot_thinks)):
                    st.write(f"Step {i + 1}:")
                    if i % 2 == 0:
                        st.write(f"User: {bot_thinks[i]}")
                    else:
                        response = generate_response(user_message, bot_thinks)
                        st.write(f"AiResponse: {response}")
    
    # Add a loading spinner while processing files
    with st.expander("Waiting..."):
        pass

if __name__ == "__main__":
    main()