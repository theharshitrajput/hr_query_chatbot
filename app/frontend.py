import streamlit as st
import requests

# --- Configuration ---
FASTAPI_URL = "http://127.0.0.1:8000/chat"
st.set_page_config(page_title="HR Resource Bot", page_icon="🤖")

# --- UI Elements ---
st.title("🤖 HR Resource Query Bot")
st.caption("Your intelligent assistant for finding the right talent.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! How can I help you find the right person for your project today?"}]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and Logic ---
if prompt := st.chat_input("e.g., 'Find Python developers with 3+ years experience'"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                # Call the FastAPI backend
                response = requests.post(FASTAPI_URL, json={"query": prompt})
                response.raise_for_status()  # Raise an exception for bad status codes
                
                full_response = response.json().get("response", "Sorry, I couldn't get a response.")
                message_placeholder.markdown(full_response)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the backend at {FASTAPI_URL}. Is the backend running?")
                full_response = "Error: Could not connect to the API."
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                full_response = f"An error occurred: {e}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})