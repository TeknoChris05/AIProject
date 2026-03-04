from src.pipeline import run_pipeline
from src.reporting import to_markdown

if __name__ == "__main__":
    # Change this to /var/log/auth.log if you want to analyze your VM’s real logs
    path = "src/data/samples/auth_sample.log"
    report = run_pipeline(auth_log_path=path)
    print(to_markdown(report))