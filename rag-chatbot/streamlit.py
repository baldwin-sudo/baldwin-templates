import streamlit as st
from io import BytesIO
import tempfile
import os
from parse_lama import process_pdf_file
from embed import index_data
from rag_chatbot import setup_chatbot, init_es

st.title("Welcome to Baldwin-AI")
st.sidebar.header("Configure your RAG Assistant")

openai_api_key = st.sidebar.text_input("Enter your OpenAI API key :", type="password")
llama_cloud_api_key = st.sidebar.text_input("Enter your LlamaCloud API key :", type="password")

# Add explanatory text for index
index_name = st.sidebar.text_input(
    "Enter a name for your index :",
    help="An 'index' is like a folder where your uploaded documents will be stored. "
         "It helps you organize and search through your documents efficiently."
)

# Initialize session state for file processing and chatbot setup
if 'files_processed' not in st.session_state:
    st.session_state.files_processed = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None

# Multiple file uploader
uploaded_files = st.sidebar.file_uploader("Upload your PDFs", type=["pdf"], accept_multiple_files=True)

if uploaded_files and not st.session_state.files_processed:
    st.write("### Uploaded PDFs Content:")

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Iterate over each uploaded file
        for uploaded_file in uploaded_files:
            st.write(f"**{uploaded_file.name}**")

            # Save the uploaded file to the temporary directory
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            process_pdf_file(file_path)
            st.write(f"File saved temporarily to: {file_path}")

    st.session_state.files_processed = True  # Mark files as processed

if st.sidebar.button("Process Files"):
    if index_name:
        with st.spinner('Processing ...'):
            index_data(index_name=index_name)
            st.session_state.chatbot = setup_chatbot(index_name=index_name, es=init_es())

        st.success("Files processed successfully")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message["content"])

# React to user prompt
if prompt := st.chat_input('...'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Ensure chatbot is set up before asking a question
    if st.session_state.chatbot:
        response = st.session_state.chatbot.ask(prompt)
        st.chat_message("assistant").markdown(response.content)
        st.session_state.messages.append({'role': "assistant", "content": response.content})
else:
    st.error("Please enter a name for your index before processing files.")
