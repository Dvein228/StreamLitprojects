
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="фоточки",
    page_icon="🧠",
    layout="wide"
)

st.title("фотоедитор")

st.sidebar.header("фильтры")

uploaded_file = st.sidebar.file_uploader(
    "Выберите изображение:",
    type=["png", "jpg", "jpeg"]
)

filter_option = st.sidebar.selectbox(
    "Фильтры:",
    options=[
        "Оригинал",
        "Черно-Белый",
        "Яркость",
        "Контраст",
        "Размытие",
        "Инверсия"
    ]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    img_arr = np.array(image)

    processed_img = img_arr.copy()

    if filter_option == "Черно-Белый":
        processed_img = cv2.cvtColor(
            img_arr, cv2.COLOR_RGB2GRAY
        )

    elif filter_option == "Яркость":
        processed_img = cv2.convertScaleAbs(
            img_arr, alpha=1, beta=50
        )

    elif filter_option == "Контраст":
        processed_img = cv2.convertScaleAbs(
            img_arr, alpha=1.5, beta=0
        )

    elif filter_option == "Размытие":
        processed_img = cv2.GaussianBlur(
            img_arr, (15, 15), 0
        )

    elif filter_option == "Инверсия":
        processed_img = cv2.bitwise_not(img_arr)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Оригинал")
        st.image(img_arr, width="stretch")

    with col2:
        st.subheader("Изменённая")
        st.image(processed_img, width="stretch")

else:
    st.info("Загрузите фотографию, чтобы начать обработку.")
