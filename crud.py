from sqlalchemy.orm import Session
import models, schemas

# The CREATE operation
def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())
    db.add(db_patient) 
    db.commit() 
    db.refresh(db_patient) 
    return db_patient 

# READ only one record
def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
# READ ALL record 
def get_patients(db: Session):
    return db.query(models.Patient).all()

# UPDATE a record
def update_patient(db: Session, patient_id: int, data: schemas.PatientUpdate):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        return None
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(patient, field, value)

    db.commit()
    db.refresh(patient)
    return patient

# DELETE/REMOVE a record
def delete_patient(db: Session, patient_id: int):
   
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
    if not patient:
        return None
    
    db.delete(patient)
    
    db.commit()
    return patient