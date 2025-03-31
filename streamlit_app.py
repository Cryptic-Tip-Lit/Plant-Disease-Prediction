import streamlit as st
import requests

st.title("🌿 Plant Disease Detection")
st.write("Upload an image of the plant leaf to predict the disease.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.write("Processing...")

    # ✅ Fix: Convert image to bytes
    files = {"file": uploaded_file.getvalue()}

    # ✅ Fix: Use deployed API instead of localhost
    API_URL = "https://plant-disease-prediction-1-6nzd.onrender.com"  # Replace with actual Render URL

    try:
        response = requests.post("https://plant-disease-prediction-1-6nzd.onrender.com", files=files)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction: {result['prediction']}")
            st.write(result['report'])
            st.markdown(f"[Buy Recommended Pesticide]({result['pesticide_link']})")
        else:
            st.error("Error processing the image. Please try again.")
    
    except requests.exceptions.RequestException:
        st.error("Failed to connect to the server. Make sure the Flask API is running.")
