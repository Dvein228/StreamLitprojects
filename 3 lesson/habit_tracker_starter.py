"""
Habit Tracker Dashboard — стартовий шаблон
Курс «Інноваційні технології», заняття 8.

Готові функції-обгортки load_data() та save_data() вже реалізовано —
твоя задача зібрати з них Streamlit-застосунок, дотримуючись кроків із заняття.
"""

import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "habit_data_sample.json")

def load_data() -> list:
    """Читає всі записи з JSON-файлу.

    Якщо файлу ще немає (наприклад, перший запуск застосунку) — повертає
    порожній список, а не викликає помилку.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(records: list) -> None:
    """Зберігає список записів назад у JSON-файл.

    Файл перезаписується цілком — щоб додати один новий запис, спочатку
    завантаж усі наявні через load_data(), допиши новий елемент і лише
    тоді виклич save_data() з повним оновленим списком.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


records = load_data()
df = pd.DataFrame(records)
print(df)

by_category = df.groupby("category")["minutes"].sum().reset_index()
print(by_category)

fig_bar = px.bar(by_category, x="category", y="minutes", title="Час за категоріями")
st.plotly_chart(fig_bar)

by_day = df.groupby("date")["minutes"].sum().reset_index()
fig_line = px.line(by_day, x="date", y="minutes", title="Динаміка по днях")
st.plotly_chart(fig_line)


# ---------------------------------------------------------------------------
# Streamlit-інтерфейс
# ---------------------------------------------------------------------------

st.title("📊 Habit Tracker Dashboard")
st.write("Записуй свою щоденну активність — я збережу дані і покажу статистику.")

with st.form("new_record"):
    date = st.date_input("Дата")
    category = st.selectbox("Категорія", ["Навчання", "Спорт", "Читання", "Інше"])
    minutes = st.number_input("Скільки хвилин?", min_value=1, max_value=600, value=30)
    submitted = st.form_submit_button("➕ Додати запис")

# TODO Крок 1: якщо форму надіслано (submitted) — завантаж наявні записи
#             через load_data(), додай новий запис (словник із date, category,
#             minutes) у список і збережи його через save_data(). Не забудь
#             показати st.success() після успішного збереження.

# TODO Крок 2: завантаж усі записи через load_data() і покажи їх таблицею
#             (st.dataframe). Якщо записів ще немає — покажи st.info() з
#             підказкою додати перший запис.

# TODO Крок 3: перетвори записи на pd.DataFrame, переведи колонку "date" у
#             справжній тип дати через pd.to_datetime(). Підготуй підсумки:
#             df.groupby("category")["minutes"].sum() та
#             df.groupby("date")["minutes"].sum(). Покажи загальну суму
#             хвилин через st.metric().

# TODO Крок 4: побудуй стовпчиковий графік (px.bar) за категоріями і
#             лінійний графік (px.line) динаміки по днях, вбудуй обидва
#             в застосунок через st.plotly_chart().

# TODO Крок 5 (демонстрація на занятті, реалізується вдома в ДЗ рівня
#             Senior): додай st.multiselect() для вибору категорій і
#             st.date_input() для періоду, відфільтруй DataFrame перед
#             побудовою графіка (df["category"].isin(...) та
#             df["date"].between(...)).
