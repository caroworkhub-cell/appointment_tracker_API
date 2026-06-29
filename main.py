from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Appointment Tracker", 
              description="Track patient appointment with FastAPI",
              version= "1.0.0")

# CREATE 
@app.post("/patients", response_model= schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

# READ ALL
@app.get("/patients/", response_model = List[schemas.PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return crud.get_patients(db)

# READ ONE
@app.get("/patients/{patient_id}", response_model = schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return patient

# UPDATE
@app.put("/patients/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(patient_id: int, patient: schemas.PatientUpdate, db: Session = Depends(get_db)):
    updated_patient = crud.update_patient(db, patient_id, patient)
    if not updated_patient:
        raise HTTPException(404, "Patient not found")
    return updated_patient

# DELETE
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = crud.delete_patient(db, patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")
    return {"message": "Patient deleted successfully"}