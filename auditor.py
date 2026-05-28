import os
from google import genai
from google.genai import types
from models import ComprehensiveAuditReport

def deterministic_pre_filter(raw_data):

    flagged_for_review = []
    
    for account in raw_data:
        if len(account.get("last_90_days_activity", [])) == 0:
            account["deterministic_flag"] = "CRITICAL_DORMANT_ACCOUNT"
            flagged_for_review.append(account)
            continue
            
        if "AWS_AdministratorAccess" in account.get("granted_permissions", []) or "Azure_GlobalAdmin" in account.get("granted_permissions", []):
            account["deterministic_flag"] = "HIGH_PRIVILEGE_MONITORING"
            flagged_for_review.append(account)
            
    return flagged_for_review

def run_identity_audit(target_data) -> ComprehensiveAuditReport:
    client = genai.Client()
    
    system_prompt = """
    You are an elite automated Identity Threat Detection and Response (ITDR) engine.
    Analyze the provided corporate cloud access logs. Compare what permissions each account holds against what they actually utilized over the last 90 days.
    
    Look specifically for:
    - Privilege Drift: Accounts possessing extensive permissions they never use.
    - Dormant Risks: Non-human service accounts holding admin control with no recent activity logs.
    
    Provide the analysis and include the exact terminal execution script (AWS CLI format) to remediate the vulnerability.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Execute comprehensive identity audit for this footprint:\n{str(target_data)}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ComprehensiveAuditReport,
        ),
    )
    
    return ComprehensiveAuditReport.model_validate_json(response.text)