import os
import gdown

def download_model():
    model_path = "plant_disease_model.tflite"

    if not os.path.exists(model_path):
        print("Model not found. Downloading from Google Drive...")
        gdown.download(
            "https://drive.google.com/uc?id=11bgaWNeWhHYMNE6-lqRkqZcLaeYNNI4i",
            model_path,
            quiet=False
        )
        print("Model downloaded successfully.")
    else:
        print("Model already exists. Skipping download.")

if __name__ == "__main__":
    download_model()
