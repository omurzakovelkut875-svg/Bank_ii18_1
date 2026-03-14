from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import joblib


model = joblib.load('api/log_model.pkl')
scaler = joblib.load('api/scaler (2).pkl')


bank_app = FastAPI()

gender_list = ['male']
education_list = ['Bachelor', 'Doctorate', 'High School', 'Master']
ownership_list = ['OTHER', 'OWN', 'RENT']
loan_intent_list = ['EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE']
previous_loan_defaults_on_file_list = ['Yes']

class BankSchema(BaseModel):
    person_age: float
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: str


@bank_app.post('/predict', response_model=dict)
async def predict_bank(bank: BankSchema):
    bank_dict = bank.dict()

    person_gender = bank_dict.pop('person_gender')
    person_gender_1_0 = [1 if person_gender == i else 0 for i in gender_list]

    person_education = bank_dict.pop('person_education')
    person_education_1_0 = [
        1 if person_education == i else 0 for i in education_list
    ]

    person_home_ownership = bank_dict.pop('person_home_ownership')
    person_home_ownership_1_0 = [
        1 if person_home_ownership == i else 0 for i in ownership_list
    ]

    loan_intent = bank_dict.pop('loan_intent')
    loan_intent_1_0 = [
        1 if loan_intent == i else 0 for i in loan_intent_list
    ]

    previous_loan_defaults_on_file = bank_dict.pop('previous_loan_defaults_on_file')
    previous_loan_defaults_on_file_1_0 = [
        1 if previous_loan_defaults_on_file == i else 0 for i in previous_loan_defaults_on_file_list
    ]

    bank_data = (list(bank_dict.values()) + person_gender_1_0 + person_education_1_0 +
     person_home_ownership_1_0 + loan_intent_1_0 + previous_loan_defaults_on_file_1_0)

    scaler_data = scaler.transform([bank_data])
    pred = model.predict(scaler_data)[0]
    final_pred = 'approved' if pred == 1 else 'Rejected'
    return {"Answer": final_pred}





if __name__ == "__main__":
    uvicorn.run(bank_app, host="127.0.0.1", port=8000)