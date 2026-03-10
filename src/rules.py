from .config import settings


def apply_detection_rules(incidents):
    results = []

    for incident in incidents:
        alert = False
        reasons = []

        source_ip = incident.get("source_ip")
        event_type = incident.get("event_type")

        if source_ip in settings.SUSPICIOUS_IPS:
            alert = True
            reasons.append("Source IP flagged as suspicious")

        if event_type == "login_failure":
            alert = True
            reasons.append("Failed login attempt detected")

        results.append({
            "alert": alert,
            "reasons": reasons
        })

    return results
