# gui_app.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import requests
import base64
import io
import threading
import json


class SkinCancerDetectionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skin Cancer Detection - AI Diagnostic Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # API Configuration
        self.api_url = "http://127.0.0.1:5000"

        # Variables
        self.current_image = None
        self.current_image_path = None

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Configure colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#f39c12"
        self.danger_color = "#e74c3c"

        self.root.configure(bg=self.bg_color)

        self.create_widgets()
        self.check_api_connection()

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = tk.Label(main_frame, text="🔬 Skin Cancer Detection System",
                               font=("Arial", 24, "bold"), bg=self.bg_color, fg=self.primary_color)
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Subtitle
        subtitle_label = tk.Label(main_frame, text="AI-powered dermatological analysis for early detection",
                                  font=("Arial", 12), bg=self.bg_color, fg="#7f8c8d")
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))

        # Left panel - Image upload and display
        left_frame = ttk.LabelFrame(main_frame, text="Image Upload", padding="15")
        left_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Upload button
        self.upload_btn = tk.Button(left_frame, text="📁 Select Image",
                                    command=self.upload_image, font=("Arial", 12, "bold"),
                                    bg=self.secondary_color, fg="white", relief="flat",
                                    padx=20, pady=10, cursor="hand2")
        self.upload_btn.pack(pady=(0, 15))

        # Image display area
        self.image_frame = tk.Frame(left_frame, bg="white", relief="sunken", bd=2)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self.image_frame,
                                    text="No image selected\n\nSupported formats:\nJPG, PNG, BMP, GIF",
                                    bg="white", fg="#bdc3c7", font=("Arial", 11))
        self.image_label.pack(expand=True)

        # File info
        self.file_info_label = tk.Label(left_frame, text="", font=("Arial", 9),
                                        bg=self.bg_color, fg="#7f8c8d")
        self.file_info_label.pack(pady=(10, 0))

        # Right panel - Analysis and results
        right_frame = ttk.LabelFrame(main_frame, text="Analysis & Results", padding="15")
        right_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)

        # Analyze button
        self.analyze_btn = tk.Button(right_frame, text="🔍 Analyze Image",
                                     command=self.analyze_image, font=("Arial", 12, "bold"),
                                     bg=self.success_color, fg="white", relief="flat",
                                     padx=20, pady=10, cursor="hand2", state="disabled")
        self.analyze_btn.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        # Progress bar
        self.progress = ttk.Progressbar(right_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Status label
        self.status_label = tk.Label(right_frame, text="Ready to analyze",
                                     font=("Arial", 10), bg=self.bg_color, fg="#7f8c8d")
        self.status_label.grid(row=2, column=0, pady=(0, 15))

        # Results frame
        self.results_frame = ttk.LabelFrame(right_frame, text="Prediction Results", padding="10")
        self.results_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.results_frame.columnconfigure(0, weight=1)

        # Main prediction
        self.main_prediction_label = tk.Label(self.results_frame, text="",
                                              font=("Arial", 14, "bold"), bg=self.bg_color)
        self.main_prediction_label.grid(row=0, column=0, pady=(0, 10), sticky="ew")

        # Confidence
        self.confidence_label = tk.Label(self.results_frame, text="",
                                         font=("Arial", 12), bg=self.bg_color)
        self.confidence_label.grid(row=1, column=0, pady=(0, 15), sticky="ew")

        # Detailed results
        self.details_frame = tk.Frame(self.results_frame, bg=self.bg_color)
        self.details_frame.grid(row=2, column=0, sticky="ew")
        self.details_frame.columnconfigure(0, weight=1)

        # API status
        self.api_status_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.api_status_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        self.api_status_label = tk.Label(self.api_status_frame, text="🔴 API Status: Checking...",
                                         font=("Arial", 10), bg=self.bg_color, fg="#e74c3c")
        self.api_status_label.pack()

        # Disclaimer
        disclaimer_text = ("⚠️ DISCLAIMER: This tool is for educational purposes only. "
                           "Always consult with healthcare professionals for medical advice.")
        disclaimer_label = tk.Label(main_frame, text=disclaimer_text,
                                    font=("Arial", 9), bg="#fff3cd", fg="#856404",
                                    wraplength=850, justify="center", padx=10, pady=8, relief="solid", bd=1)
        disclaimer_label.grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky="ew")

    def check_api_connection(self):
        """Check if Flask API is running"""

        def check():
            try:
                response = requests.get(f"{self.api_url}/health", timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('model_loaded', False):
                        self.api_status_label.config(text="🟢 API Status: Connected & Model Loaded",
                                                     fg=self.success_color)
                    else:
                        self.api_status_label.config(text="🟡 API Status: Connected but Model Not Loaded",
                                                     fg=self.warning_color)
                else:
                    self.api_status_label.config(text="🔴 API Status: Connection Error", fg=self.danger_color)
            except Exception as e:
                self.api_status_label.config(text="🔴 API Status: Server Unavailable", fg=self.danger_color)

        # Run check in background thread
        threading.Thread(target=check, daemon=True).start()

    def upload_image(self):
        """Handle image upload"""
        file_types = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]

        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=file_types
        )

        if file_path:
            try:
                # Load and display image
                image = Image.open(file_path)
                self.current_image = image
                self.current_image_path = file_path

                # Display image in GUI
                self.display_image(image)

                # Update file info
                file_size = len(open(file_path, 'rb').read())
                file_size_mb = file_size / (1024 * 1024)
                self.file_info_label.config(
                    text=f"File: {file_path.split('/')[-1]} | Size: {file_size_mb:.2f} MB | Dimensions: {image.size}")

                # Enable analyze button
                self.analyze_btn.config(state="normal")
                self.status_label.config(text="Image loaded successfully. Ready to analyze.")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")

    def display_image(self, image):
        """Display image in the GUI"""
        # Calculate display size (maintain aspect ratio)
        display_size = (300, 300)
        image_copy = image.copy()
        image_copy.thumbnail(display_size, Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(image_copy)

        # Update label
        self.image_label.config(image=photo, text="")
        self.image_label.image = photo  # Keep a reference

    def analyze_image(self):
        """Send image to API for analysis"""
        if not self.current_image:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        # Start analysis in background thread
        threading.Thread(target=self._perform_analysis, daemon=True).start()

    def _perform_analysis(self):
        """Perform the actual analysis (runs in background thread)"""
        try:
            # Update UI
            self.root.after(0, self._update_ui_analyzing)

            # Convert image to base64
            buffered = io.BytesIO()
            self.current_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Send to API
            payload = {"image": img_str}
            response = requests.post(f"{self.api_url}/predict", json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.root.after(0, lambda: self._display_results(result['prediction']))
                else:
                    self.root.after(0, lambda: self._display_error(result.get('error', 'Unknown error')))
            else:
                error_msg = response.json().get('error', 'Server error') if response.content else 'Server unavailable'
                self.root.after(0, lambda: self._display_error(error_msg))

        except requests.exceptions.RequestException as e:
            self.root.after(0, lambda: self._display_error(f"Connection error: {str(e)}"))
        except Exception as e:
            self.root.after(0, lambda: self._display_error(f"Analysis error: {str(e)}"))

    def _update_ui_analyzing(self):
        """Update UI to show analysis in progress"""
        self.progress.start()
        self.analyze_btn.config(state="disabled")
        self.status_label.config(text="Analyzing image... Please wait.")

        # Clear previous results
        for widget in self.details_frame.winfo_children():
            widget.destroy()
        self.main_prediction_label.config(text="")
        self.confidence_label.config(text="")

    def _display_results(self, prediction):
        """Display analysis results"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        self.status_label.config(text="Analysis completed successfully.")

        # Main prediction
        predicted_class = prediction['predicted_class']
        confidence = prediction['confidence']

        self.main_prediction_label.config(text=f"Prediction: {predicted_class}")

        # Set confidence color and risk level based on prediction
        if predicted_class.lower() == 'malignant':
            if confidence >= 0.8:
                confidence_color = self.danger_color
                risk_level = "HIGH RISK"
                recommendation = "⚠️ URGENT: Consult a dermatologist immediately"
            elif confidence >= 0.6:
                confidence_color = self.warning_color
                risk_level = "MODERATE RISK"
                recommendation = "⚠️ Recommended: Schedule dermatologist consultation"
            else:
                confidence_color = self.warning_color
                risk_level = "LOW-MODERATE RISK"
                recommendation = "Consider dermatologist consultation for confirmation"
        else:  # Benign
            if confidence >= 0.8:
                confidence_color = self.success_color
                risk_level = "LOW RISK"
                recommendation = "✓ Likely benign, but monitor for changes"
            elif confidence >= 0.6:
                confidence_color = self.warning_color
                risk_level = "UNCERTAIN"
                recommendation = "Consider professional evaluation for peace of mind"
            else:
                confidence_color = self.warning_color
                risk_level = "UNCERTAIN"
                recommendation = "Professional evaluation recommended"

        self.confidence_label.config(text=f"Confidence: {confidence:.1%} | Risk Level: {risk_level}",
                                     fg=confidence_color)

        # Add recommendation
        recommendation_label = tk.Label(self.details_frame, text=recommendation,
                                        font=("Arial", 10, "bold"), bg=self.bg_color,
                                        fg=confidence_color, wraplength=400, justify="center")
        recommendation_label.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        # Add separator
        separator = tk.Frame(self.details_frame, height=2, bg="#ddd")
        separator.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Detailed probabilities
        tk.Label(self.details_frame, text="Classification Breakdown:", font=("Arial", 11, "bold"),
                 bg=self.bg_color).grid(row=2, column=0, sticky="w", pady=(0, 5))

        for i, prob_data in enumerate(prediction['all_probabilities']):  # Show both classes
            class_name = prob_data['class']
            probability = prob_data['probability']
            description = prob_data.get('description', '')

            row_frame = tk.Frame(self.details_frame, bg=self.bg_color)
            row_frame.grid(row=i + 3, column=0, sticky="ew", pady=2)
            row_frame.columnconfigure(1, weight=1)

            # Class name with color coding
            class_color = self.danger_color if class_name.lower() == 'malignant' else self.success_color
            tk.Label(row_frame, text=class_name, font=("Arial", 10, "bold"),
                     bg=self.bg_color, fg=class_color, width=12, anchor="w").grid(row=0, column=0, sticky="w")

            # Progress bar for probability
            prob_frame = tk.Frame(row_frame, bg=self.bg_color)
            prob_frame.grid(row=0, column=1, sticky="ew", padx=(10, 0))
            prob_frame.columnconfigure(0, weight=1)

            progress_bar = ttk.Progressbar(prob_frame, length=200, mode='determinate')
            progress_bar.grid(row=0, column=0, sticky="ew")
            progress_bar['value'] = probability * 100

            # Percentage text
            tk.Label(prob_frame, text=f"{probability:.1%}", font=("Arial", 9, "bold"),
                     bg=self.bg_color).grid(row=0, column=1, padx=(10, 0))

            # Description
            if description:
                desc_label = tk.Label(self.details_frame, text=description,
                                      font=("Arial", 8), bg=self.bg_color, fg="#666",
                                      wraplength=450, justify="left")
                desc_label.grid(row=i + 4, column=0, sticky="ew", padx=(20, 0), pady=(0, 5))

    def _display_error(self, error_message):
        """Display error message"""
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        self.status_label.config(text=f"Error: {error_message}")

        messagebox.showerror("Analysis Error", f"Failed to analyze image:\n{error_message}")


def main():
    root = tk.Tk()
    app = SkinCancerDetectionGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()