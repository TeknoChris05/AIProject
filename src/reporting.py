import json
from datetime import datetime


def generate_report(results, output_path: str):
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "total_incidents": len(results),
        "incidents": []
    }

    for item in results:
        incident = item.get("incident")
        rule_analysis = item.get("rule_analysis")
        model_analysis = item.get("model_analysis")

        incident_report = {
            "incident_data": incident,
            "rule_analysis": rule_analysis,
            "model_analysis": model_analysis,
            "risk_level": determine_risk(rule_analysis, model_analysis),
            "recommendations": generate_recommendations(rule_analysis, model_analysis)
        }

        report["incidents"].append(incident_report)

    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"Report saved to {output_path}")


def determine_risk(rule_analysis, model_analysis):

    if rule_analysis and rule_analysis.get("alert"):
        return "HIGH"

    if model_analysis and model_analysis.get("suspicious"):
        return "MEDIUM"

    return "LOW"


def generate_recommendations(rule_analysis, model_analysis):

    recommendations = []

    if rule_analysis and rule_analysis.get("alert"):
        recommendations.append(
            "Investigate the triggered security rule and review related logs."
        )

    if model_analysis and model_analysis.get("suspicious"):
        recommendations.append(
            "Run deeper behavioral analysis on this incident."
        )

    if not recommendations:
        recommendations.append(
            "No immediate action required. Continue monitoring."
        )

    return recommendations
