from .config import settings
from .io_utils import load_incident_data
from .rules import apply_detection_rules
from .models import analyze_with_model
from .reporting import generate_report


class IncidentPipeline:
    def __init__(self):
        self.config = settings

    def run(self, input_path: str, output_path: str):
        print("Starting Incident Analysis Pipeline")

        incidents = load_incident_data(input_path)
        print(f"Loaded {len(incidents)} records")

        rule_results = apply_detection_rules(incidents)
        print("Rule-based analysis complete")

        model_results = analyze_with_model(incidents)
        print("Model analysis complete")

        combined_results = []
        for i, incident in enumerate(incidents):
            combined_results.append({
                "incident": incident,
                "rule_analysis": rule_results[i] if i < len(rule_results) else None,
                "model_analysis": model_results[i] if i < len(model_results) else None
            })

        generate_report(combined_results, output_path)

        print("Pipeline complete")
        return combined_results


def run_pipeline(input_path: str, output_path: str):
    pipeline = IncidentPipeline()
    return pipeline.run(input_path, output_path)
