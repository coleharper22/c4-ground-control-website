#!/usr/bin/env python3
"""
C4 Ground Control Lead Capture API
Receives form submissions from website → creates HCP customers automatically
"""

import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime

# HCP API Configuration
HCP_API_KEY = "10d6d33f386e4d0d9eba59e89313c53d"
HCP_API_BASE = "https://api.housecallpro.com"

def create_hcp_customer(form_data):
    """Create customer in HousecallPro"""
    
    # Prepare customer data
    customer_payload = {
        "first_name": form_data.get("firstName", ""),
        "last_name": form_data.get("lastName", ""),
        "email": form_data.get("email", ""),
        "mobile_number": form_data.get("phone", ""),
        "company": form_data.get("company", ""),
        "address": {
            "street": form_data.get("address", ""),
            "city": "",
            "state": "FL",
            "zip": "",
            "country": "US"
        },
        "lead_source": "Website - c4groundcontrol.com"
    }
    
    # Create customer
    headers = {
        "Authorization": f"Bearer {HCP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        f"{HCP_API_BASE}/customers",
        data=json.dumps(customer_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            customer_data = json.loads(response.read().decode('utf-8'))
            customer_id = customer_data.get("customer", {}).get("id")
            
            # Create estimate with project details
            if customer_id:
                create_estimate(customer_id, form_data)
            
            return {
                "success": True,
                "customer_id": customer_id,
                "customer_data": customer_data
            }
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return {
            "success": False,
            "error": f"HCP API error: {e.code} - {error_body}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def create_estimate(customer_id, form_data):
    """Create estimate in HCP with project details"""
    
    property_type = form_data.get("propertyType", "")
    services = form_data.get("services", "")
    message = form_data.get("message", "")
    
    # Build estimate description
    description = f"""
Lead from Website - {datetime.now().strftime('%Y-%m-%d %H:%M')}

Property Type: {property_type}
Services Requested: {services}

Customer Notes:
{message}

FOLLOW UP REQUIRED - Schedule site visit for quote
    """.strip()
    
    estimate_payload = {
        "customer_id": customer_id,
        "options": [
            {
                "name": f"{services} - Initial Consultation",
                "line_items": [
                    {
                        "name": "Site Visit & Consultation",
                        "description": description,
                        "quantity": 1,
                        "unit_price": 0,  # Free consultation
                        "unit_cost": 0
                    }
                ]
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {HCP_API_KEY}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        f"{HCP_API_BASE}/estimates",
        data=json.dumps(estimate_payload).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            estimate_data = json.loads(response.read().decode('utf-8'))
            return estimate_data
    except Exception as e:
        print(f"Warning: Could not create estimate - {e}", file=sys.stderr)
        return None

def save_lead_backup(form_data, hcp_result):
    """Save lead to local backup file"""
    import os
    
    backup_dir = os.path.expanduser("~/Documents/C4-AI-Bot/Website-Leads")
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{backup_dir}/{timestamp}-{form_data.get('lastName', 'Unknown')}.json"
    
    lead_record = {
        "timestamp": datetime.now().isoformat(),
        "form_data": form_data,
        "hcp_result": hcp_result
    }
    
    with open(filename, 'w') as f:
        json.dump(lead_record, f, indent=2)
    
    return filename

def main():
    """Main API endpoint handler"""
    
    # Read form data from stdin (sent by web server)
    try:
        form_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "Invalid JSON input"
        }))
        return 1
    
    # Validate required fields
    required_fields = ["firstName", "lastName", "phone", "address", "services"]
    missing_fields = [f for f in required_fields if not form_data.get(f)]
    
    if missing_fields:
        print(json.dumps({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }))
        return 1
    
    # Create HCP customer
    hcp_result = create_hcp_customer(form_data)
    
    # Save backup
    backup_file = save_lead_backup(form_data, hcp_result)
    
    # Return result
    result = {
        "success": hcp_result.get("success", False),
        "customer_id": hcp_result.get("customer_id"),
        "backup_file": backup_file,
        "message": "Lead captured successfully!" if hcp_result.get("success") else "Error capturing lead"
    }
    
    if not hcp_result.get("success"):
        result["error"] = hcp_result.get("error")
    
    print(json.dumps(result))
    return 0 if hcp_result.get("success") else 1

if __name__ == "__main__":
    sys.exit(main())
