import streamlit as st
st.title("Название.")
st.write("Описание.")

user_name = st.text_input("Введите ваше имя:")
if st.button("Отправить"):
    if user_name:   
        st.success(f"Привет, {user_name}!")
    else:
        st.error("Пожалуйста, введите ваше имя.")

st.subheader("Загрузите изображение ")
uploaded_file = st.file_uploader("Выберите изображение", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file,use_container_width=True)