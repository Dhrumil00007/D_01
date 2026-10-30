from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
from controllers.patientController import (
    create_patient, get_patients, get_patient_by_id,
    update_patient_by_id, delete_patient_by_id
)
from models.patientModel import Patient

app = FastAPI(title="Patient API", version="1.0.0")


@app.get("/")
async def home():
    return RedirectResponse(url="/docs")


@app.post("/addPatient")
async def add_patient(patient: Patient, response: Response):
    return await create_patient(patient, response)


@app.get("/getPatients")
async def get_patient_list(response: Response):
    return await get_patients(response)


@app.get("/getPatient/{id}")
async def get_patient(id: str, response: Response):
    return await get_patient_by_id(id, response)


@app.put("/updatePatient/{id}")
async def update_patient(id: str, patient: Patient, response: Response):
    return await update_patient_by_id(id, patient, response)


@app.delete("/deletePatient/{id}")
async def delete_patient(id: str, response: Response):
    return await delete_patient_by_id(id, response)
