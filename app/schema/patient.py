from pydantic import BaseModel


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    email: str


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    phone: str
    email: str

    class Config:
        from_attributes = True