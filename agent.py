import requests
import pandas as pd
from scipy.stats import skew
from smolagents import CodeAgent, LiteLLMModel, tool

from proximity_check import proximity_check

# ======== Real Compilot API Tool ========
@tool
def call_compilot(public_key: str) -> str:
    """
    Checks if the given public key is safe using Compilot API.

    Args:
        public_key (str): The public key to check.

    Returns:
        str: A message indicating if the key is safe or unsafe.
    """
    url = "https://api.compilot.ai"
    headers = {
        "Authorization": "Bearer bcd8e355-6eec-47bb-b714-15b4b5f6b539",
        "Content-Type": "application/json"
    }
    payload = {
        "public_key": public_key
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        status = data.get("status", "unknown")
        return f"Compilot check for {public_key}: {status}"
    except requests.exceptions.RequestException as e:
        return f"Error contacting Compilot: {e}"

# ========== Model and Agent Setup ==========
model = LiteLLMModel(
    model_id="gemini/gemini-2.0-flash",
    api_key="AIzaSyA4dPMvJsfG68at1iepaiAx7MmAdjjvw3M"
)

agent = CodeAgent(
    tools=[call_compilot, proximity_check],
    model=model
)

# ========== Run the Agent ==========
public_key = "0xx000"  # Replace with real key to test

task = f"""
Step 1: Use the public key: {public_key}.
Step 2: Call Compilot API to check if it is safe or unsafe.
Step 3: Return the result to the user.
"""

result = agent.run(task)
print(result)
