import streamlit as st
import requests

st.title("Банк проект")

api_url = "http://127.0.0.1:8000/predict/"

person_age = st.number_input("Возраст", value=21)
person_gender = st.selectbox("Пол", ["male", "female"])
person_education = st.selectbox("Образование", ["High School","Bachelor","Master"])
person_income = st.number_input("Доход", value=71948.0)
person_emp_exp = st.number_input("Стаж", value=0)

person_home_ownership = st.selectbox("Жильё", ["RENT","OWN","MORTGAGE"])
loan_amnt = st.number_input("Сумма кредита", value=35000.0)

loan_intent = st.selectbox(
    "Цель кредита",
    ["PERSONAL","EDUCATION","MEDICAL","VENTURE"]
)

loan_int_rate = st.number_input("Процентная ставка", value=16.02)
loan_percent_income = st.number_input("Доход и кредит", value=0.49)

cb_person_cred_hist_length = st.number_input(
    "Длина кредитной истории", value=3.0
)

credit_score = st.number_input("Кредитный балл", value=561)
previous_loan_defaults_on_file = st.selectbox("Дефолт", ["Yes","No"])


if st.button("Проверка"):

    bank_data = {
        "person_age": person_age,
        "person_gender": person_gender,
        "person_education": person_education,
        "person_income": person_income,
        "person_emp_exp": person_emp_exp,
        "person_home_ownership": person_home_ownership,
        "loan_amnt": loan_amnt,
        "loan_intent": loan_intent,
        "loan_int_rate": loan_int_rate,
        "loan_percent_income": loan_percent_income,
        "cb_person_cred_hist_length": cb_person_cred_hist_length,
        "credit_score": credit_score,
        "previous_loan_defaults_on_file": previous_loan_defaults_on_file
    }

    try:
        answer = requests.post(api_url, json=bank_data, timeout=10)

        if answer.status_code == 200:
            result = answer.json()
            st.json(result)

        else:
            st.error(f"Ошибка: {answer.status_code}")

    except requests.exceptions.RequestException:
        st.error("Не удалось подключиться к API")