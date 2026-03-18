from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime
import uvicorn

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./iot_devices.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    status = Column(String, index=True)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    preferences = Column(String)

class AnalyticsData(Base):
    __tablename__ = 'analytics_data'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    device_id = Column(Integer, index=True)
    metric = Column(String)
    value = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
def seed_data(db: Session):
    if not db.query(Device).first():
        db.add_all([
            Device(type="Temperature Sensor", status="active"),
            Device(type="Humidity Sensor", status="inactive")
        ])
        db.commit()

    if not db.query(UserProfile).first():
        db.add(UserProfile(username="admin", email="admin@example.com", preferences="{}"))
        db.commit()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request, db: Session = Depends(get_db)):
    seed_data(db)
    devices = db.query(Device).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "devices": devices})

@app.get("/devices", response_class=HTMLResponse)
async def manage_devices(request: Request, db: Session = Depends(get_db)):
    devices = db.query(Device).all()
    return templates.TemplateResponse("devices.html", {"request": request, "devices": devices})

@app.get("/analytics", response_class=HTMLResponse)
async def view_analytics(request: Request, db: Session = Depends(get_db)):
    analytics_data = db.query(AnalyticsData).all()
    return templates.TemplateResponse("analytics.html", {"request": request, "analytics_data": analytics_data})

@app.get("/profile", response_class=HTMLResponse)
async def user_profile(request: Request, db: Session = Depends(get_db)):
    user_profile = db.query(UserProfile).first()
    return templates.TemplateResponse("profile.html", {"request": request, "user_profile": user_profile})

@app.get("/api/devices")
async def get_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()

@app.post("/api/devices")
async def create_device(device: Device, db: Session = Depends(get_db)):
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@app.get("/api/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    return db.query(AnalyticsData).all()

@app.get("/api/user/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    return db.query(UserProfile).first()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
