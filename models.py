from pydantic import BaseModel, Field
from typing import List

class SecurityFinding(BaseModel):
    username: str = Field(description="The username of the account analyzed.")
    risk_level: str = Field(description="Must be one of: CRITICAL, HIGH, MEDIUM, LOW.")
    findings: List[str] = Field(description="List of specific security issues found (e.g., 'Dormant Admin Account', 'Privilege Drift').")
    drift_explanation: str = Field(description="Clear explanation comparing granted rights vs actual usage.")
    remediated_policy: str = Field(description="A clean, minimized mock JSON block outlining only the permissions this user actually requires.")
    remediation_cli_command: str = Field(description="The exact terminal/CLI command needed to fix the user's overprivilaged permissions (e.g., AWS IAM commands).")

class ComprehensiveAuditReport(BaseModel):
    total_accounts_analyzed: int
    critical_alerts_count: int
    individual_findings: List[SecurityFinding]