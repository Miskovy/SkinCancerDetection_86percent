# setup_and_run.py
import subprocess
import sys
import os
import threading
import time


def install_requirements():
    """Install required packages"""
    requirements = [
        'flask==2.3.3',
        'tensorflow==2.13.0',
        'pillow==10.0.0',
        'numpy==1.24.3',
        'requests==2.31.0'
    ]

    print("Installing required packages...")
    for package in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False

    print("All packages installed successfully!")
    return True


def start_flask_server():
    """Start the Flask API server"""
    print("Starting Flask API server...")
    os.system("python flask_api.py")


def start_gui():
    """Start the Tkinter GUI"""
    print("Starting GUI application...")
    time.sleep(3)  # Wait for Flask server to start
    os.system("python gui_app.py")


def main():
    print("=" * 60)
    print("SKIN CANCER DETECTION - SETUP AND LAUNCHER")
    print("=" * 60)

    # Check if model file exists
    model_path = "skin_cancer_model.h5"
    if not os.path.exists(model_path):
        print(f"\n⚠️  WARNING: Model file '{model_path}' not found!")
        print("Please make sure your trained model file is in the same directory")
        print("and update the MODEL_PATH in flask_api.py if needed.\n")

    # Install requirements
    choice = input("Do you want to install required packages? (y/n): ").lower()
    if choice == 'y':
        if not install_requirements():
            print("Failed to install requirements. Please install manually.")
            return

    print("\n" + "=" * 60)
    print("STARTING APPLICATION")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Flask API server will start first")
    print("2. GUI application will start after 3 seconds")
    print("3. Keep both windows open for the application to work")
    print("4. Use Ctrl+C in the terminal to stop the server")
    print("\nStarting in 3 seconds...")

    time.sleep(3)

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()

    # Start GUI
    start_gui()


if __name__ == "__main__":
    main()

# Alternative launcher scripts for manual execution:

# start_server.py
"""
Simple script to start only the Flask server
"""
import os

if __name__ == "__main__":
    print("Starting Flask API Server...")
    print("Server will run on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop")
    os.system("python flask_api.py")

# start_gui.py
"""
Simple script to start only the GUI
"""
import os

if __name__ == "__main__":
    print("Starting Tkinter GUI...")
    print("Make sure Flask server is running first!")
    os.system("python gui_app.py")