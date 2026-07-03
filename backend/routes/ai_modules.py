from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Village
from modules.agriculture import get_agriculture_advice
from modules.water import get_water_advice
from modules.healthcare import get_healthcare_advice
from modules.education import get_education_advice
from modules.schemes import get_scheme_recommendations

router = APIRouter(prefix="/api", tags=["AI Modules"])

@router.post("/agriculture/{village_id}")
async def agriculture_advice(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return await get_agriculture_advice({
        "name": village.name, "rainfall_mm": village.rainfall_mm,
        "soil_type": village.soil_type, "primary_crops": village.primary_crops,
        "area_hectares": village.area_hectares, "state": village.state,
    })

@router.post("/water/{village_id}")
async def water_advice(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return await get_water_advice({
        "name": village.name, "rainfall_mm": village.rainfall_mm,
        "water_sources": village.water_sources, "population": village.population,
        "area_hectares": village.area_hectares,
    })

@router.post("/healthcare/{village_id}")
async def healthcare_advice(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return await get_healthcare_advice({
        "name": village.name, "population": village.population,
        "num_health_centers": village.num_health_centers,
    })

@router.post("/education/{village_id}")
async def education_advice(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return await get_education_advice({
        "name": village.name, "population": village.population,
        "num_schools": village.num_schools,
    })

@router.post("/schemes/{village_id}")
async def scheme_recommendations(village_id: int, db: Session = Depends(get_db)):
    village = db.query(Village).filter(Village.id == village_id).first()
    if not village:
        raise HTTPException(status_code=404, detail="Village not found")
    return await get_scheme_recommendations({
        "name": village.name, "rainfall_mm": village.rainfall_mm,
        "num_schools": village.num_schools, "num_health_centers": village.num_health_centers,
        "population": village.population, "budget_lakhs": village.budget_lakhs,
    })