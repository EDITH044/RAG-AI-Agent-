"""
LoadWise AI – Smart Building Load Balancing Advisor
A multi-agent AI application powered by IBM watsonx.ai Granite Models.
Flask application with separated frontend/backend.
"""

import os
from flask import Flask, render_template, request, jsonify
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────
IBM_API_KEY    = os.environ.get("IBM_API_KEY",    "k0XTipxR-x0F98nUm-A69s9MgC0J0nOurM4JT6UycccC")
IBM_PROJECT_ID = os.environ.get("IBM_PROJECT_ID", "1167a783-b1bf-410a-b13a-261f15d4a582")
IBM_URL        = os.environ.get("IBM_URL",        "https://us-south.ml.cloud.ibm.com")
MODEL_ID       = "meta-llama/llama-3-3-70b-instruct"

app = Flask(__name__)

# ──────────────────────────────────────────────
# watsonx.ai helper
# ──────────────────────────────────────────────
def get_model():
    credentials = Credentials(url=IBM_URL, api_key=IBM_API_KEY)
    client = APIClient(credentials=credentials, project_id=IBM_PROJECT_ID)
    params = {
        GenParams.MAX_NEW_TOKENS: 1024,
        GenParams.MIN_NEW_TOKENS: 80,
        GenParams.TEMPERATURE: 0.7,
        GenParams.TOP_P: 0.9,
        GenParams.REPETITION_PENALTY: 1.1,
    }
    return ModelInference(model_id=MODEL_ID, api_client=client, params=params)

def query_granite(prompt: str) -> str:
    try:
        model = get_model()
        response = model.generate_text(prompt=prompt)
        return response.strip() if isinstance(response, str) else str(response)
    except Exception as e:
        return f"[watsonx.ai Error] {str(e)}"

# ──────────────────────────────────────────────
# Agent 1 – Load Monitoring & Analysis
# ──────────────────────────────────────────────
def agent_load_monitoring(data: dict) -> str:
    building_type  = data.get("building_type", "Commercial Office")
    floors         = data.get("floors", "10")
    daily_kwh      = data.get("daily_kwh", "5000")
    hourly_usage   = data.get("hourly_usage", "")
    smart_meter    = data.get("smart_meter", "")
    dept_data      = data.get("dept_data", "")
    equipment_logs = data.get("equipment_logs", "")
    question       = data.get("question", "Analyze my building's energy usage.")
    systems_list   = data.get("systems", [])
    systems_str    = ", ".join(systems_list) if systems_list else "HVAC, Lighting, Elevators, Office Equipment"

    prompt = f"""You are an expert Building Energy Analyst AI Agent specializing in electricity consumption monitoring.

Building Profile:
- Building Type: {building_type}
- Number of Floors: {floors}
- Daily Electricity Consumption: {daily_kwh} kWh
- Active Building Systems: {systems_str}
- Hourly Energy Usage: {hourly_usage if hourly_usage else 'Not provided'}
- Smart Meter Readings: {smart_meter if smart_meter else 'Not provided'}
- Department/Floor-wise Consumption: {dept_data if dept_data else 'Not provided'}
- Equipment Energy Logs: {equipment_logs if equipment_logs else 'Not provided'}

User Question: {question}

Provide a comprehensive Load Monitoring & Analysis report with the following clearly labeled sections:

## 1. Electricity Consumption Summary
Summarize the overall consumption pattern and total energy usage for this building profile.

## 2. Load Distribution Analysis
Explain how electrical loads are distributed across the active building systems. Identify which system consumes the most electricity and why.

## 3. Department / System-wise Consumption Breakdown
Provide a detailed breakdown of consumption per system or department based on the data provided. Use approximate percentages.

## 4. Daily & Weekly Energy Trends
Describe expected daily usage peaks and valleys. Explain weekly patterns relevant to the building type.

## 5. AI Insights & Key Observations
Highlight any anomalies, inefficiencies, or noteworthy patterns detected in this building's energy consumption.

Be specific, data-driven, and actionable. Format your response clearly with headings.
"""
    return query_granite(prompt)

