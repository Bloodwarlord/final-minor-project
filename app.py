from flask import Flask, request, jsonify
import cv2
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image


model = load_model('base model files/Model.keras')


categories = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G',
    7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N',
    14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z',
    26: 'del', 27: 'nothing', 28: 'space'
}


DEFAULT_CONFIDENCE_THRESHOLD = 0.6


custom_thresholds = {
    'D': 0.30,
    'Z': 0.10,
    'T': 0.10,
    'F': 0.10,
    'E': 0.10
    
}

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image is provided
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        # Read image from request
        file = request.files['image'].read()
        npimg = np.frombuffer(file, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Preprocess the image
        img = cv2.resize(img, (200, 200))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)

        # Make prediction
        prediction = model.predict(img)
        predicted_class = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction)

        # Get the predicted alphabet
        predicted_alphabet = categories[predicted_class]

        # Determine the confidence threshold for the predicted alphabet
        threshold = custom_thresholds.get(predicted_alphabet, DEFAULT_CONFIDENCE_THRESHOLD)

        # Check if the confidence is above the threshold
        if confidence < threshold:
            return jsonify({
                "prediction": "UNkown Expression",
                "confidence": float(confidence)
            }), 200

        # Return prediction and confidence
        return jsonify({
            "prediction": predicted_alphabet,
            "confidence": float(confidence)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
