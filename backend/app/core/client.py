"""Vertex AI GenAI client factory.

Replaces the Streamlit ``@st.cache_resource`` client with a process-lifetime
``lru_cache``. The genai client is thread-safe and effectively a singleton per
(project, region); caching it matches the Cloud Run instance lifetime and avoids
reconnecting per request.
"""
from functools import lru_cache

from google import genai


@lru_cache(maxsize=4)
def get_client(project_id: str, region: str) -> genai.Client:
    return genai.Client(vertexai=True, project=project_id, location=region)
