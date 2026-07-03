def analyze_village(data: dict) -> dict:
    population      = data["population"]
    area            = data["area_hectares"]
    rainfall        = data["rainfall_mm"]
    water_sources   = data["water_sources"]
    num_schools     = data["num_schools"]
    num_health      = data["num_health_centers"]
    budget          = data["budget_lakhs"]

    metrics = []

    density = population / area if area > 0 else 0
    metrics.append({
        "label": "Population Density",
        "value": f"{density:.1f} people/hectare",
        "status": "good" if density < 5 else "warning" if density < 10 else "critical",
        "detail": "High density strains infrastructure." if density >= 10 else "Density is manageable."
    })

    metrics.append({
        "label": "Rainfall Status",
        "value": f"{rainfall} mm/year",
        "status": "critical" if rainfall < 400 else "warning" if rainfall < 600 else "good",
        "detail": "Severely drought-prone." if rainfall < 400 else "Below ideal." if rainfall < 600 else "Adequate rainfall."
    })

    water_per_1000 = (water_sources / population) * 1000 if population > 0 else 0
    metrics.append({
        "label": "Water Source Coverage",
        "value": f"{water_sources} sources",
        "status": "critical" if water_per_1000 < 0.1 else "warning" if water_per_1000 < 0.3 else "good",
        "detail": "No reliable water infrastructure." if water_per_1000 < 0.1 else "Limited coverage." if water_per_1000 < 0.3 else "Adequate."
    })

    school_ratio = (num_schools / population) * 1000 if population > 0 else 0
    metrics.append({
        "label": "School Coverage",
        "value": f"{num_schools} schools",
        "status": "critical" if school_ratio < 0.2 else "warning" if school_ratio < 0.5 else "good",
        "detail": "Critically under-served." if school_ratio < 0.2 else "Below recommended." if school_ratio < 0.5 else "Adequate."
    })

    health_ratio = (num_health / population) * 10000 if population > 0 else 0
    metrics.append({
        "label": "Healthcare Coverage",
        "value": f"{num_health} centers",
        "status": "critical" if health_ratio < 0.5 else "warning" if health_ratio < 1.0 else "good",
        "detail": "No healthcare access." if health_ratio < 0.5 else "Below standard." if health_ratio < 1.0 else "Adequate."
    })

    budget_per_person = (budget * 100000) / population if population > 0 else 0
    metrics.append({
        "label": "Budget per Person",
        "value": f"Rs.{budget_per_person:,.0f} per person",
        "status": "critical" if budget_per_person < 500 else "warning" if budget_per_person < 2000 else "good",
        "detail": "Very limited budget." if budget_per_person < 500 else "Moderate budget." if budget_per_person < 2000 else "Good budget."
    })

    all_statuses = [m["status"] for m in metrics]
    overall = "critical" if "critical" in all_statuses else "warning" if "warning" in all_statuses else "good"

    gaps = {
        "water_stressed":   rainfall < 600,
        "no_water_sources": water_per_1000 < 0.1,
        "school_gap":       school_ratio < 0.5,
        "health_gap":       health_ratio < 1.0,
        "low_budget":       budget_per_person < 500,
    }

    return {
        "metrics": metrics,
        "overall_status": overall,
        "gaps": gaps
    }