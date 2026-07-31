from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment

from app.routers.auth_routes import router as auth_router
from app.routers.patient_routes import router as patient_router
from app.routers.doctor_routes import router as doctor_router
from app.routers.appointment_routes import router as appointment_router
from app.routers.dashboard import router as dashboard_router


app = FastAPI(
    title="Niyati Clinic Appointment System"
)


# CORS Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",

        # Deployment ke baad yahan frontend URL add karna
        # "https://your-frontend-url.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
Base.metadata.create_all(bind=engine)


# API Routers
app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(dashboard_router)


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "clinic-api",
        "stack": "FastAPI"
    }


@app.get("/api/ping")
def ping():
    return {
        "ok": True,
        "message": "pong"
    }


@app.post("/api/version")
def version():
    return {
        "version": "production-v1",
        "runtime": "python",
        "deploy_target": "render"
    }