import streamlit as st
from src.pipeline import run_pipeline
from src.reporting import to_markdown
from src.config import PipelineConfig

st.set_page_config(page_title="IncidentLens", layout="wide")

st.title("IncidentLens — Linux Incident Assistant (MVP)")

st.markdown(
    """
Upload a Linux auth log (or point to a local file) and generate an incident triage report.
This demo focuses on Linux SSH/sudo/account activity.
"""
)

with st.sidebar:
    st.header("Config")
    brute_threshold = st.number_input("Brute-force fail threshold", min_value=3, max_value=100, value=8)
    window_minutes = st.number_input("Brute-force window (minutes)", min_value=1, max_value=120, value=10)
    timeline_limit = st.number_input("Timeline items", min_value=20, max_value=500, value=200)
    st.divider()
    st.caption("Tip: For a live demo, use a sample auth.log file with SSH failures + sudo usage.")

cfg = PipelineConfig(
    brute_force_fail_threshold=int(brute_threshold),
    brute_force_window_minutes=int(window_minutes),
    timeline_limit=int(timeline_limit),
)

tab1, tab2 = st.tabs(["Upload file", "Use local path"])

path = None

with tab1:
    up = st.file_uploader("Upload auth log", type=["log", "txt"])
    if up:
        content = up.getvalue().decode("utf-8", errors="replace")
        tmp_path = "/tmp/incidentlens_auth.log"
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content)
        path = tmp_path

with tab2:
    path_in = st.text_input("Local path (e.g., /var/log/auth.log or data/samples/auth_sample.log)")
    if path_in:
        path = path_in

if st.button("Generate Report", type="primary", disabled=not bool(path)):
    try:
        report = run_pipeline(path, cfg=cfg)
        md = to_markdown(report)
        st.success("Report generated.")
        st.download_button("Download report.md", data=md, file_name="incident_report.md")
        st.markdown(md)
    except Exception as e:
        st.error(f"Failed: {e}")