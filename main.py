import streamlit as st
import backend

folder_path = "LFIDocs"
#knowledge.upload_pdfs_to_pinecone(folder_path)

# Set up the title of the app
st.title('Legal AI App')
with st.sidebar:
    uploaded_file = st.file_uploader("Choose a PDF file to upload", type=['pdf'])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream, urls = backend.get_answer(prompt)
        response = st.write(stream + "\n" + urls)
        st.session_state.messages.append({"role": "assistant", "content": stream})
