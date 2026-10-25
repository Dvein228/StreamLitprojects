import streamlit as st
st.set_page_config(page_title="Мій Супер-Додаток",page_icon="istockphoto-1276164321-612x612-removebg-preview.png",
                   layout="wide")
st.title("Ласкаво просимо до мого додатку")

tab1, tab2 = st.tabs (["Про мене", "Мій інструмент"])
with tab1:
    st.header("Знайомство з автором")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("istockphoto-1276164321-612x612-removebg-preview.png", caption="Я", width=400)
    with col2:
        st.subheader("Привіт, я майбутній Python Developer")
        st.write("Я навчаюсь в Малій Комп'ютерній Академії IT STEP. Створюю круті веб-додатки та вивчаю")
        with st.container():
            st.info("Контакти для зв'язку") 
            st.markdown("- GitHub: [Мій профіль](https://github.com/Dvein228)")

with tab2:
    st.info("Ця вкладка у розробці")