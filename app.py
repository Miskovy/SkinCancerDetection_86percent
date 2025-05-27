from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from model_loader import predict_skin_cancer # Import from your model_loader.py

# --- Configuration ---
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key" # Important for session management, change it

# --- Ensure upload folder exists ---
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def upload_and_predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
        except Exception as e:
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

        try:
            # Get prediction from the model_loader
            label, confidence = predict_skin_cancer(filepath)

            # Optionally remove the file after prediction
            # os.remove(filepath)

            if "Error:" in label: # Check if prediction itself returned an error
                 return jsonify({'error': label, 'confidence': confidence}), 500

            return jsonify({'prediction': label, 'confidence': f'{confidence:.4f}'})
        except Exception as e:
            # Clean up uploaded file if an error occurs during prediction
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error during prediction: {str(e)}'}), 500
        finally:
            # Ensure file is removed if it still exists and you want to clean up
            # (Be careful if multiple requests might use the same filename concurrently
            # if not using unique filenames)
            if os.path.exists(filepath) and True: # Set to False to keep files
                try:
                    pass # os.remove(filepath) # Commented out to allow GUI to display it
                except Exception as e:
                    print(f"Could not remove file {filepath}: {e}")

    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    # Make sure to run this with a different port if your GUI uses 5000 by default,
    # or configure the GUI to use this port.
    app.run(debug=True, port=5001) # Running on port 5001 to avoid conflict if GUI uses 5000