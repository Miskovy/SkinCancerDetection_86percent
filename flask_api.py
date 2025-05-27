# flask_api.py
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
MODEL_PATH = 'mobilenetv2_checkpoint.h5'  # Updated to match your checkpoint name

# Binary classification class names (based on your training code)
CLASS_NAMES = [
    'Benign',
    'Malignant'
]

# Detailed explanation for each class
CLASS_DESCRIPTIONS = {
    'Benign': 'Non-cancerous skin lesion (nv - Melanocytic nevus, vasc - Vascular lesion, df - Dermatofibroma)',
    'Malignant': 'Potentially cancerous lesion (mel - Melanoma, bkl - Benign keratosis-like, bcc - Basal cell carcinoma, akiec - Actinic keratosis)'
}

# Load the trained model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
    print(f"Model input shape: {model.input_shape}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None


def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess the image for model prediction
    Matches the preprocessing used in training with MobileNetV2
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Resize image to match training target size
    image = image.resize(target_size)

    # Convert to numpy array
    img_array = np.array(image)

    # Normalize pixel values (rescale=1./255 as in training)
    img_array = img_array.astype('float32') / 255.0

    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def predict_skin_cancer(image):
    """Make prediction on the preprocessed image"""
    if model is None:
        return None, "Model not loaded"

    try:
        # Preprocess image
        processed_image = preprocess_image(image)

        # Make prediction
        predictions = model.predict(processed_image)

        # Get the predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])

        # Get all class probabilities with descriptions
        class_probabilities = []
        for i, prob in enumerate(predictions[0]):
            class_name = CLASS_NAMES[i] if i < len(CLASS_NAMES) else f'Class {i}'
            class_probabilities.append({
                'class': class_name,
                'probability': float(prob),
                'description': CLASS_DESCRIPTIONS.get(class_name, 'No description available')
            })

        # Sort by probability
        class_probabilities.sort(key=lambda x: x['probability'], reverse=True)

        predicted_class = CLASS_NAMES[predicted_class_idx] if predicted_class_idx < len(
            CLASS_NAMES) else f'Class {predicted_class_idx}'

        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'all_probabilities': class_probabilities
        }, None

    except Exception as e:
        return None, str(e)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if image data is provided
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # Decode base64 image
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))

        # Make prediction
        result, error = predict_skin_cancer(image)

        if error:
            return jsonify({'error': error}), 500

        return jsonify({
            'success': True,
            'prediction': result
        })

    except Exception as e:
        return jsonify({'error': f'Error processing image: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })


if __name__ == '__main__':
    print("Starting Flask API server...")
    print("Model loaded:", model is not None)
    app.run(debug=True, host='127.0.0.1', port=5000)