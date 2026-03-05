import os
from google import genai

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/darshangada/Desktop/backtrader/vertex_key.json"

client = genai.Client(
    vertexai=True,
    project="project-avs-dev",
    location="us-central1"
)

news = "D Pinaults Sell Puma Stake to China’s Anta for $1.8 Billion (1) BN 13:48"

prompt = f"""
You are a financial sentiment analysis model.

Return ONLY JSON.

Format:
{{
"sentiment": -1 | 0 | 1,
"confidence": 0-1
}}

News:
{news}
"""

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

print(response.text)