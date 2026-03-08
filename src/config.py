class Settings:
    FAILED_LOGIN_THRESHOLD = 5
    SUSPICIOUS_IPS = [
        "192.168.1.100",
        "10.0.0.66"
    ]

    MODEL_RISK_THRESHOLD = 0.7

    DEFAULT_INPUT_FILE = "data/incidents.json"
    DEFAULT_OUTPUT_FILE = "output/report.json"


settings = Settings()
