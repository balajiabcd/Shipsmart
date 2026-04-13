# Milestone #241: Build Notification System

**Your Role:** AI/LLM Engineer

Prepare alert notifications:

```python
# src/anomaly/notifications.py

from typing import List, Dict
import smtplib
from email.mime.text import MIMEText

class AlertNotificationSystem:
    def __init__(self):
        self.channels = ["email", "sms", "webhook", "slack"]
        self.recipients = {
            "critical": ["ops-manager@shipsmart.com", "cto@shipsmart.com"],
            "high": ["ops-team@shipsmart.com"],
            "medium": ["dashboard@shipsmart.com"],
            "low": []
        }
    
    def send_notifications(self, alerts: List[Dict]):
        for alert in alerts:
            severity = alert.get("severity", "low")
            recipients = self.recipients.get(severity, [])
            
            for recipient in recipients:
                self._send_alert(recipient, alert)
    
    def _send_alert(self, recipient: str, alert: Dict):
        if "@shipsmart.com" in recipient:
            self._send_email(recipient, alert)
        elif recipient.startswith("http"):
            self._send_webhook(recipient, alert)
    
    def _send_email(self, recipient: str, alert: Dict):
        msg = MIMEText(f"""
Alert: {alert['title']}
Severity: {alert['severity']}
Message: {alert['message']}
Time: {alert['timestamp']}
        """)
        msg['Subject'] = f"[{alert['severity'].upper()}] {alert['title']}"
        msg['From'] = "alerts@shipsmart.com"
        msg['To'] = recipient
        
        # In production, use actual SMTP
        # with smtplib.SMTP('smtp.example.com') as server:
        #     server.send_message(msg)
    
    def _send_webhook(self, url: str, alert: Dict):
        import requests
        try:
            requests.post(url, json=alert, timeout=5)
        except:
            pass

def create_notification_payload(alert: Dict) -> Dict:
    return {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚨 {alert['title']}"}
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": alert['message']}
            }
        ]
    }
```

Commit.