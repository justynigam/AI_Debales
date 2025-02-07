# **Custom Chatbot with LangChain and Flask**

This project is a custom chatbot that leverages **LangChain**, **HuggingFace embeddings**, and **FAISS vector storage** to provide conversational responses based on data extracted from a website. The chatbot is exposed as a **RESTful API** using **Flask**, making it easy to integrate into other applications.

---

## **Features**
- **Web Scraping**: Extracts data from a specified URL using LangChain's `WebBaseLoader`.
- **Embeddings**: Uses **HuggingFace embeddings** to convert text into vector representations.
- **Vector Storage**: Stores embeddings in a **FAISS vector store** for efficient similarity search.
- **Conversational Memory**: Maintains conversation history using LangChain's `ConversationBufferMemory`.
- **RESTful API**: Exposes the chatbot as a **Flask API** for easy integration.
- **Customizable**: Supports different HuggingFace models and embedding configurations.

---

## **Technologies Used**
- **LangChain**: For building the conversational chain and handling embeddings.
- **HuggingFace Transformers**: For generating embeddings and powering the chatbot's language model.
- **FAISS**: For efficient vector storage and similarity search.
- **Flask**: For creating the RESTful API.
- **Python**: The core programming language.

---

## **LLM Used**
The chatbot uses **HuggingFace's `google/flan-t5-large`** as its language model. This model is fine-tuned for text generation tasks and provides high-quality responses for conversational AI.

---

## **Installation**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### **Step 2: Install Dependencies**
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **Step 3: Set HuggingFace API Token**
1. Go to [HuggingFace Hub](https://huggingface.co/settings/tokens) and generate an API token.
2. Set the token as an environment variable:
   - **Windows**:
     ```cmd
     set HUGGINGFACEHUB_API_TOKEN=your_api_token_here
     ```
   - **Linux/macOS**:
     ```bash
     export HUGGINGFACEHUB_API_TOKEN=your_api_token_here
     ```

---

## **Usage**

### **Step 1: Run the Flask Server**
Start the Flask server:
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`.

### **Step 2: Test the API**
You can interact with the chatbot using `curl`, Postman, or any HTTP client.

#### **Example Request**
Send a POST request to the `/chat` endpoint with a JSON payload:
```bash
curl -X POST http://127.0.0.1:5000/chat \
-H "Content-Type: application/json" \
-d '{"message": "What technical courses are available?"}'
```

#### **Example Response**
```json
{
  "response": "The available technical courses include Python programming, Machine Learning, and Data Science."
}
```

---

## **How It Works**

### **Step 1: Data Extraction**
The chatbot extracts data from a specified URL using LangChain's `WebBaseLoader`.

### **Step 2: Embeddings**
The extracted data is converted into embeddings using HuggingFace's `sentence-transformers/all-mpnet-base-v2`.

### **Step 3: Vector Storage**
The embeddings are stored in a FAISS vector store for efficient retrieval.

### **Step 4: Conversation Chain**
A conversational chain is initialized using HuggingFace's `google/flan-t5-large` model and the FAISS vector store.

### **Step 5: API Endpoint**
The chatbot is exposed as a RESTful API using Flask. Users can send messages to the `/chat` endpoint and receive responses.

---

## **Customization**

### **Change the Embedding Model**
Modify the `model_name` parameter in the `create_vector_store` function:
```python
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

### **Change the Language Model**
Replace the HuggingFace model (`google/flan-t5-large`) with any other supported model:
```python
llm = HuggingFaceEndpoint(
    repo_id="another-model-name",
    huggingfacehub_api_token=huggingfacehub_api_token,
    temperature=0.7,
    max_length=512
)
```

### **Add More Endpoints**
Extend the Flask API by adding more routes in `app.py`.

---

## **Contributing**
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Screenshots**
![Screenshot (172)](https://github.com/user-attachments/assets/910b4a21-a40b-4137-823c-a2c1c0f29730)

![Screenshot 2025-02-07 232812](https://github.com/user-attachments/assets/29d35276-bcc1-4bd3-aba9-a909bc7b70c5)




---

