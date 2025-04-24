import os
import gdown  # Use gdown instead of google_drive_downloader

def download_model():
    model_path = "plant_disease_model.h5"  # Path where the model will be saved
    
    # Check if the model already exists
    if not os.path.exists(model_path):
        print("Model not found. Downloading from Google Drive...")
        
        # Replace with gdown.download and use the file ID
        gdown.download(
            id="1kcMD1FWnCdtWkvgW6Qhh63kmGU1BpluV",  # Actual file ID from Google Drive
            output=model_path,  # Path where the model file will be saved
            quiet=False  # Set to False to see download progress
        )
        
        print("Model downloaded successfully.")
    else:
        print("Model already exists. Skipping download.")

if __name__ == "__main__":
    download_model()
