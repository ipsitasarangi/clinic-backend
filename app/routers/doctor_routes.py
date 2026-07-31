from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.doctor import Doctor
from app.schema import DoctorCreate, DoctorResponse
from app.auth import get_current_user

router = APIRouter(
    prefix="/api/doctors",
    tags=["Doctors"]
)


# Create Doctor
@router.post("/", response_model=DoctorResponse)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    new_doctor = Doctor(
        name=doctor.name,
        specialization=doctor.specialization,
        phone=doctor.phone,
        email=doctor.email
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


# Get All Doctors
@router.get("/", response_model=list[DoctorResponse])
def get_doctors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Doctor).all()


# Update Doctor
@router.put("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db_doctor.name = doctor.name
    db_doctor.specialization = doctor.specialization
    db_doctor.phone = doctor.phone
    db_doctor.email = doctor.email

    db.commit()
    db.refresh(db_doctor)

    return db_doctor


# Delete Doctor
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_doctor)
    db.commit()

    return {"message": "Doctor deleted successfully"}