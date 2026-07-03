async def get_education_advice(village_data: dict) -> dict:
    population = village_data.get('population', 0)
    num_schools = village_data.get('num_schools', 0)
    name = village_data.get('name', 'Unknown')

    children = population // 4
    teachers_needed = max(0, (children // 30) - (num_schools * 3))
    schools_needed = max(0, (population // 1500) - num_schools)

    advice = f"""EDUCATION IMPROVEMENT PLAN FOR {name.upper()}

Population: {population} | Existing schools: {num_schools}
Estimated children (under 14): {children}

1. SCHOOLS NEEDED: {schools_needed} new schools
   - 1 school per 1500 population is standard
   - Each school needs minimum 3 classrooms
   - Construction cost: Rs.15-20 lakhs per school

2. TEACHERS REQUIRED: {teachers_needed} additional teachers
   - Current ratio: 1 teacher per 30 students recommended
   - Apply under Samagra Shiksha for teacher recruitment
   - Focus on Math, Science, English teachers

3. INFRASTRUCTURE IMPROVEMENTS:
   - Build separate toilets for girls (increases attendance by 40%)
   - Install drinking water facility in every school
   - Boundary wall and proper gate for safety
   - Cost: Rs.3-5 lakhs per school for basic facilities

4. DIGITAL LEARNING CENTER:
   - Set up 1 computer lab with 10 computers
   - Install projector in each classroom
   - Connect to PM eVidya for digital content
   - Cost: Rs.5 lakhs for full setup

5. SMART CLASSROOM:
   - Interactive digital board in senior classes
   - Solar power backup for uninterrupted learning
   - Cost: Rs.2 lakhs per smart classroom

6. DROPOUT PREVENTION:
   - Mid-day meal program (increases attendance by 25%)
   - Free uniforms and books under state schemes
   - Monthly parent-teacher meetings

GOVERNMENT SCHEMES:
   - Samagra Shiksha Abhiyan (school construction funding)
   - PM Poshan (mid-day meal scheme)
   - Eklavya Digital Classrooms (free digital equipment)
   - National Scholarship Portal (scholarships for students)"""

    return {
        "module": "education",
        "priority": "high" if schools_needed > 0 else "medium",
        "title": "Education Infrastructure Plan",
        "content": advice,
        "cost_lakhs": 20.0
    }