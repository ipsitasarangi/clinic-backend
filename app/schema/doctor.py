from pydantic import BaseModel


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str
    email: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str
    email: str

    class Config:
        from_attributes = True