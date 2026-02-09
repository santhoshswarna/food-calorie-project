import streamlit as st
import requests
from PIL import Image
import io

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Scanner",
    page_icon="🍽️",
    layout="centered"
)

st.title("🍽️ Food Scanner & Calorie Estimator")
st.caption("Upload or capture a food image to predict calories")

# ---------------- IMAGE INPUT OPTIONS ----------------
option = st.radio(
    "Choose image input method:",
    ("Upload Image", "Capture from Camera")
)

image_bytes = None


if option == "Upload Image":
    uploaded_file = st.file_uploader(
        "Upload food image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Selected Image", use_column_width=True)
        image_bytes = uploaded_file.getvalue()


elif option == "Capture from Camera":
    camera_image = st.camera_input("Take a photo")

    if camera_image is not None:
        image = Image.open(camera_image)
        st.image(image, caption="Captured Image", use_column_width=True)
        image_bytes = camera_image.getvalue()


if image_bytes is not None:
    if st.button("🔍 Predict Food"):
        with st.spinner("Analyzing food..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    files={"file": ("image.png", image_bytes, "image/png")}
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("Prediction Successful ✅")

                    st.markdown(f"""
                    ### 🍽 Food: **{result.get('food', 'Unknown').title()}**
                    🔥 Calories: **{result.get('calories', 'N/A')} kcal**  
                    📊 Confidence: **{round(result.get('confidence', 0)*100, 2)}%**
                    """)

                else:
                    st.error(response.json().get("error", "Backend error"))

            except Exception as e:
                st.error(f"❌ Error: {e}")