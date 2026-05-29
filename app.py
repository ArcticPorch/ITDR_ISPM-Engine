import streamlit as st
import json
from data_generator import get_mock_cloud_data
from normalizer import normalize_cloudtrail_firehose
from auditor import run_identity_audit

st.set_page_config(page_title="Ambient Identity Auditor Engine", layout="wide", page_icon="🛡️")
st.title("Ambient Identity Auditor Engine")
st.caption("Advanced AI-Driven Identity Security Posture Management (ISPM) with Integrated Data Normalization Pipelines")
st.markdown("---")

st.sidebar.header("Data Ingestion Interface")

# Configuration Input: Upload raw infrastructure trail file
uploaded_raw_logs = st.sidebar.file_uploader("Ingest Raw AWS CloudTrail Firehose (JSON)", type=["json"])

# Static configuration base data
static_iam_privileges = get_mock_cloud_data()

if st.sidebar.button("Execute Normalization & Full Identity Audit", type="primary"):
    st.session_state.audit_triggered = True

if 'audit_triggered' not in st.session_state:
    st.session_state.audit_triggered = False

tab1, tab2 = st.tabs(["Audited Security Posture Insights", "Ingested Pipeline Telemetry"])

# Simulation or normalized transformation pipeline parsing execution
if uploaded_raw_logs is not None:
    raw_ingested_json = json.load(uploaded_raw_logs)
    active_dataset = normalize_cloudtrail_firehose(raw_ingested_json, static_iam_privileges)
else:
    active_dataset = static_iam_privileges

with tab2:
    st.subheader("Normalized Pipeline Ingestion Stream")
    st.markdown("This feed represents raw cloud monitoring output compiled and compressed via local preprocessing code execution blocks.")
    st.json(active_dataset)

with tab1:
    if not st.session_state.audit_triggered:
        st.info("Systems Online. Ingest infrastructure logs and click execution trigger in controls sidebar.")
    else:
        with st.spinner("Querying Gemini Orchestration Engine with normalized footprints..."):
            try:
                report = run_identity_audit(active_dataset)
                
                col1, col2, col3 = st.columns(3)
                col1.metric(label="Accounts Scanned", value=report.total_accounts_analyzed)
                col2.metric(label="Critical Gaps Detected", value=report.critical_alerts_count, delta="- Actions Generated", delta_color="inverse")
                col3.metric(label="Log Optimization Status", value="Normalized")
                
                st.markdown("### Detected Identity Debt Profiles")
                for finding in report.individual_findings:
                    with st.expander(f"Account: {finding.username} | Risk Status: {finding.risk_level}"):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Identified Gaps:**")
                            for issue in finding.findings:
                                st.markdown(f"- `{issue}`")
                            st.markdown(f"**Drift Analysis:** {finding.drift_explanation}")
                            st.markdown("**Automated CLI Fix Command:**")
                            st.code(finding.remediation_cli_command, language="bash")
                        with c2:
                            st.markdown("**AI-Remediated Least-Privilege Target Configuration Policy:**")
                            st.code(finding.remediated_policy, language="json")
                st.success("Automated infrastructure configuration remediation scan complete.")
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")