import os

from google.genai import types
from google import genai
from google.genai.types import (
    CreateCachedContentConfig,
    EmbedContentConfig,
    FunctionDeclaration,
    GenerateContentConfig,
    Part,
    SafetySetting,
    Tool,
    # GenerationConfig,
)

# https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/configure-safety-filters
safety_settings = [
    SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="BLOCK_ONLY_HIGH",
    ),
    SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="OFF",
    ),
    SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="BLOCK_ONLY_HIGH",
    ),
    SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

# Initialize LLM
def initialize_llm_vertex(project_id,region,model_name,max_output_tokens,temperature,top_p):
    
    client = genai.Client(vertexai=True, project=project_id, location=region)

    generation_config = GenerateContentConfig(temperature=temperature,
                                     top_p=top_p,
                                     max_output_tokens=max_output_tokens,)
    return client, safety_settings,generation_config

# def get_from_secrets_manager(secret_name,gcp_project):
#     # if langsmith_key:
#     #     return langsmith_key

#     # print("token")
#     client = secretmanager.SecretManagerServiceClient()

#     # name = f"projects/{PROJECT_ID}/secrets/langchain-api-key/versions/1"
#     name = f"projects/{gcp_project}/secrets/{secret_name}/versions/1"

#     # Access the secret version.
#     response = client.access_secret_version(request={"name": name})

#     # Extract the payload.
#     payload = response.payload.data.decode("UTF-8")

#     return payload