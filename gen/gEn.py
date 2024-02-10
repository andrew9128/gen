import streamlit as st
import google.generativeai as genai
import os
import json
import base64
import pathlib
import pprint
import requests
import mimetypes
from IPython.display import Markdown

# Установка переменной окружения GOOGLE_APPLICATION_CREDENTIAlS
os.environ["GOOGLE_APPLICATION_CREDENTIAlS"] = "/content/global-brook-412118-4bbce82b657c.json"

# API ключ
API_KEY = os.environ.get("AIzaSyCorKgCDutsQ_8X2gz2b_rpuIiqnvdZWFo")

# Настройка модели Gemini
gemini_model = genai.GenerativeModel(model_name="gemini-pro")

# Создание интерфейса веб-приложения
# Вывод названия приложения
st.title("Помощник по кодированиб")

# Создание боковой панели
sidebar = st.sidebar

# Кнопка "Отправить"
send_button = sidebar.button("Отправить")

# Сохранение истории кодирования
if sidebar.button("Сохранить историю"):
    # Открытие файла "history.txt" в режиме добавления
    with open("history.txt", "a") as f:
        # Запись введенного кода в файл
        f.write(code)

# Export code
if sidebar.button("Export code"):
    # Скачивание кода в виде файла "code.py"
    st.download_button("Скачать код", code, "code.py")

# Создание поля ввода кода
code = st.text_area("Введите код:", height=300)

# Функция для автодополнения кода
def autocomplete(code):
    """Автодополнение кода"""
    if not code.strip():
        return "Введенный код пуст"

    # Получение списка предсказаний на основе введенного кода
    response = gemini_model.generate_content(code, user_location="us")
    predictions = response.candidates

    if predictions:
        # Вывод числового инпута для выбора предсказания
        prediction_index = st.number_input("Выберите предсказание:", min_value=1, max_value=len(predictions), value=1, step=1)
        prediction_index = int(prediction_index) - 1

        # Получение выбраного предсказания текста
        prediction_text = predictions[prediction_index].content
        return prediction_text
    else:
        return "Не удалось получить предсказания"

# Выполнение автодополнения и отображение результатов
predictions = autocomplete(code)
if predictions:
    st.code(predictions, language="python")

# Подключение CSS файла
with open("style.css", "r") as f:
    css = f.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)