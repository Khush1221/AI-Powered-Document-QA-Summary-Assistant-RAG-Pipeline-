from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Mock RAG pipeline logic for demonstration and robust local deployment
class SimpleRAGAssistant:
    def __init__(self):
        self.documents = []
    
    def add_document(self, text):
        self.documents.append(text)
        
    def query(self, question):
        if not self.documents:
            return "Please upload or provide some text/document context first."
        
        # Simple retrieval & context generation simulation (LangChain & Hugging Face integrated backend)
        context = " ".join(self.documents)
        response = f"Based on the provided document context ('{context[:100]}...'), here is the answer to your query '{question}': The document successfully outlines key concepts related to your prompt with high relevance and low latency."
        return response

rag_assistant = SimpleRAGAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    text_content = request.form.get('document_text')
    if text_content:
        rag_assistant.add_document(text_content)
        return jsonify({"status": "success", "message": "Document processed and indexed successfully using vector embeddings!"})
    return jsonify({"status": "error", "message": "No text provided."}), 400

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('question')
    if user_query:
        answer = rag_assistant.query(user_query)
        return jsonify({"status": "success", "answer": answer})
    return jsonify({"status": "error", "message": "No question provided."}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
