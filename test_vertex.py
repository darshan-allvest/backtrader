import os
from google import genai
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vertex_key.json"

client = genai.Client(
    vertexai=True,
    project="project-avs-dev",
    location="us-central1"
)

news = "Pinaults Sell Puma Stake to China’s Anta for $1.8 Billion"

prompt = f"""
You are a financial sentiment analysis model.

Analyze the sentiment of the following financial news headline.

Rules:
1 = positive
0 = neutral
-1 = negative

Return ONLY valid JSON.

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

# CLEAN RESPONSE
clean_text = response.text.strip().replace("```json", "").replace("```", "")

data = json.loads(clean_text)

score = data["sentiment"] * data["confidence"]

print("Score:", score)