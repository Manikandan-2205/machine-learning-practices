import os
import shutil
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, pipeline

app = Flask(__name__)

# Directory and model name
MODEL_DIR = "models/DialoGPT-medium"
MODEL_NAME = "microsoft/DialoGPT-medium"
MESSAGE_LOG = "message_log.txt"

# Function to check if model is fully downloaded
def is_model_downloaded(model_dir):
    required_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json", "vocab.json"]
    return all(os.path.exists(os.path.join(model_dir, file)) for file in required_files)

# Function to force re-download the model if needed
def force_redownload_model():
    if os.path.exists(MODEL_DIR):
        print(f"Deleting the existing model directory at {MODEL_DIR}...")
        shutil.rmtree(MODEL_DIR)
        print("Model directory deleted.")

# Function to log messages to a file
def log_message(message):
    with open(MESSAGE_LOG, "a") as f:
        f.write(message + "\n")

# Ensure the model directory exists
os.makedirs(MODEL_DIR, exist_ok=True)

# Download the model if not already downloaded
if not is_model_downloaded(MODEL_DIR):
    # Optionally delete the directory if forcing a re-download
    force_redownload_model()

    print(f"Downloading model from {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = pipeline("text-generation", model=MODEL_NAME, tokenizer=tokenizer)

    # Save the downloaded model and tokenizer locally
    print(f"Saving model and tokenizer to {MODEL_DIR}...")
    tokenizer.save_pretrained(MODEL_DIR)
    model.save_pretrained(MODEL_DIR)
    print(f"Model and tokenizer have been successfully saved to {MODEL_DIR}.")
else:
    print(f"Model is already downloaded in {MODEL_DIR}.")

# Load the model and tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = pipeline("text-generation", model=MODEL_DIR, tokenizer=tokenizer)
    print(f"Model loaded successfully from {MODEL_DIR}.")
except Exception as e:
    print(f"Error loading the model: {e}")
    exit(1)

@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Please enter a valid message."})

        # Log user message
        log_message(f":User  {user_message}")

        # Generate a response
        responses = model(user_message, max_length=50, num_return_sequences=1)
        bot_response = responses[0]["generated_text"]

        # Log bot response
        log_message(f"Bot: {bot_response}")

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Ensure message log file exists
    if not os.path.exists(MESSAGE_LOG):
        with open(MESSAGE_LOG, "w") as f:
            f.write("Message Log\n")
    
    app.run(debug=True)
