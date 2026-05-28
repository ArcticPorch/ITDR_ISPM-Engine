import json

def get_mock_cloud_data():
    """
    ARCHITECTURE NOTE: This function provides an abstracted mock data contract 
    simulating live infrastructure state profiles. In production deployment, 
    this interface is decoupled to pull live telemetry via the AWS SDK (Boto3).
    """
    return [
        {
            "username": "ananya_marketing_intern",
            "account_type": "Human User",
            "granted_permissions": ["AdministratorAccess", "S3_FullAccess", "RDS_DatabaseDelete"],
            "last_90_days_activity": [
                {"action": "S3_Read", "resource": "marketing_assets/summer_camp.png"},
                {"action": "S3_Read", "resource": "marketing_assets/logo.png"}
            ],
            "status": "Active"
        },
        {
            "username": "legacy_payment_token_service",
            "account_type": "Service Account (Non-Human)",
            "granted_permissions": ["PaymentGateway_Write", "UserDatabase_Delete", "Cloud_Infrastructure_Admin"],
            "last_90_days_activity": [], 
            "status": "Dormant (Created 2 years ago)"
        },
        {
            "username": "rahul_senior_dev",
            "account_type": "Human User",
            "granted_permissions": ["S3_Read", "S3_Write", "EC2_DeployInstance"],
            "last_90_days_activity": [
                {"action": "S3_Read", "resource": "code_repository/main.zip"},
                {"action": "EC2_DeployInstance", "resource": "production_server_01"}
            ],
            "status": "Active"
        }
    ]

if __name__ == "__main__":
    print(json.dumps(get_mock_cloud_data(), indent=2))