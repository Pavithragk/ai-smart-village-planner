async def get_healthcare_advice(village_data: dict) -> dict:
    population = village_data.get('population', 0)
    health_centers = village_data.get('num_health_centers', 0)
    name = village_data.get('name', 'Unknown')

    centers_needed = max(0, (population // 3000) - health_centers)
    doctors_needed = max(1, population // 2000)

    advice = f"""HEALTHCARE PLAN FOR {name.upper()}

Population: {population} | Existing centers: {health_centers}

1. PRIMARY HEALTH CENTERS NEEDED: {centers_needed} new centers
   - 1 PHC per 3000 population is standard
   - Each PHC needs: 1 doctor, 2 nurses, 1 lab technician
   - Construction cost: Rs.25-30 lakhs per PHC

2. MOBILE HEALTH CLINIC:
   - Deploy 1 mobile van visiting every week
   - Cover remote hamlets within 5km radius
   - Cost: Rs.8 lakhs for vehicle + Rs.2 lakhs/year operating

3. DOCTORS & STAFF NEEDED:
   - Doctors required: {doctors_needed}
   - ANM (Auxiliary Nurse Midwife): {population // 1000} posts
   - ASHA workers: {population // 1000} workers (1 per 1000 population)

4. VACCINATION DRIVES:
   - Monthly immunization camps for children under 5
   - Quarterly health checkup camps for all residents
   - Annual eye/dental camps

5. TELEMEDICINE:
   - Connect existing center to district hospital via video
   - Cost: Rs.50,000 for equipment setup
   - Enables specialist consultation without travel

GOVERNMENT SCHEMES:
   - Ayushman Bharat (Rs.5 lakh health insurance per family)
   - PM Jan Arogya Yojana (free treatment at empanelled hospitals)
   - National Health Mission (PHC construction funding)
   - Rashtriya Bal Swasthya Karyakram (child health screening)"""

    return {
        "module": "healthcare",
        "priority": "high" if health_centers == 0 else "medium",
        "title": "Healthcare Development Plan",
        "content": advice,
        "cost_lakhs": 35.0
    }