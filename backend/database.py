from sqlalchemy import (
    create_engine, Column, Integer, String, Float,
    Text, DateTime, ForeignKey, Boolean
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin123@localhost:5432/village_planner")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Village(Base):
    __tablename__ = "villages"
    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(200), nullable=False)
    district       = Column(String(200))
    state          = Column(String(100), default="Karnataka")
    population     = Column(Integer, nullable=False)
    area_hectares  = Column(Float, nullable=False)
    rainfall_mm    = Column(Float, nullable=False)
    water_sources  = Column(Integer, default=0)
    num_schools    = Column(Integer, default=0)
    num_health_centers = Column(Integer, default=0)
    primary_crops  = Column(String(500))
    soil_type      = Column(String(100))
    budget_lakhs   = Column(Float, default=0)
    electricity    = Column(Boolean, default=True)
    road_connectivity = Column(Boolean, default=True)
    created_at     = Column(DateTime, default=datetime.utcnow)
    recommendations = relationship("Recommendation", back_populates="village")

class Recommendation(Base):
    __tablename__ = "recommendations"
    id          = Column(Integer, primary_key=True, index=True)
    village_id  = Column(Integer, ForeignKey("villages.id"), nullable=False)
    module      = Column(String(50))
    priority    = Column(String(20))
    title       = Column(String(300))
    content     = Column(Text)
    cost_lakhs  = Column(Float, default=0)
    created_at  = Column(DateTime, default=datetime.utcnow)
    village = relationship("Village", back_populates="recommendations")

def init_db():
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()