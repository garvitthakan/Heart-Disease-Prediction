# main.py
from fastapi import FastAPI, HTTPException, Request
from typing import List
from model import train_model_and_predict, save_to_mongodb
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.post("/predict/")
async def predict(input_data: List[int]):
    try:
        if len(input_data) != 13:
            raise HTTPException(status_code=400, detail="Input data must contain 13 values")
        
        prediction = train_model_and_predict(input_data)
        save_to_mongodb(input_data, prediction)
        
        if prediction == 0:
            return {"prediction": "The Person does not have a Heart Disease"}
        else:
            return {"prediction": "The Person has Heart Disease"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})