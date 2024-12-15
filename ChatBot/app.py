from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load an NLP model (e.g., Hugging Face transformers)
chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_message = data.get("message", "")
    response = chatbot_pipeline(user_message)[0]['generated_text']
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
