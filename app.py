from fastapi import FastAPI, HTTPException , Request,Form
from pydantic import BaseModel, Field, computed_field ,field_validator
from typing import Optional, List, Literal, Annotated, Dict
import json
import pickle
import pandas as pd
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

with open("insurance_pipeline.pkl", "rb") as file:
    model = pickle.load(file)

# Allow CORS if frontend is separate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates dir
templates = Jinja2Templates(directory="templates")

# Show form at root
@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt = 0,lt = 100, title="Age of the User", description="Age should be between 1 and 99", example=30)]
    sex: Annotated[Literal["male","female"], Field(..., title = "Sex of the User", description = "Either Male or Female")]
    Height: Annotated[float, Field(..., gt = 0, title="Height of the User", description="Height in meters", example=1.75)]
    Weight: Annotated[float, Field(..., gt = 0, title="Weight of the User", description="Weight in kilograms", example=70.5)]
    children: Annotated[int, Field(..., ge = 0, le = 5, title="Number of Children", description="Number of children the user has", example=2)]
    smoker: Annotated[Literal["yes", "no"], Field(..., title="Smoking Status", description="Whether the user is a smoker or not", example="no")]
    region: Annotated[Literal["northeast", "northwest", "southeast", "southwest"], Field(..., title="Region", description="Geographical region of the user", example="northeast")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.Weight / (self.Height ** 2), 2)
        return bmi
    @field_validator("sex", "smoker", "region", mode="before")
    @classmethod
    def lowercase_strings(cls, v):
        return v.lower()

@app.post("/predict")
def predict_insurance_cost(data: UserInput):
    try:
        df = pd.DataFrame([data.model_dump()])
        df['bmi'] = data.bmi
        df = df.drop(columns=["Height", "Weight"])
        prediction = model.predict(df)
        return JSONResponse(content={"predicted_cost": float(prediction[0])},status_code=200)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
    
    