# ──────────────────────────────────────────────
# Agent 2 – Peak Load Detection
# ──────────────────────────────────────────────
def agent_peak_load(data: dict) -> str:
    hourly_readings  = data.get("hourly_readings", "")
    daily_profile    = data.get("daily_profile", "")
    max_demand       = data.get("max_demand", "")
    historical_data  = data.get("historical_data", "")
    question         = data.get("question", "When is my building consuming the most electricity?")
    building_type    = data.get("building_type", "Commercial Office")

    prompt = f"""You are an expert Peak Load Detection AI Agent specializing in identifying electricity demand spikes and abnormal consumption in buildings.

Input Data:
- Building Type: {building_type}
- Hourly Load Readings (kW): {hourly_readings if hourly_readings else 'Not provided'}
- Daily Demand Profile: {daily_profile if daily_profile else 'Not provided'}
- Maximum Demand Value (kW): {max_demand if max_demand else 'Not provided'}
- Historical Consumption Data: {historical_data if historical_data else 'Not provided'}

User Question: {question}

Provide a detailed Peak Load Detection Report with the following clearly labeled sections:

## 1. Peak Demand Periods Identified
Identify the top peak demand windows during the day and week. Specify exact hours where maximum demand occurs.

## 2. Load Spike Detection & Alerts
Detect any abnormal consumption spikes. Classify each spike as: Low Risk / Medium Risk / High Risk. Explain what triggered each spike.

## 3. Abnormal Consumption Alerts
List specific alerts for unusual demand patterns. Describe what could be causing them.

## 4. Equipment Causing Peak Demand
Identify which building systems or equipment are most likely responsible for peak demand events.

## 5. Risk Assessment
Assess the financial and operational risks associated with the detected peaks — including demand charges, grid instability, and equipment stress.

## 6. AI Demand Behavior Explanation
Provide an intelligent narrative explanation of the building's demand behavior, including contributing factors and temporal patterns.

Be specific, technical, and actionable.
"""
    return query_granite(prompt)

# ──────────────────────────────────────────────
# Agent 3 – Smart Load Balancing Recommendations
# ──────────────────────────────────────────────
def agent_load_balancing(data: dict) -> str:
    schedules       = data.get("schedules", "")
    working_hours   = data.get("working_hours", "9 AM – 6 PM")
    critical_equip  = data.get("critical_equip", "")
    flexible_loads  = data.get("flexible_loads", "")
    occupancy       = data.get("occupancy", "")
    seasonal        = data.get("seasonal", "")
    peak_period     = data.get("peak_period", "")
    building_type   = data.get("building_type", "Commercial Office")
    question        = data.get("question", "How can I balance my building loads to reduce peak demand?")

    prompt = f"""You are a Smart Load Balancing AI Agent for buildings, expert in demand response and intelligent load scheduling.

Building Context:
- Building Type: {building_type}
- Working Hours: {working_hours}
- Operating Schedules: {schedules if schedules else 'Standard office schedule'}
- Critical Equipment (cannot be interrupted): {critical_equip if critical_equip else 'Servers, Safety systems'}
- Flexible / Deferrable Loads: {flexible_loads if flexible_loads else 'EV charging, water pumps, pre-cooling'}
- Occupancy Pattern: {occupancy if occupancy else 'Not provided'}
- Seasonal Considerations: {seasonal if seasonal else 'Not provided'}
- Current Peak Period: {peak_period if peak_period else 'Not provided'}

User Question: {question}

Provide a comprehensive Smart Load Balancing Recommendation Report with the following clearly labeled sections:

## 1. Recommended Appliance Scheduling Plan
Provide a specific time-table for when each flexible load should operate to avoid peak demand hours.

## 2. Load Shifting Strategies
Explain 3-5 actionable load shifting strategies customized for this building type and schedule.

## 3. Time-Based Optimization Plan
Design a 24-hour optimized load schedule that minimizes peak demand while maintaining full building operations.

## 4. Demand Balancing Recommendations
Suggest specific demand balancing techniques: load rotation, staggered starts, pre-conditioning, etc.

## 5. Smart Automation Suggestions
Recommend Building Management System (BMS) automation rules, IoT sensor integrations, and smart control strategies.

## 6. Priority-Based Load Allocation
Define load priority tiers (Critical / High / Medium / Deferrable) and allocation rules during peak events.

## 7. Estimated Peak Demand Reduction
Estimate the expected reduction in peak demand (in %) if these recommendations are implemented.

Be practical, specific, and prioritize recommendations with the greatest impact first.
"""
    return query_granite(prompt)

