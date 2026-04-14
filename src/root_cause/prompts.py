ROOT_CAUSE_PROMPTS = {
    "delay_prediction": """You are a logistics expert analyzing delivery delays.

SHAP Feature Values (positive = increases delay probability):
{shap_values}

Delivery Context:
- Origin: {origin}
- Destination: {destination}
- Distance: {distance} km
- Weather: {weather}
- Traffic Level: {traffic}

Task: Identify the top 3 root causes of potential delay and explain each in one sentence.
Format: 1. [Feature]: [Explanation]""",
    "driver_analysis": """Analyze driver-related delay factors:

Driver Performance:
- On-time rate: {on_time_rate}%
- Average speed: {avg_speed} km/h
- Experience: {experience} years
- Current load: {current_load} deliveries

Task: Explain which factors most contribute to delay risk.""",
    "weather_impact": """Analyze weather impact on delivery:

Weather Conditions:
- Temperature: {temperature}°C
- Precipitation: {precipitation} mm
- Wind: {wind} km/h
- Visibility: {visibility} km

Task: Determine if weather conditions will cause delays and explain why.""",
    "route_analysis": """Analyze route-related delay factors:

Route Information:
- Distance: {distance} km
- Estimated duration: {duration} min
- Number of stops: {stops}
- Traffic patterns: {traffic_pattern}

Task: Identify route factors contributing to potential delay.""",
    "traffic_analysis": """Analyze traffic impact on delivery:

Traffic Conditions:
- Current index: {traffic_index}
- Peak hours: {peak_hours}
- Road type: {road_type}
- Construction zones: {construction}

Task: Assess how traffic will affect delivery timing.""",
    "warehouse_analysis": """Analyze warehouse impact on delivery:

Warehouse Status:
- Processing time: {processing_time} min
- Queue length: {queue_length}
- Staff available: {staff_available}
- Current load: {warehouse_load}%

Task: Determine warehouse contribution to potential delay.""",
}


def build_prompt(prompt_type: str, **kwargs) -> str:
    prompt_template = ROOT_CAUSE_PROMPTS.get(
        prompt_type, ROOT_CAUSE_PROMPTS["delay_prediction"]
    )
    try:
        return prompt_template.format(**kwargs)
    except KeyError:
        return ROOT_CAUSE_PROMPTS["delay_prediction"]


def get_available_prompts():
    return list(ROOT_CAUSE_PROMPTS.keys())


def add_custom_prompt(name: str, template: str):
    ROOT_CAUSE_PROMPTS[name] = template


if __name__ == "__main__":
    print("Available prompts:", get_available_prompts())
