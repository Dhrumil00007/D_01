from fastapi import Response
from dbConnect import patientCollection
from bson import ObjectId


# CREATE
async def create_patient(patient, response: Response):
    try:
        result = await patientCollection.insert_one(patient.dict(exclude={"id"}))
        response.status_code = 201
        return {
            "isSuccess": True,
            "message": "Patient added successfully",
            "patientId": str(result.inserted_id)
        }
    except Exception as e:
        response.status_code = 500
        return {"isSuccess": False, "error": str(e)}


# READ ALL
async def get_patients(response: Response):
    try:
        patients = []
        async for patient in patientCollection.find({}):
            patient["id"] = str(patient.pop("_id"))
            patients.append(patient)
        response.status_code = 200
        return {"isSuccess": True, "count": len(patients), "patients": patients}
    except Exception as e:
        response.status_code = 500
        return {"isSuccess": False, "error": str(e)}


# READ BY ID
async def get_patient_by_id(id: str, response: Response):
    try:
        if not ObjectId.is_valid(id):
            response.status_code = 400
            return {"isSuccess": False, "message": "Invalid Patient ID"}

        patient = await patientCollection.find_one({"_id": ObjectId(id)})
        if patient:
            patient["id"] = str(patient.pop("_id"))
            response.status_code = 200
            return {"isSuccess": True, "patient": patient}

        response.status_code = 404
        return {"isSuccess": False, "message": "Patient not found"}
    except Exception as e:
        response.status_code = 500
        return {"isSuccess": False, "error": str(e)}


# UPDATE
async def update_patient_by_id(id: str, patient, response: Response):
    try:
        if not ObjectId.is_valid(id):
            response.status_code = 400
            return {"isSuccess": False, "message": "Invalid Patient ID"}

        result = await patientCollection.update_one(
            {"_id": ObjectId(id)},
            {"$set": patient.dict(exclude={"id"})}
        )
        if result.matched_count == 1:
            response.status_code = 200
            return {"isSuccess": True, "message": "Patient updated"}

        response.status_code = 404
        return {"isSuccess": False, "message": "Patient not found"}
    except Exception as e:
        response.status_code = 500
        return {"isSuccess": False, "error": str(e)}


# DELETE
async def delete_patient_by_id(id: str, response: Response):
    try:
        if not ObjectId.is_valid(id):
            response.status_code = 400
            return {"isSuccess": False, "message": "Invalid Patient ID"}

        result = await patientCollection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            response.status_code = 200
            return {"isSuccess": True, "message": "Patient deleted"}

        response.status_code = 404
        return {"isSuccess": False, "message": "Patient not found"}
    except Exception as e:
        response.status_code = 500
        return {"isSuccess": False, "error": str(e)}
