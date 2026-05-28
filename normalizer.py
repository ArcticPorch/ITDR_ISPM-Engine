import json

def normalize_cloudtrail_firehose(raw_cloudtrail_logs, static_iam_privileges):
    """
    PRODUCTION PIPELINE DESIGN: Extracts core identity signals and strips out 
    uncompressed metadata noise to prevent LLM context window inflation.
    """
    normalized_profiles = {}
    
    # 1. Initializing mapping using static configuration permissions
    for user_policy in static_iam_privileges:
        username = user_policy.get("username")
        normalized_profiles[username] = {
            "username": username,
            "account_type": user_policy.get("account_type", "AWS IAM Principal"),
            "granted_permissions": user_policy.get("granted_permissions", []),
            "last_90_days_activity": [],
            "status": user_policy.get("status", "Active")
        }
        
    # 2. Iterate through complex, uncompressed logging footprints
    for log_event in raw_cloudtrail_logs:
        user_identity = log_event.get("userIdentity", {})
        principal_arn = user_identity.get("arn", "")
        
        # Extract the logical username from the infrastructure ARN
        resolved_username = None
        if "/" in principal_arn:
            resolved_username = principal_arn.split("/")[-1]
        elif "userName" in user_identity:
            resolved_username = user_identity.get("userName")
            
        if resolved_username in normalized_profiles:
            action = log_event.get("eventName")
            
            # Extract target resource identifier safely across various schemas
            req_params = log_event.get("requestParameters", {})
            resource_target = "Unknown_Resource"
            if req_params:
                # Look for common AWS API target configuration key flags
                for key_flag in ["bucketName", "key", "resourceName", "dbInstanceIdentifier"]:
                    if key_flag in req_params:
                        resource_target = req_params[key_flag]
                        break
            
            normalized_profiles[resolved_username]["last_90_days_activity"].append({
                "action": action,
                "resource": resource_target
            })
            
    return list(normalized_profiles.values())