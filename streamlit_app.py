import streamlit as st
import requests

st.title("🌿 Plant Disease Detection")
st.write("Upload an image of the plant leaf to predict the disease.")

# Language selection
language_options = {"en": "English", "es": "Spanish", "fr": "French", "hi": "Hindi"}
language = st.selectbox("Select Language", options=list(language_options.keys()), format_func=lambda x: language_options[x])

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    st.write("Processing...")
    
    files = {"file": uploaded_file.getvalue()}
    data = {"language": language}
    
    API_URL = "https://plant-disease-prediction-1-6nzd.onrender.com/predict"
    
    try:
        response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {result['prediction']}")
            st.write(f"Severity: {result['severity']}")
            st.write(f"Cause: {result['cause']}")
            st.write(f"Info: {result['info']}")
            st.markdown(f"[Buy Recommended Pesticide]({result['pesticide_link']})")
            st.write(result['report'])
            
            # Download PDF report
            pdf_url = "https://plant-disease-prediction-1-6nzd.onrender.com/download_report"
            st.markdown(f"[Download PDF Report]({pdf_url})")
        else:
            st.error("Error processing the image. Please try again.")
    
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the server. Make sure the Flask API is running.")
