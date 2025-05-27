import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# --- Configuration ---
IMG_WIDTH, IMG_HEIGHT = 224, 224  # MobileNetV2 default input size, adjust if different
MODEL_PATH = 'mobilenetv2_checkpoint.h5' # Replace with your checkpoint file name

# --- Load the Model ---
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(img_path):
    """Loads and preprocesses an image for MobileNetV2."""
    try:
        img = image.load_img(img_path, target_size=(IMG_WIDTH, IMG_HEIGHT))
        img_array = image.img_to_array(img)
        img_array_expanded_dims = np.expand_dims(img_array, axis=0)
        # MobileNetV2 preprocessing function (adjust if you used a different one during training)
        return tf.keras.applications.mobilenet_v2.preprocess_input(img_array_expanded_dims)
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def predict_skin_cancer(img_path):
    """
    Predicts if an image contains skin cancer.
    Returns a tuple: (prediction_label, confidence_score)
    """
    if model is None:
        return "Error: Model not loaded.", 0.0

    processed_img = preprocess_image(img_path)
    if processed_img is None:
        return "Error: Image preprocessing failed.", 0.0

    try:
        prediction = model.predict(processed_img)
        # Assuming your model outputs probabilities for two classes:
        # prediction[0][0] for 'not cancer' and prediction[0][1] for 'cancer'
        # Or if it's a single output neuron (sigmoid):
        # prediction[0][0] > 0.5 for 'cancer'

        # --- Adjust this logic based on your model's output layer ---
        # Example for a 2-class output (softmax):
        # class_names = ['Benign', 'Malignant'] # Or 'Not Cancer', 'Cancer'
        # predicted_class_index = np.argmax(prediction[0])
        # confidence = prediction[0][predicted_class_index]
        # predicted_label = class_names[predicted_class_index]

        # Example for a single sigmoid output (0 for benign, 1 for malignant)
        confidence = prediction[0][0]
        if confidence > 0.5: # Adjust threshold as needed
            predicted_label = "Malignant (Cancer)"
            confidence_score = confidence
        else:
            predicted_label = "Benign (Not Cancer)"
            confidence_score = 1 - confidence # Confidence in being benign

        return predicted_label, float(confidence_score)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return f"Error: Prediction failed - {e}", 0.0

if __name__ == '__main__':
    # Test the prediction (replace 'test_image.jpg' with an actual image path)
    # Create a dummy image file for testing if you don't have one readily available
    try:
        from PIL import Image
        dummy_image = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), color = 'red')
        dummy_image_path = "dummy_test_image.jpg"
        dummy_image.save(dummy_image_path)
        print(f"Testing with a dummy image: {dummy_image_path}")
        label, score = predict_skin_cancer(dummy_image_path)
        print(f"Prediction: {label}, Confidence: {score:.4f}")
        import os
        os.remove(dummy_image_path) # Clean up dummy image
    except ImportError:
        print("Pillow (PIL) is not installed. Skipping dummy image test.")
    except Exception as e:
        print(f"Error in dummy image test: {e}")