from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Village
from schemas import VillageCreate, VillageResponse, AnalysisResponse
from modules.analyzer import analyze_village

router = APIRouter(prefix="/api/villages", tags=["Villages"])

@router.post("/", response_model=VillageResponse, status_code=201)
def create_village(village_data: VillageCreate, db: Session = Depends(get_db)):
    village = Village(**village_data.model_dump())
    db.add(village)
    db.commit()
    db.refresh(village)
    return village

@router.get("/", response_model=List[VillageResponse])
def list_villages(db: Session = Depends(get_db)):
    return db.query(Village).order_by(Village.created_at.desc()).all()

@router.get("/{village_id}", response_model=VillageResponse)
def get_village(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return village

@router.get("/{village_id}/analyze", response_model=AnalysisResponse)
def analyze(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    village_dict = {
        "population":         village.population,
        "area_hectares":      village.area_hectares,
        "rainfall_mm":        village.rainfall_mm,
        "water_sources":      village.water_sources,
        "num_schools":        village.num_schools,
        "num_health_centers": village.num_health_centers,
        "budget_lakhs":       village.budget_lakhs,
    }
    result = analyze_village(village_dict)
    return {
        "village_id":     village.id,
        "village_name":   village.name,
        "metrics":        result["metrics"],
        "overall_status": result["overall_status"],
    }

@router.delete("/{village_id}", status_code=204)
def delete_village(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    db.delete(village)
    db.commit()