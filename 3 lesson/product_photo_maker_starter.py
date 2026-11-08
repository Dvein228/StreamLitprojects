"""
Product Photo Maker — стартовий шаблон
Курс «Інноваційні технології», заняття 7.

Готові функції-обгортки remove_background() та add_background() вже реалізовано —
твоя задача зібрати з них Streamlit-застосунок, дотримуючись кроків із заняття.
"""

import io

import streamlit as st
from PIL import Image
from rembg import remove

def remove_background(image: Image.Image) -> Image.Image:
    """Видаляє фон із зображення за допомогою моделі rembg.

    Працює локально, без API-ключа. При першому виклику в сесії rembg
    завантажує модель сегментації (~176 МБ) — це нормально і трапляється лише раз.

    Повертає RGBA-зображення: там, де був фон, тепер прозорість (alpha = 0).
    """
    return remove(image)


def add_background(foreground: Image.Image, bg_color: tuple) -> Image.Image:
    """Накладає прозоре зображення (RGBA) на новий суцільний фон.

    foreground — результат remove_background() (режим RGBA).
    bg_color — колір фону як кортеж (R, G, B), наприклад (255, 255, 255).
    Повертає готове RGB-зображення без прозорості.
    """
    background = Image.new("RGBA", foreground.size, bg_color + (255,))
    combined = Image.alpha_composite(background, foreground)
    return combined.convert("RGB")


# ---------------------------------------------------------------------------
# Streamlit-інтерфейс
# ---------------------------------------------------------------------------

st.title("🛍️ Product Photo Maker")
st.write("Завантаж фото товару — я приберу фон і поставлю новий.")

uploaded_file = st.file_uploader("Завантаж фото товару", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original = Image.open(uploaded_file).convert("RGBA")
    st.image(original, caption="Оригінал", use_column_width=True)

# TODO Крок 2: додай кнопку "Прибрати фон" і виклик remove_background(original).
#             Не забудь st.spinner() на час очікування відповіді та збережи
#             результат у st.session_state, щоб використати його далі.

# TODO Крок 3: додай st.color_picker() для вибору кольору нового фону,
#             переведи обраний колір з hex у кортеж (R, G, B) і виклич
#             add_background(), щоб показати фінальний результат.

# TODO Крок 4: обгорни виклик remove_background() у try/except, щоб застосунок
#             не "падав" при пошкодженому файлі. Додай st.download_button(),
#             яка дозволяє зберегти фінальне зображення файлом .png
#             (підказка: збережи зображення в io.BytesIO() перед завантаженням).

# TODO Крок 5 (демонстрація на занятті, реалізується вдома в ДЗ рівня Senior):
#             замість суцільного кольору можна згенерувати тематичний фон
#             через generate_image() з уроку 6 і накласти товар на нього
#             (не забудь .resize() згенерований фон до розміру товару
#             перед Image.alpha_composite()).
