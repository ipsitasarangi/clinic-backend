from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# Roles
class UserRole(str, Enum):
    admin = "admin"
    receptionist = "receptionist"
    doctor = "doctor"

# User schemas
class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        from_attributes = True

# Doctor schemas
class DoctorBase(BaseModel):
    name: str
    specialization: str

class DoctorCreate(DoctorBase):
    pass

class DoctorRead(DoctorBase):
    id: int
    class Config:
        from_attributes = True

# Patient schemas
class PatientBase(BaseModel):
    name: str
    age: int
    gender: str

class PatientCreate(PatientBase):
    pass

class PatientRead(PatientBase):
    id: int
    class Config:
        from_attributes = True

# Appointment schemas
class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentRead(AppointmentBase):
    id: int
    class Config:
        from_attributes = True
