async def get_scheme_recommendations(village_data: dict) -> dict:
    rainfall = village_data.get('rainfall_mm', 0)
    num_schools = village_data.get('num_schools', 0)
    num_health = village_data.get('num_health_centers', 0)
    population = village_data.get('population', 0)
    budget = village_data.get('budget_lakhs', 0)
    name = village_data.get('name', 'Unknown')

    schemes = []

    schemes.append({
        "name": "PM Krishi Sinchai Yojana (PMKSY)",
        "ministry": "Ministry of Agriculture",
        "benefit": "Free drip/sprinkler irrigation equipment, 55-90% subsidy",
        "amount": "Up to Rs.50,000 per hectare subsidy",
        "apply": "Visit nearest agriculture office or pmksy.gov.in"
    })

    if rainfall < 600:
        schemes.append({
            "name": "Pradhan Mantri Fasal Bima Yojana",
            "ministry": "Ministry of Agriculture",
            "benefit": "Crop insurance against drought, flood, pest attacks",
            "amount": "Premium only 2% for Kharif, 1.5% for Rabi crops",
            "apply": "Apply through bank or insurance company before sowing"
        })

    schemes.append({
        "name": "Jal Jeevan Mission",
        "ministry": "Ministry of Jal Shakti",
        "benefit": "Piped drinking water to every household by 2024",
        "amount": "Full funding from central government",
        "apply": "Contact District Collector or jaljeevanmission.gov.in"
    })

    if num_health < 1:
        schemes.append({
            "name": "Ayushman Bharat - PM Jan Arogya Yojana",
            "ministry": "Ministry of Health",
            "benefit": "Rs.5 lakh health insurance per family per year",
            "amount": "Rs.5,00,000 per family annually",
            "apply": "Register at nearest CSC center or pmjay.gov.in"
        })

    schemes.append({
        "name": "National Health Mission (NHM)",
        "ministry": "Ministry of Health",
        "benefit": "Free PHC construction, mobile health units, ASHA workers",
        "amount": "Rs.25-30 lakhs per PHC construction",
        "apply": "Apply through District Health Officer"
    })

    if num_schools < 2:
        schemes.append({
            "name": "Samagra Shiksha Abhiyan",
            "ministry": "Ministry of Education",
            "benefit": "School construction, teacher recruitment, digital classrooms",
            "amount": "Rs.15-20 lakhs per school construction",
            "apply": "Apply through District Education Officer"
        })

    schemes.append({
        "name": "PM Poshan Shakti Nirman (Mid-Day Meal)",
        "ministry": "Ministry of Education",
        "benefit": "Free nutritious meal for all school children",
            "amount": "Rs.8-12 per child per day funded by government",
        "apply": "Automatic for all government schools"
    })

    schemes.append({
        "name": "MNREGA (Mahatma Gandhi NREGA)",
        "ministry": "Ministry of Rural Development",
        "benefit": "100 days guaranteed employment, pond/road construction",
        "amount": "Rs.267/day wages + free infrastructure work",
        "apply": "Register at Gram Panchayat office"
    })

    schemes.append({
        "name": "PM Awaas Yojana - Gramin",
        "ministry": "Ministry of Rural Development",
        "benefit": "Free house construction for homeless/kutcha house families",
        "amount": "Rs.1.20 lakhs per house (plain areas)",
        "apply": "Apply through Gram Panchayat or pmayg.nic.in"
    })

    if population > 3000:
        schemes.append({
            "name": "Smart Village Initiative",
            "ministry": "Ministry of Electronics & IT",
            "benefit": "WiFi hotspot, digital literacy, e-governance services",
            "amount": "Full infrastructure funded by government",
            "apply": "Apply through District Collector office"
        })

    content = f"GOVERNMENT SCHEMES FOR {name.upper()}\n\n"
    content += f"Total schemes identified: {len(schemes)}\n"
    content += "=" * 50 + "\n\n"

    for i, s in enumerate(schemes, 1):
        content += f"{i}. {s['name']}\n"
        content += f"   Ministry: {s['ministry']}\n"
        content += f"   Benefit: {s['benefit']}\n"
        content += f"   Amount: {s['amount']}\n"
        content += f"   How to Apply: {s['apply']}\n\n"

    return {
        "module": "schemes",
        "priority": "high",
        "title": "Government Schemes & Funding",
        "content": content,
        "cost_lakhs": 0.0,
        "schemes_count": len(schemes)
    }