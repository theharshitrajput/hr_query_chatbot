# HR Resource Query Chatbot

![Chatbot Demo](https://github.com/theharshitrajput/hr_query_chatbot/blob/main/working.png?raw=true)

---

## Overview
This project is an intelligent HR assistant chatbot designed to help managers and HR teams find suitable employees for projects based on natural language queries. It leverages a Retrieval-Augmented Generation (RAG) system to understand user requests and provide insightful, context-aware recommendations.

The application uses a hybrid AI approach, performing semantic search locally for speed and privacy, while using a powerful cloud-based LLM for high-quality response generation. It is built with a **FastAPI** backend and a **Streamlit** frontend.

---

## Features
- **Natural Language Understanding**: Ask complex questions like "Who has worked on healthcare projects?" or "Compare developers with AWS and Python skills."
- **Hybrid RAG Pipeline**:
  - **Retrieval**: Uses a local `Sentence-Transformers` model and `FAISS` vector search to find relevant employees semantically. This process is fast, free, and keeps employee data private.
  - **Generation**: Leverages **Google's Gemini API** (specifically `gemini-1.5-flash-latest` via the free tier) to generate high-quality, synthesized responses.
- **RESTful API**: A robust FastAPI backend provides endpoints for the chat functionality and a basic structured search.
- **Interactive UI**: A clean and simple chat interface built with Streamlit for easy interaction.

---

## Architecture
The system consists of three main components:

1.  **Frontend (Streamlit)**: A lightweight web interface that captures user queries and displays the generated responses in a chat format.
2.  **Backend (FastAPI)**: The application's core. It exposes REST endpoints, handles incoming requests, and orchestrates the RAG pipeline.
3.  **RAG System (AI/ML Core)**:
    - **Data Loader**: Loads and preprocesses employee data from the `employees.json` file.
    - **Vector Store**: On startup, employee profiles are converted into vector embeddings using a local `SentenceTransformer` model and indexed in-memory using `FAISS` for fast similarity searches.
    - **LLM Service**: Interacts with the Google Gemini API to generate the final, coherent response based on the retrieved context.

**Flow Diagram:**
`User Query (Streamlit) -> POST Request -> FastAPI Backend -> RAG System (Local Retrieve -> Augment -> Cloud Generate) -> Google Gemini API -> Response -> Streamlit UI`

---

## Setup & Installation

**Prerequisites:**
- Python 3.8+
- A Google Gemini API Key (available for free from Google AI Studio)

**Instructions:**
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/theharshitrajput/hr_query_chatbot.git](https://github.com/theharshitrajput/hr_query_chatbot.git)
    cd hr_query_chatbot
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the environment file:**
    Create a file named `.env` in the root directory and add your API key:
    ```
    GOOGLE_API_KEY="your_api_key_here"
    ```

5.  **Run the application:**
    You will need two separate terminals.

    * **In Terminal 1, start the FastAPI backend:**
        ```bash
        uvicorn app.main:app --reload
        ```

    * **In Terminal 2, start the Streamlit frontend:**
        ```bash
        streamlit run app/frontend.py
        ```
    Your browser should automatically open to the chat application.

---

## Technical Decisions
- **Hybrid AI Model**: We chose a hybrid approach to get the best of both worlds.
  - **Local Embeddings** (`Sentence-Transformers`): Retrieval is a high-frequency task. Running it locally makes it free, instant, and ensures sensitive employee data used for searching never leaves the machine.
  - **Cloud Generation** (`Google Gemini API`): Generation requires a powerful LLM for high-quality, nuanced responses. Using the Gemini API's generous free tier gives us state-of-the-art text generation without requiring powerful local hardware (like a GPU).
- **FAISS vs. Vector Database**: For the scale of this project (15-1000s of employees), an in-memory library like `FAISS` is highly efficient and avoids the operational overhead and cost of setting up a dedicated database service like Pinecone or Chroma.