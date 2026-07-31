from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment

router = APIRouter(
    prefix="/api",
    tags=["Dashboard"]
)


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()
    total_appointments = db.query(Appointment).count()

    today = date.today()

    appointments = (
        db.query(Appointment)
        .all()
    )

    today_appointments = []

    for appointment in appointments:

        if appointment.date_time.date() == today:

            today_appointments.append({
                "id": appointment.id,
                "patient": appointment.patient.name,
                "doctor": appointment.doctor.name,
                "time": appointment.date_time.strftime("%I:%M %p"),
                "status": appointment.status
            })

    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "today_appointments": today_appointments
    }