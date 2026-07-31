from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schema import AppointmentCreate, AppointmentResponse

router = APIRouter(
    prefix="/api/appointments",
    tags=["Appointments"]
)


@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    new_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        date_time=appointment.date_time
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "id": new_appointment.id,
        "patient_id": new_appointment.patient_id,
        "doctor_id": new_appointment.doctor_id,
        "patient_name": patient.name,
        "doctor_name": doctor.name,
        "date_time": new_appointment.date_time,
        "status": new_appointment.status,
    }


@router.get("/", response_model=list[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):

    appointments = db.query(Appointment).all()

    result = []

    for appointment in appointments:

        result.append({
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_id": appointment.doctor_id,
            "patient_name": appointment.patient.name,
            "doctor_name": appointment.doctor.name,
            "date_time": appointment.date_time,
            "status": appointment.status,
        })

    return result


@router.get("/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "patient_name": appointment.patient.name,
        "doctor_name": appointment.doctor.name,
        "date_time": appointment.date_time,
        "status": appointment.status,
    }


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    updated: AppointmentCreate,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == updated.doctor_id
    ).first()

    patient = db.query(Patient).filter(
        Patient.id == updated.patient_id
    ).first()

    if not doctor or not patient:
        raise HTTPException(
            status_code=404,
            detail="Doctor or Patient not found"
        )

    appointment.doctor_id = updated.doctor_id
    appointment.patient_id = updated.patient_id
    appointment.date_time = updated.date_time

    db.commit()
    db.refresh(appointment)

    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "patient_name": patient.name,
        "doctor_name": doctor.name,
        "date_time": appointment.date_time,
        "status": appointment.status,
    }


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully"
    }