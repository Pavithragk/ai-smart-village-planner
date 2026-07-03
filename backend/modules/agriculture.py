import os
from dotenv import load_dotenv

load_dotenv()

async def get_agriculture_advice(village_data: dict) -> dict:
    rainfall = village_data.get('rainfall_mm', 0)
    soil = village_data.get('soil_type', 'loamy')
    crops = village_data.get('primary_crops', 'unknown')
    area = village_data.get('area_hectares', 0)
    name = village_data.get('name', 'Unknown')

    if rainfall < 400:
        crop_rec = "Millets, Sorghum, Groundnut (drought resistant crops)"
        irrigation = "Drip irrigation is essential - water scarcity is critical"
    elif rainfall < 600:
        crop_rec = "Ragi, Maize, Pulses (moderate water crops)"
        irrigation = "Sprinkler irrigation recommended"
    else:
        crop_rec = "Rice, Sugarcane, Vegetables (good rainfall crops)"
        irrigation = "Canal or borewell irrigation suitable"

    if soil == "loamy":
        fertilizer = "NPK 10:26:26 for base, Urea top dressing after 30 days"
    elif soil == "sandy":
        fertilizer = "Organic manure + NPK 20:20:0, frequent small doses"
    else:
        fertilizer = "Lime treatment first, then NPK 14:35:14"

    advice = f"""AGRICULTURE RECOMMENDATIONS FOR {name.upper()}

1. RECOMMENDED CROPS:
   {crop_rec}
   Current crops ({crops}) can continue alongside new ones.

2. IRRIGATION METHOD:
   {irrigation}
   For {area} hectares, install drip system in phases.

3. FERTILIZER SCHEDULE:
   {fertilizer}
   Apply before sowing, top dress at 30 and 60 days.

4. PEST MANAGEMENT:
   - Use neem oil spray (5ml/liter) for organic pest control
   - Install yellow sticky traps for whitefly control
   - Crop rotation every 2 seasons to reduce soil pests

5. EXPECTED YIELD IMPROVEMENT:
   With proper irrigation and fertilizer: 30-40% yield increase
   Estimated additional income: Rs.15,000-25,000 per acre per season

GOVERNMENT SCHEMES TO APPLY:
   - PM Krishi Sinchai Yojana (free drip irrigation subsidy)
   - Soil Health Card Scheme (free soil testing)
   - PM Fasal Bima Yojana (crop insurance)"""

    return {
        "module": "agriculture",
        "priority": "high",
        "title": "Agriculture & Crop Recommendations",
        "content": advice,
        "cost_lakhs": 5.0
    }