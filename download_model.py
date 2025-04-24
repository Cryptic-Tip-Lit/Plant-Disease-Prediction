import os
from google_drive_downloader import GoogleDriveDownloader as gdd

def download_model():
    model_path = "plant_disease_model.h5"  # Path where the model will be saved
    
    # Check if the model already exists
    if not os.path.exists(model_path):
        print("Model not found. Downloading from Google Drive...")
        gdd.download_file_from_google_drive(
            file_id="1kcMD1FWnCdtWkvgW6Qhh63kmGU1BpluV",  # Actual file ID from Google Drive
            dest_path=model_path  # Path where the model file will be saved
        )
        print("Model downloaded successfully.")
    else:
        print("Model already exists. Skipping download.")

if __name__ == "__main__":
    download_model()
