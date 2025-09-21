from flask import Flask, request, jsonify
from flask_cors import CORS
import with_antiSpoofing  # import your existing file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get JSON input from POST
    user_input = data.get("input", "")
    
    # Call your preexisting function
    result = with_antiSpoofing.run_model(user_input)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # accessible on LAN
