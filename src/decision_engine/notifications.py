import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_delay_notification(delivery_id: str, prediction_context: Dict) -> Dict:
    """Generate proactive notification message"""

    delay_prob = prediction_context.get("delay_probability", 0)
    main_factors = prediction_context.get("top_factors", [])

    if delay_prob > 0.8:
        urgency = "high"
        template = (
            "We're experiencing significant delays due to {reason}. New ETA: {new_eta}"
        )
    elif delay_prob > 0.5:
        urgency = "medium"
        template = (
            "Your delivery may be delayed by {delay_minutes} mins. Reason: {reason}"
        )
    else:
        urgency = "low"
        template = "Your delivery is on track. Expected: {eta}"

    reason = main_factors[0] if main_factors else "weather conditions"

    message = template.format(
        reason=reason,
        delay_minutes=int(prediction_context.get("expected_delay_mins", 15)),
        new_eta=prediction_context.get("new_eta", "2-3 hours"),
        eta=prediction_context.get("eta", "on time"),
    )

    return {
        "delivery_id": delivery_id,
        "message": message,
        "urgency": urgency,
        "channels": ["sms", "email", "app_push"],
        "template_id": f"delay_{urgency}_template",
    }


def send_sms(message: str) -> bool:
    """Send SMS notification"""
    logger.info(f"Sending SMS: {message[:50]}...")
    return True


def send_email(message: str) -> bool:
    """Send email notification"""
    logger.info(f"Sending Email: {message[:50]}...")
    return True


def send_push_notification(message: str) -> bool:
    """Send push notification"""
    logger.info(f"Sending Push: {message[:50]}...")
    return True


def log_notification(notification: Dict):
    """Log notification for audit"""
    logger.info(
        f"Notification logged: {notification['delivery_id']} - {notification['urgency']}"
    )


def send_notification(notification: Dict) -> bool:
    """Send notification via multiple channels"""

    for channel in notification.get("channels", []):
        if channel == "sms":
            send_sms(notification["message"])
        elif channel == "email":
            send_email(notification["message"])
        elif channel == "app_push":
            send_push_notification(notification["message"])

    log_notification(notification)
    return True


def generate_reroute_notification(delivery_id: str, alternative_route: Dict) -> Dict:
    """Generate reroute suggestion notification"""

    return {
        "delivery_id": delivery_id,
        "message": f"We suggest an alternative route. Save {alternative_route.get('time_saved_min', 0)} mins!",
        "urgency": "medium",
        "channels": ["app_push", "email"],
        "template_id": "reroute_suggestion",
    }


def generate_driver_change_notification(delivery_id: str, new_driver: Dict) -> Dict:
    """Generate driver change notification"""

    return {
        "delivery_id": delivery_id,
        "message": f"Your delivery will be handled by {new_driver.get('name', 'a new driver')} for better service.",
        "urgency": "low",
        "channels": ["app_push"],
        "template_id": "driver_change",
    }


def generate_slot_change_notification(delivery_id: str, new_slot: Dict) -> Dict:
    """Generate slot change notification"""

    return {
        "delivery_id": delivery_id,
        "message": f"Your delivery has been rescheduled to {new_slot.get('start_time')}-{new_slot.get('end_time')}.",
        "urgency": "medium",
        "channels": ["sms", "email", "app_push"],
        "template_id": "slot_change",
    }


def should_send_notification(
    prediction_context: Dict, customer_tier: str = "standard"
) -> bool:
    """Determine if notification should be sent"""

    delay_prob = prediction_context.get("delay_probability", 0)

    if customer_tier == "premium":
        return delay_prob > 0.3
    elif customer_tier == "standard":
        return delay_prob > 0.5
    else:
        return delay_prob > 0.7


def get_notification_preferences(customer_id: str) -> Dict:
    """Get customer notification preferences (placeholder)"""

    return {
        "customer_id": customer_id,
        "sms_enabled": True,
        "email_enabled": True,
        "push_enabled": True,
        "preferred_language": "en",
        "quiet_hours_start": 22,
        "quiet_hours_end": 7,
    }


def schedule_notification(notification: Dict, send_at: datetime) -> Dict:
    """Schedule notification for later"""

    return {
        **notification,
        "scheduled": True,
        "send_at": send_at.isoformat(),
        "status": "pending",
    }
