from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_huggingface import HuggingFaceEndpoint
import os

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Global variables for vector store and conversation chain
vector_store = None
qa_chain = None

@app.route('/')
def index():
    return "Welcome to the Chatbot API. Use the /chat endpoint to interact with the chatbot."



# Step 1: Extract data from the URL
def extract_data(url):
    print("Extracting data from URL...")
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        print(f"Extracted {len(documents)} documents.")
        return documents
    except Exception as e:
        print(f"Error extracting data: {e}")
        return []


# Step 2: Create embeddings and store in a vector store
def create_vector_store(documents, model_name="sentence-transformers/all-mpnet-base-v2"):
    print("Creating embeddings and vector store...")
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        vector_store = FAISS.from_documents(documents, embedding_model)
        vector_store.save_local("vector_store")
        print("Vector store created and saved.")
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None


# Step 3: Initialize the conversation chain
def initialize_conversation_chain(vector_store):
    print("Initializing conversation chain...")

    # Set HuggingFace API token
    huggingfacehub_api_token = "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"
    print(f"HuggingFace API Token: {huggingfacehub_api_token}")  # Debug print
    if not huggingfacehub_api_token:
        raise ValueError("HUGGINGFACEHUB_API_TOKEN environment variable not set.")

    # Initialize HuggingFace LLM
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-large",
        huggingfacehub_api_token=huggingfacehub_api_token,
        temperature=0.7,  # Pass temperature explicitly
        max_length=512  # Pass max_length explicitly
    )

    # Initialize memory and conversation chain
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    print("Conversation chain initialized.")
    return qa_chain


# Step 4: Flask RESTful API for conversation
class ChatbotAPI(Resource):
    def post(self):
        global qa_chain
        data = request.get_json()
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        try:
            response = qa_chain({"question": user_input})
            return jsonify({"response": response["answer"]})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Initialize the chatbot
def initialize_chatbot():
    global vector_store, qa_chain
    url = "https://brainlox.com/courses/category/technical"

    # Step 1: Extract data
    documents = extract_data(url)
    print(f"Extracted documents: {len(documents)}")

    # Step 2: Create vector store
    vector_store = create_vector_store(documents)
    print("Vector store created successfully.")

    # Step 3: Initialize conversation chain
    qa_chain = initialize_conversation_chain(vector_store)
    print("Conversation chain initialized successfully.")


# Add the API resource
api.add_resource(ChatbotAPI, "/chat")

import requests

url = "http://127.0.0.1:5000/chat"
headers = {"Content-Type": "application/json"}
data = {"message": "Hello, how can I help you?"}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Chatbot response:", response.json()["response"])
else:
    print("Error:", response.json()["error"])

# Run the Flask app
if __name__ == "__main__":
    print("Initializing chatbot...")
    initialize_chatbot()
    print("Chatbot initialized. Starting Flask server...")
    app.run(debug=True)