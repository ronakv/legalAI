import streamlit as st
import backend

# Set up the title and layout of the app
st.set_page_config(
    page_title='Indian Arbitration Robot',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'About': "This is an Indian Arbitration Robot designed to answer your arbitration related questions."
    }
)

st.title('Indian Arbitration Robot')

# Theming and Custom CSS
st.markdown("""
<style>
.stTextInput>div>div>input {
    color: black;
}
.stButton>button {
    color: white;
    background-color: #4CAF50; /* Green */
}
</style>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for tools and settings
with st.sidebar:
    st.header("Tools")
    uploaded_file = st.file_uploader("Upload a PDF file:", type=['pdf'])
    st.header("Settings")
    language = st.selectbox("Choose a Language", ["English", "Hindi"])

# Display chat messages from history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.info(message["content"])
        else:
            st.success(message["content"])

# Chat input
prompt = st.text_input("Hello! Ask me an arbitration related question")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Simulate processing time and get the response from the backend
    with st.spinner('Fetching the best response...'):
        response = backend.get_answer(prompt)  # assuming backend.get_answer returns a string
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Refresh the chat messages to include the latest
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.info(message["content"])
            else:
                st.success(message["content"])
