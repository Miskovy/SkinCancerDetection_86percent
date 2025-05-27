import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import requests # To send requests to the Flask API
import os

# --- Configuration ---
FLASK_API_URL = "http://127.0.0.1:5001/predict" # URL of your Flask API
TEMP_IMAGE_DIR = "static/uploads/" # To access the image displayed after upload

# Ensure the temporary directory exists (though Flask app should create it)
if not os.path.exists(TEMP_IMAGE_DIR):
    os.makedirs(TEMP_IMAGE_DIR)


class SkinCancerApp:
    def __init__(self, master):
        self.master = master
        master.title("Skin Cancer Detector")
        master.geometry("600x500") # Adjusted size

        # --- Style ---
        style = ttk.Style()
        style.theme_use('clam') # or 'alt', 'default', 'classic'

        # --- Title ---
        self.title_label = ttk.Label(master, text="Skin Cancer Detection", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        # --- Image Display ---
        self.image_label = ttk.Label(master, text="Upload an image to predict")
        self.image_label.pack(pady=10)
        self.img_display_width = 300
        self.img_display_height = 300

        # --- Upload Button ---
        self.upload_button = ttk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        # --- Prediction Result ---
        self.result_label_var = tk.StringVar()
        self.result_label_var.set("Prediction: N/A")
        self.result_label = ttk.Label(master, textvariable=self.result_label_var, font=("Helvetica", 12))
        self.result_label.pack(pady=5)

        self.confidence_label_var = tk.StringVar()
        self.confidence_label_var.set("Confidence: N/A")
        self.confidence_label = ttk.Label(master, textvariable=self.confidence_label_var, font=("Helvetica", 12))
        self.confidence_label.pack(pady=5)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.uploaded_image_path = None # To store the path of the uploaded image for display

    def upload_image(self):
        self.status_var.set("Opening file dialog...")
        filepath = filedialog.askopenfilename(
            title="Select Skin Lesion Image",
            filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png"), ("all files", "*.*"))
        )
        if not filepath:
            self.status_var.set("No image selected.")
            return

        self.status_var.set(f"Selected: {os.path.basename(filepath)}")
        self.uploaded_image_path = filepath # Store for display

        # Display the image
        try:
            img = Image.open(filepath)
            img.thumbnail((self.img_display_width, self.img_display_height)) # Resize for display
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo # Keep a reference!
        except Exception as e:
            messagebox.showerror("Image Display Error", f"Could not display image: {e}")
            self.status_var.set("Error displaying image.")
            self.image_label.config(image=None, text="Error displaying image") # Clear image
            return

        # --- Call the API for prediction ---
        self.predict_image(filepath)

    def predict_image(self, filepath):
        self.status_var.set(f"Sending '{os.path.basename(filepath)}' to API for prediction...")
        self.result_label_var.set("Prediction: Processing...")
        self.confidence_label_var.set("Confidence: ...")
        self.master.update_idletasks() # Update GUI before blocking call

        try:
            with open(filepath, 'rb') as f:
                files = {'file': (os.path.basename(filepath), f, 'image/jpeg')} # Or image/png
                response = requests.post(FLASK_API_URL, files=files, timeout=20) # Added timeout
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

            data = response.json()
            if 'error' in data:
                prediction_text = f"Prediction: Error - {data['error']}"
                confidence_text = f"Confidence: {data.get('confidence', 'N/A')}"
                messagebox.showerror("API Error", data['error'])
            else:
                prediction_text = f"Prediction: {data['prediction']}"
                confidence_text = f"Confidence: {data['confidence']}"
            self.result_label_var.set(prediction_text)
            self.confidence_label_var.set(confidence_text)
            self.status_var.set("Prediction complete.")

        except requests.exceptions.ConnectionError:
            error_msg = "API Connection Error: Could not connect to the Flask API. Is it running?"
            self.result_label_var.set("Prediction: API Connection Error")
            self.confidence_label_var.set("Confidence: N/A")
            self.status_var.set("Error: API connection failed.")
            messagebox.showerror("API Error", error_msg)
        except requests.exceptions.Timeout:
            error_msg = "API Timeout: The request to the API timed out."
            self.result_label_var.set("Prediction: API Timeout")
            self.confidence_label_var.set("Confidence: N/A")
            self.status_var.set("Error: API request timed out.")
            messagebox.showerror("API Error", error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"API Request Error: {e}"
            self.result_label_var.set(f"Prediction: API Error")
            self.confidence_label_var.set("Confidence: N/A")
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("API Error", error_msg)
        except Exception as e: # Catch any other errors
            error_msg = f"An unexpected error occurred: {e}"
            self.result_label_var.set("Prediction: Failed")
            self.confidence_label_var.set("Confidence: N/A")
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Error", error_msg)


if __name__ == '__main__':
    root = tk.Tk()
    app_gui = SkinCancerApp(root)
    root.mainloop()