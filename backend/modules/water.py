async def get_water_advice(village_data: dict) -> dict:
    rainfall = village_data.get('rainfall_mm', 0)
    water_sources = village_data.get('water_sources', 0)
    population = village_data.get('population', 0)
    area = village_data.get('area_hectares', 0)
    name = village_data.get('name', 'Unknown')

    borewells_needed = max(0, (population // 500) - water_sources)

    if rainfall < 400:
        situation = "CRITICAL - Severely drought prone"
        harvesting = "Build 3 check dams + 5 farm ponds immediately"
        priority = "critical"
    elif rainfall < 600:
        situation = "WARNING - Below average rainfall"
        harvesting = "Build 2 check dams + rainwater harvesting tanks"
        priority = "high"
    else:
        situation = "MODERATE - Average rainfall"
        harvesting = "Build 1 check dam + improve existing water sources"
        priority = "medium"

    advice = f"""WATER MANAGEMENT PLAN FOR {name.upper()}

CURRENT STATUS: {situation}
Rainfall: {rainfall} mm/year | Existing sources: {water_sources} | Population: {population}

1. RAINWATER HARVESTING:
   {harvesting}
   Each farm pond (30x30x3m) can store 2.7 lakh litres
   Cost estimate: Rs.1.5-2 lakhs per pond

2. BOREWELL RECOMMENDATIONS:
   Borewells needed: {borewells_needed} new borewells
   Recommended depth: 200-250 feet for this region
   Cost: Rs.1.5 lakhs per borewell
   Total borewell cost: Rs.{borewells_needed * 1.5:.1f} lakhs

3. CHECK DAM CONSTRUCTION:
   Location: Identify lowest point of village boundary
   Size: 20m width x 2m height recommended
   Storage capacity: 50,000 to 1,00,000 litres
   Cost estimate: Rs.8-12 lakhs per check dam

4. WATER CONSERVATION STRATEGIES:
   - Install water meters in all households
   - Repair all leaking pipes (reduces wastage by 30%)
   - Plant trees along water channels to reduce evaporation
   - Promote drip irrigation for all farms (saves 50% water)

5. WATER REQUIREMENT VS AVAILABILITY:
   Daily requirement: {population * 55} litres/day ({population} people x 55L)
   Current availability: {water_sources * 50000} litres/day (estimated)
   Deficit: {max(0, population * 55 - water_sources * 50000)} litres/day

GOVERNMENT SCHEMES:
   - Jal Jeevan Mission (free piped water to all homes)
   - PMKSY Watershed Development (check dam funding)
   - MNREGA (free labor for pond construction)
   - National Water Mission (grants up to Rs.25 lakhs)"""

    return {
        "module": "water",
        "priority": priority,
        "title": "Water Management Plan",
        "content": advice,
        "cost_lakhs": 25.0
    }