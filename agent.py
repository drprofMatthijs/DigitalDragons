import requests

# Compilot credentials
COMPILOT_API_URL = "https://api.compilot.ai"
COMPILOT_API_KEY = "bcd8e355-6eec-47bb-b714-15b4b5f6b539"
COMPILOT_WORKFLOW_ID = "ee8a6cff-8800-4320-b780-58d12364fba8"

# Data to submit
individual = {
    "individualPersonalInformation": {
        "age": 23,
        "nationality": "SVNa",
        "residence": "aSVN"
    },
    "workspaceId": "682cd6bf3ba88bb1a4a819b6", 
    "organizationId": "682cd6bf3ba88bb1a4a8199e",
    "individualData": [
        {
            "externalId": "digitaldragon",
            "individualWallet": {
                "wallet": "0x165a526ef7576995E139B016e2c4654142c53fa1",
                "blockchainNamespace": "eip155",
                "verified": True
            }
        }
    ]
}

# URL
url = f"{COMPILOT_API_URL}/workflows/{COMPILOT_WORKFLOW_ID}/individuals"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {COMPILOT_API_KEY}"
}

# Make the request
response = requests.post(url, headers=headers, json=individual)

# Output the response
print("Status Code:", response.status_code)
try:
    print("Response JSON:", response.json())
except ValueError:
    print("Response Text:", response.text)
