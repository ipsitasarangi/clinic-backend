from pydantic import BaseModel
from datetime import datetime


# ---------------- User ----------------

class UserLogin(BaseModel):
    username: str
    password: str


# ---------------- Doctor ----------------

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: str


class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True


# ---------------- Patient ----------------

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: str
    address: str


class PatientResponse(PatientCreate):
    id: int

    class Config:
        from_attributes = True


# ---------------- Appointment ----------------

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    date_time: datetime

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    patient_name: str
    doctor_name: str
    date_time: datetime
    status: str

    class Config:
        from_attributes = True