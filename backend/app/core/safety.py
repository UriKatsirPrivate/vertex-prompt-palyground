"""Vertex AI safety-filter settings.

Ported verbatim from the Streamlit app's ``initialization.py`` — same harm
categories and thresholds (HATE / SEXUAL / HARASSMENT = BLOCK_ONLY_HIGH,
DANGEROUS = OFF).
https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
"""
from google.genai.types import SafetySetting

safety_settings = [
    SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"),
    SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
    SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"),
    SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"),
]
