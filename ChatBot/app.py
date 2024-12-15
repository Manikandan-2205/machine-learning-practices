import os
import shutil
from flask import Flask, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)

# Directory and model name
MODEL_DIR = "models/DialoGPT-medium"
MODEL_NAME = "microsoft/DialoGPT-medium"

# Function to force re-download the model if the directory exists
def force_redownload_model():
    if os.path.exists(MODEL_DIR):
        print(f"Model directory exists. Deleting the existing model at {MODEL_DIR}...")
        shutil.rmtree(MODEL_DIR)  # Delete the model directory and its contents
        print("Existing model deleted. Re-downloading the model...")

# Check if the model directory exists and download if necessary
if not os.path.exists(MODEL_DIR) or not os.path.exists(os.path.join(MODEL_DIR, "pytorch_model.bin")):
    # Optionally force re-download the model
    force_redownload_model()
    
    # Create the directory if it doesn't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    try:
        # Download and save the model and tokenizer
        print(f"Downloading model from {MODEL_NAME}...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        
        # Save the downloaded model and tokenizer to the local directory
        print(f"Saving model and tokenizer to {MODEL_DIR}...")
        tokenizer.save_pretrained(MODEL_DIR)
        model.save_pretrained(MODEL_DIR)
        print(f"Model and tokenizer have been successfully saved to {MODEL_DIR}.")
    except Exception as e:
        print(f"Error occurred while downloading the model: {e}")
else:
    print(f"Model is already downloaded in {MODEL_DIR}.")

# Load the locally stored model
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)
    print(f"Model loaded from {MODEL_DIR}.")
except Exception as e:
    print(f"Error loading the model: {e}")

# Initialize the pipeline
chatbot_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"response": "Please enter a valid message."})

        # Generate a response
        responses = chatbot_pipeline(user_message, max_length=50, num_return_sequences=1)
        bot_response = responses[0]["generated_text"]

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
