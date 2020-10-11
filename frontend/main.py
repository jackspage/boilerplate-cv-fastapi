# frontend/main.py
import time
import uuid

import requests
import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image

STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}

st.set_option("deprecation.showfileUploaderEncoding", False)

# defines an h1 header
st.title("Style transfer web app")

# displays a file uploader widget
image = st.file_uploader("Choose an image")

if image:
    img = Image.open(image)
    cropped_img = st_cropper(img, realtime_update=True, box_color="#E4E39E")

    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((500, 500))
    st.image(cropped_img)
    #TODO: NEED TO CONVERT THE CROPPED IMAGE SOMEHOW. THE PIPELINE WORKS NOW FOR IMAGE FILES.


if st.button("Style Transfer"):
    if image is not None:
        st.write("Generate models!")
        files = {"file": image.getvalue()}
        res = requests.post(f"http://backend:8080/transfer", files=files)

        # Display unmodified picture
        res_original = requests.post(f"http://backend:8080/upload", files=files)
        img_path_original = res_original.json()
        image_original = Image.open(img_path_original.get("filename")).convert('RGB')
        st.image(image_original)

        displayed_styles = []
        displayed = 0
        total = len(STYLES)

        while displayed < total:
            for style in STYLES.values():
                if style not in displayed_styles:
                    try:
                        path = f"/storage/{res.json().get('image_uuid')}_{style}.jpg"
                        image = Image.open(path)
                        st.image(image, width=500)
                        time.sleep(1)
                        displayed += 1
                        displayed_styles.append(style)
                    except:
                        pass