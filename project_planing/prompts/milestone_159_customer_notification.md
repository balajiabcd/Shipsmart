# Milestone #159: Build Customer Notification

**Your Role:** AI/LLM Engineer

Generate proactive customer messages:

```python
# decision_engine/notifications.py

def generate_delay_notification(delivery_id: str, prediction_context: dict) -> dict:
    """Generate proactive notification message"""
    
    delay_prob = prediction_context["delay_probability"]
    main_factors = prediction_context.get("top_factors", [])
    
    if delay_prob > 0.8:
        urgency = "high"
        template = "We're experiencing significant delays due to {reason}. New ETA: {new_eta}"
    elif delay_prob > 0.5:
        urgency = "medium"
        template = "Your delivery may be delayed by {delay_minutes} mins. Reason: {reason}"
    else:
        urgency = "low"
        template = "Your delivery is on track. Expected: {eta}"
    
    reason = main_factors[0] if main_factors else "weather conditions"
    
    return {
        "delivery_id": delivery_id,
        "message": template.format(
            reason=reason,
            delay_minutes=int(prediction_context.get("expected_delay_mins", 15)),
            new_eta=prediction_context.get("new_eta", "2-3 hours"),
            eta=prediction_context.get("eta", "on time")
        ),
        "urgency": urgency,
        "channels": ["sms", "email", "app_push"],
        "template_id": f"delay_{urgency}_template"
    }

def send_notification(notification: dict) -> bool:
    """Send notification via multiple channels"""
    
    for channel in notification["channels"]:
        if channel == "sms":
            send_sms(notification["message"])
        elif channel == "email":
            send_email(notification["message"])
        elif channel == "app_push":
            send_push_notification(notification["message"])
    
    log_notification(notification)
    return True
```

Commit.