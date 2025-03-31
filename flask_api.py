from flask import Flask, request, jsonify, send_file
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import os
from fpdf import FPDF
from deep_translator import GoogleTranslator

# Load the TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="plant_disease_model.tflite")
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Class labels and additional details
DISEASE_DETAILS = {
    "Pepper Bell Bacterial Spot": {"severity": "High", "cause": "Bacteria Xanthomonas campestris", "info": "Causes black lesions on leaves and fruit.", "pesticide": "https://example.com/pepper-bacterial-spot-pesticide"},
    "Potato Early Blight": {"severity": "Medium", "cause": "Fungus Alternaria solani", "info": "Brown concentric rings on leaves.", "pesticide": "https://example.com/potato-early-blight-pesticide"},
    "Potato Late Blight": {"severity": "High", "cause": "Pathogen Phytophthora infestans", "info": "Dark lesions with white fungal growth.", "pesticide": "https://example.com/potato-late-blight-pesticide"},
    "Tomato Target Spot": {"severity": "Medium", "cause": "Fungus Corynespora cassiicola", "info": "Small dark spots with yellow halos.", "pesticide": "https://example.com/tomato-target-spot-pesticide"}
}

app = Flask(__name__)

@app.route("/")
def home():
    return "Plant Disease Prediction API is running. Use the /predict endpoint to analyze an image."

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files or "language" not in request.form:
        return jsonify({"error": "No file or language provided"}), 400
    
    file = request.files["file"]
    language = request.form["language"]
    if file.filename == "":
        return jsonify({"error": "Empty file"}), 400
    
    try:
        # Load and preprocess the image
        img = image.load_img(io.BytesIO(file.read()), target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

        # Set the input tensor
        interpreter.set_tensor(input_details[0]['index'], img_array)

        # Run inference
        interpreter.invoke()

        # Get the output tensor
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predicted_class = np.argmax(output_data, axis=1)[0]
        disease_name = list(DISEASE_DETAILS.keys())[predicted_class]

        # Get disease details
        details = DISEASE_DETAILS.get(disease_name, {"severity": "Unknown", "cause": "Unknown", "info": "No information available.", "pesticide": "No specific pesticide needed."})

        # Generate disease report
        report = f"Disease: {disease_name}\nSeverity: {details['severity']}\nCause: {details['cause']}\nInfo: {details['info']}\nRecommended Pesticide: {details['pesticide']}"
        translated_report = GoogleTranslator(source='auto', target=language).translate(report)
        
        # Generate PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, translated_report)
        pdf_filename = "report.pdf"
        pdf.output(pdf_filename)
        
        return jsonify({
            "prediction": disease_name,
            "severity": details['severity'],
            "cause": details['cause'],
            "info": details['info'],
            "pesticide_link": details['pesticide'],
            "report": translated_report,
            "pdf_report": pdf_filename
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download_report", methods=["GET"])
def download_report():
    return send_file("report.pdf", as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
