from src.pipeline import run_pipeline
from src.reporting import to_markdown

if __name__ == "__main__":
    path = "src/data/samples/auth_sample.log"

    report = run_pipeline(path)
    print(to_markdown(report))