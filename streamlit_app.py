import streamlit as st
import requests

# Language options
LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "zh": "Chinese"
}

st.title("🌿 Plant Disease Detection")
st.write("Upload an image of the plant leaf to predict the disease.")

# Language selection
def get_language_code(language):
    return next((code for code, lang in LANGUAGES.items() if lang == language), "en")

selected_language = st.selectbox("Select Language", options=list(LANGUAGES.values()))
language_code = get_language_code(selected_language)

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.write("Processing...")

    # Convert image to bytes
    files = {"file": uploaded_file.getvalue()}
    data = {"language": language_code}  # Send selected language to API

    API_URL = "https://plant-disease-prediction-1-6nzd.onrender.com/predict"

    try:
        response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {result['prediction']}")
            st.write(result['report'])
            st.markdown(f"[Buy Recommended Pesticide]({result['pesticide_link']})")
            
            # Provide a download link for the PDF report
            st.download_button("Download Report", result["pdf_report"], file_name="disease_report.pdf", mime="application/pdf")
        else:
            st.error("Error processing the image. Please try again.")
    
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the server. Make sure the Flask API is running.")
