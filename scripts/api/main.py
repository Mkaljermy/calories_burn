from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import pandas as pd
import joblib
import os


model = joblib.load(f'D:/calories_burn/scripts/building_model/saved_model/best_calories_model.pkl')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Data(BaseModel):
    Gender: str
    Age: int
    Height: float
    Weight: float
    Duration: float
    Heart_Rate: float
    Body_Temp: float


@app.post('/Calories_predict/')
def predict(data: Data):
    # Create a DataFrame with a single row
    input_data = pd.DataFrame({
        "Gender": [data.Gender],
        "Age": [data.Age],
        "Height" : [data.Height],
        "Weight": [data.Weight],
        "Duration": [data.Duration],
        "Heart_Rate": [data.Heart_Rate],
        "Body_Temp" : [data.Body_Temp]
    })
    
    try:
        prediction = model.predict(input_data)[0]
        return {'Prediction': round(float(prediction))}
    except Exception as e:
        return {'error': str(e)}