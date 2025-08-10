import os
import numpy as np
import faiss
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from typing import List, Dict

from .data_loader import load_employees, format_employee_for_embedding

# Load environment variables
load_dotenv()

class RAGSystem:
    def __init__(self, employees_data: List[Dict]):
        # Configure the Gemini API
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.generation_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Load the local sentence transformer model for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Store employee data and create document strings for embedding
        self.employees = employees_data
        self.employee_docs = [format_employee_for_embedding(emp) for emp in self.employees]
        
        # Create the vector store
        self.index, self.doc_map = self._create_vector_store()
        print("✅ RAG System Initialized: FAISS index and models are ready.")

    def _create_vector_store(self):
        """Creates a FAISS index from employee documents."""
        # Generate embeddings for all employee documents
        embeddings = self.embedding_model.encode(self.employee_docs, convert_to_tensor=False)
        embedding_dim = embeddings.shape[1]
        
        # Create a FAISS index for fast similarity search
        index = faiss.IndexFlatL2(embedding_dim)
        index.add(np.array(embeddings, dtype='float32'))
        
        # Map from index ID back to the original employee data
        doc_map = {i: self.employees[i] for i in range(len(self.employees))}
        
        return index, doc_map

    def retrieve(self, query: str, k: int = 4) -> List[Dict]:
        """Retrieves the top-k most relevant employees using vector search."""
        query_embedding = self.embedding_model.encode([query])
        _, indices = self.index.search(np.array(query_embedding, dtype='float32'), k)
        
        # Return the full data for the retrieved employees
        return [self.doc_map[i] for i in indices[0]]

    def generate(self, query: str, retrieved_employees: List[Dict]) -> str:
        """Generates a natural language response using the Gemini API."""
        context_str = "\n---\n".join([format_employee_for_embedding(emp) for emp in retrieved_employees])
        
        system_prompt = (
            "You are an intelligent HR assistant. Your task is to help managers find the best employees for a project "
            "based on their query and the provided employee profiles. Analyze the user's query and the context below. "
            "Synthesize the information to provide a helpful, natural language recommendation. "
            "Highlight the key strengths of each recommended candidate as they relate to the query. "
            "If a candidate's availability is 'on_project', mention this as a potential constraint."
        )

        user_prompt = (
            f"User Query: '{query}'\n\n"
            f"Here are the most relevant employee profiles I found:\n"
            f"---CONTEXT---\n{context_str}\n---END CONTEXT---"
            "\nBased on this, please provide your recommendation."
        )
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            response = self.generation_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error during LLM generation: {e}")
            return "I'm sorry, I encountered an error while generating a response. Please check the API key and configuration."