# ──────────────────────────────────────────────
# Agent 4 – Energy Optimization Insights
# ──────────────────────────────────────────────
def agent_energy_optimization(data: dict) -> str:
    building_type    = data.get("building_type", "Commercial Office")
    floors           = data.get("floors", "10")
    annual_kwh       = data.get("annual_kwh", "")
    current_systems  = data.get("current_systems", "")
    budget_range     = data.get("budget_range", "")
    sustainability   = data.get("sustainability_goals", "")
    question         = data.get("question", "What are the best strategies to improve my building's energy efficiency?")
    pain_points      = data.get("pain_points", "")

    prompt = f"""You are an Energy Optimization AI Agent specializing in long-term building efficiency, cost reduction, and sustainability.

Building Profile:
- Building Type: {building_type}
- Number of Floors: {floors}
- Annual Electricity Consumption: {annual_kwh if annual_kwh else 'Not provided'} kWh/year
- Current Building Systems: {current_systems if current_systems else 'Standard HVAC, conventional lighting, basic BMS'}
- Budget Range for Improvements: {budget_range if budget_range else 'Not specified'}
- Sustainability Goals: {sustainability if sustainability else 'Reduce costs and carbon footprint'}
- Key Pain Points: {pain_points if pain_points else 'High electricity bills, peak demand charges'}

User Question: {question}

Provide a comprehensive Energy Optimization Insights Report with the following clearly labeled sections:

## 1. Peak Demand Reduction Strategies
List the top strategies to reduce peak demand charges with estimated savings percentages.

## 2. Cost-Saving Opportunities
Identify 5-7 specific cost reduction opportunities with estimated annual savings and payback periods.

## 3. Building Efficiency Improvements
Recommend building envelope, HVAC, and operational improvements to reduce baseline consumption.

## 4. Smart Building Automation Recommendations
Suggest IoT, AI, and BMS technologies that would deliver the highest ROI for this building type.

## 5. Energy-Efficient Equipment Upgrades
Recommend specific equipment upgrades (HVAC, lighting, motors) with efficiency ratings and expected savings.

## 6. Sustainability & Carbon Footprint Reduction
Outline renewable energy integration options, carbon reduction targets, and green certification pathways.

## 7. Predictive Maintenance Recommendations
Describe how predictive maintenance can prevent energy waste and reduce equipment downtime.

## 8. Implementation Roadmap
Provide a phased 3-year implementation plan prioritizing quick wins, medium-term upgrades, and long-term investments.

Be specific, financially grounded, and sustainability-focused.
"""
    return query_granite(prompt)

# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/agent1", methods=["POST"])
def api_agent1():
    data = request.get_json(force=True)
    return jsonify({"result": agent_load_monitoring(data)})

@app.route("/api/agent2", methods=["POST"])
def api_agent2():
    data = request.get_json(force=True)
    return jsonify({"result": agent_peak_load(data)})

@app.route("/api/agent3", methods=["POST"])
def api_agent3():
    data = request.get_json(force=True)
    return jsonify({"result": agent_load_balancing(data)})

@app.route("/api/agent4", methods=["POST"])
def api_agent4():
    data = request.get_json(force=True)
    return jsonify({"result": agent_energy_optimization(data)})

# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
