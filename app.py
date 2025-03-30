from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import io

# Load the trained model
model = tf.keras.models.load_model("plant_disease_model.h5")


# Corrected class labels based on your dataset
CLASS_NAMES = [
    "Pepper Bell Bacterial Spot", "Pepper Bell Healthy", "Potato Early Blight", "Potato Healthy",
    "Potato Late Blight", "Tomato Target Spot", "Tomato Mosaic Virus", "Tomato Yellow Leaf Curl Virus",
    "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Healthy", "Tomato Late Blight",
    "Tomato Leaf Mold", "Tomato Septoria Leaf Spot", "Tomato Spider Mites Two Spotted Spider Mite"
]

# Pesticide recommendations
PESTICIDES = {
    "Pepper Bell Bacterial Spot": "https://example.com/pepper-bacterial-spot-pesticide",
    "Potato Early Blight": "https://example.com/potato-early-blight-pesticide",
    "Potato Late Blight": "https://example.com/potato-late-blight-pesticide",
    "Tomato Target Spot": "https://example.com/tomato-target-spot-pesticide",
    "Tomato Mosaic Virus": "https://example.com/tomato-mosaic-virus-pesticide",
    "Tomato Yellow Leaf Curl Virus": "https://example.com/tomato-yellow-leaf-curl-virus-pesticide",
    "Tomato Bacterial Spot": "https://example.com/tomato-bacterial-spot-pesticide",
    "Tomato Early Blight": "https://example.com/tomato-early-blight-pesticide",
    "Tomato Late Blight": "https://example.com/tomato-late-blight-pesticide",
    "Tomato Leaf Mold": "https://example.com/tomato-leaf-mold-pesticide",
    "Tomato Septoria Leaf Spot": "https://example.com/tomato-septoria-leaf-spot-pesticide",
    "Tomato Spider Mites Two Spotted Spider Mite": "https://example.com/tomato-spider-mites-pesticide"
}

app = Flask(__name__)

@app.route("/")
def home():
    return "Plant Disease Prediction API is running. Use the /predict endpoint to analyze an image."

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400
    
    try:
        # Load and preprocess image
        img = image.load_img(io.BytesIO(file.read()), target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction, axis=1)[0]
        disease_name = CLASS_NAMES[predicted_class]

        # Get pesticide link (if disease detected)
        pesticide_link = PESTICIDES.get(disease_name, "No specific pesticide needed.")

        # Generate a disease report
        report = f"The plant is affected by {disease_name}. Recommended action: {pesticide_link}"

        return jsonify({"prediction": disease_name, "report": report, "pesticide_link": pesticide_link})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
