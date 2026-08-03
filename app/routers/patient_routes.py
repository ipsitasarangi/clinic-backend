from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.schema import PatientCreate, PatientResponse

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)


# ---------------- CREATE PATIENT ----------------

@router.post("/", response_model=PatientResponse)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    try:
        new_patient = Patient(
            name=patient.name,
            age=patient.age,
            gender=patient.gender,
            phone=patient.phone,
            email=patient.email,
            address=patient.address
        )

        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)

        return new_patient

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- GET ALL PATIENTS ----------------

@router.get("/", response_model=list[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()


# ---------------- UPDATE PATIENT ----------------

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db)
):
    try:
        db_patient = db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

        if not db_patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        db_patient.name = patient.name
        db_patient.age = patient.age
        db_patient.gender = patient.gender
        db_patient.phone = patient.phone
        db_patient.email = patient.email
        db_patient.address = patient.address

        db.commit()
        db.refresh(db_patient)

        return db_patient

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- DELETE PATIENT ----------------

@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    try:

        db_patient = db.query(Patient).filter(
            Patient.id == patient_id
        ).first()

        if not db_patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found"
            )

        # Delete all appointments of this patient first
        db.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).delete(synchronize_session=False)

        # Delete patient
        db.delete(db_patient)
        db.commit()

        return {
            "message": "Patient deleted successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))