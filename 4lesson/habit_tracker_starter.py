"""
Habit Tracker Dashboard
Домашнє завдання №7: збереження даних та інтерактивна аналітика.

Файл JSON має лежати в тій самій папці, що й цей Python-файл.
"""

import json
import os
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st


# Шлях до JSON-файлу визначається відносно розташування цього скрипту.
DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "habit_data_sample.json",
)

CATEGORIES = ["Навчання", "Спорт", "Читання", "Інше"]


def load_data() -> list:
    """Завантажує всі записи з JSON. Якщо файлу ще немає — повертає []."""
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("У JSON-файлі має зберігатися список записів.")

    return data


def save_data(records: list) -> None:
    """Зберігає повний список записів у JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Заголовок та форма додавання запису
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Habit Tracker Dashboard", page_icon="📊", layout="wide")
st.title("📊 Habit Tracker Dashboard")
st.write(
    "Записуй свою щоденну активність, зберігай дані та переглядай статистику."
)

with st.form("new_record"):
    st.subheader("Додати новий запис")

    record_date = st.date_input("Дата", value=date.today())
    category = st.selectbox("Категорія", CATEGORIES)
    minutes = st.number_input(
        "Скільки хвилин?",
        min_value=1,
        max_value=600,
        value=30,
        step=5,
    )

    submitted = st.form_submit_button("➕ Додати запис")

if submitted:
    try:
        records_to_save = load_data()
        new_record = {
            "date": record_date.isoformat(),
            "category": category,
            "minutes": int(minutes),
        }
        records_to_save.append(new_record)
        save_data(records_to_save)
        st.success("✅ Запис успішно додано та збережено у JSON-файлі!")
    except (OSError, json.JSONDecodeError, ValueError) as error:
        st.error(f"Не вдалося зберегти запис: {error}")


# ---------------------------------------------------------------------------
# Завантаження та відображення всіх записів
# ---------------------------------------------------------------------------

try:
    records = load_data()
except (OSError, json.JSONDecodeError, ValueError) as error:
    st.error(f"Не вдалося прочитати дані: {error}")
    records = []

st.divider()
st.subheader("📋 Усі записи")

if not records:
    st.info("Поки що немає жодного запису. Додай перший через форму вище!")
else:
    # Явно задаємо назви колонок, щоб уникнути KeyError при порожніх/неповних даних.
    df = pd.DataFrame(records, columns=["date", "category", "minutes"])

    # Перевіряємо структуру даних перед аналітикою.
    df = df.dropna(subset=["date", "category", "minutes"]).copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["minutes"] = pd.to_numeric(df["minutes"], errors="coerce")
    df = df.dropna(subset=["date", "minutes"])
    df["minutes"] = df["minutes"].astype(int)
    df["category"] = df["category"].astype(str)

    if df.empty:
        st.info("У файлі поки немає коректних записів для відображення.")
    else:
        table_df = df.copy()
        table_df["date"] = table_df["date"].dt.strftime("%Y-%m-%d")
        st.dataframe(table_df, use_container_width=True, hide_index=True)

        # -------------------------------------------------------------------
        # Інтерактивні фільтри (додатковий крок із шаблону)
        # -------------------------------------------------------------------

        st.divider()
        st.subheader("🔎 Фільтри аналітики")

        available_categories = sorted(df["category"].unique().tolist())
        default_categories = [
            item for item in CATEGORIES if item in available_categories
        ]
        # Якщо у JSON є категорія, якої немає у стандартному списку, теж додаємо її.
        default_categories += [
            item for item in available_categories if item not in default_categories
        ]

        col_filter_1, col_filter_2 = st.columns(2)
        with col_filter_1:
            selected_categories = st.multiselect(
                "Оберіть категорії",
                options=available_categories,
                default=default_categories,
            )

        min_date = df["date"].min().date()
        max_date = df["date"].max().date()

        with col_filter_2:
            selected_period = st.date_input(
                "Період",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

        # st.date_input для діапазону повертає кортеж із двох дат.
        if isinstance(selected_period, (tuple, list)) and len(selected_period) == 2:
            start_date, end_date = selected_period
        elif isinstance(selected_period, (tuple, list)) and len(selected_period) == 1:
            start_date = end_date = selected_period[0]
        else:
            start_date = end_date = selected_period

        filtered_df = df[
            df["category"].isin(selected_categories)
            & df["date"].between(
                pd.to_datetime(start_date),
                pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1),
            )
        ].copy()

        # -------------------------------------------------------------------
        # Підсумкова аналітика
        # -------------------------------------------------------------------

        st.divider()
        st.subheader("📈 Аналітика")

        total_minutes = int(filtered_df["minutes"].sum())
        st.metric("Загальна кількість хвилин за фільтрами", f"{total_minutes} хв")

        if filtered_df.empty:
            st.info("За вибраними фільтрами записів немає. Зміни категорії або період.")
        else:
            by_category = (
                filtered_df.groupby("category")["minutes"]
                .sum()
                .reset_index()
                .sort_values("minutes", ascending=False)
            )
            by_day = (
                filtered_df.groupby("date")["minutes"]
                .sum()
                .reset_index()
                .sort_values("date")
            )

            chart_col_1, chart_col_2 = st.columns(2)

            with chart_col_1:
                fig_bar = px.bar(
                    by_category,
                    x="category",
                    y="minutes",
                    title="Час за категоріями",
                    labels={"category": "Категорія", "minutes": "Хвилини"},
                    text="minutes",
                )
                fig_bar.update_layout(xaxis_title="Категорія", yaxis_title="Хвилини")
                st.plotly_chart(fig_bar, use_container_width=True)

            with chart_col_2:
                fig_line = px.line(
                    by_day,
                    x="date",
                    y="minutes",
                    title="Динаміка активності по днях",
                    labels={"date": "Дата", "minutes": "Хвилини"},
                    markers=True,
                )
                fig_line.update_layout(xaxis_title="Дата", yaxis_title="Хвилини")
                st.plotly_chart(fig_line, use_container_width=True)
