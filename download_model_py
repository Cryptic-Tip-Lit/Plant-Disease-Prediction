import os
import gdown

def download_model():
    file_id = "1kcMD1FWnCdtWkvgW6Qhh63kmGU1BpluV"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "plant_disease_model.h5"

    if not os.path.exists(output):
        print(f"Downloading model file to '{output}'...")
        gdown.download(url, output, quiet=False)
        print("✅ Download complete.")
    else:
        print(f"✅ Model file already exists: {output}")

if __name__ == "__main__":
    download_model()
