import streamlit as st
from streamlit.errors import StreamlitAPIException
from initialization import safety_settings
from gptrim import trim
from system_prompts import (
    SYSTEM_PROMPT,
    JSON_PROMPT,
    NANO_BANANA_PROMPT,
)
from placeholders import GENERATE_IMAGES
from meta_prompt import metaprompt
from google.genai import types
from image_prompts import GenerateImageSystemPrompt
from fine_tune_prompt import (
    refine_prompt,
    prompt_improver,
    make_prompt,
    make_prompt_v2,
)
from agent_prompt import agent_prompt
from google.genai.types import (GenerateContentConfig,)
from dare_prompts import dare_prompt, dare_artifacts_generator
from video_prompt import video_prompt
from google import genai

REGIONS=["global"]
MODEL_NAMES=['gemini-2.5-flash','gemini-2.5-pro']

def get_project_id():
    # Use st.secrets for better security
    try:
        # Try to access secrets, falling back to default if key is missing
        return st.secrets.get("GCP_PROJECT_ID", "landing-zone-demo-341118")
    except StreamlitAPIException:
        # If secrets file doesn't exist at all, return the default
        return "landing-zone-demo-341118"

@st.cache_resource
def get_llm_client(project_id, region):
    """Initializes and caches the LLM client."""
    # Correctly initialize the client for Vertex AI.
    # This client object will be cached.
    return genai.Client(vertexai=True, project=project_id, location=region)

@st.cache_data
def generate_llm_content(_client, project_id, region, model_name, contents, _generation_config, system_instruction=None):
    """Generic function to generate content from the LLM with error handling."""
    full_contents = []
    if system_instruction:
        full_contents.append(types.Part(text=system_instruction))
    full_contents.append(types.Part(text=contents))

    try:
        response = _client.models.generate_content(
            contents=full_contents,
            model=f"projects/{project_id}/locations/{region}/publishers/google/models/{model_name}",
            config=_generation_config,
        )
        return response.text
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def display_result(execution_result, key_suffix):
    """Displays the execution result in a text area."""
    if execution_result:
        st.text_area(label="Execution Result:", value=execution_result, height=400, key=f"result_{key_suffix}")
    else:
        st.warning('No result to display.')

@st.cache_data
def create_refine_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = refine_prompt.format(task="improve the prompt", lazy_prompt=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def create_improved_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = prompt_improver.format(text=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def create_make_prompt(_client, project_id, region, model_name, _generation_config, prompt_version, user_input):
    prompt_template = make_prompt if prompt_version == 1 else make_prompt_v2
    prompt = prompt_template.format(task="improve the prompt", lazy_prompt=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def create_system_prompt(_client, project_id, region, model_name, _generation_config, user_input=""):
    prompt = SYSTEM_PROMPT.format(user_input=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def create_agent_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = agent_prompt.format(prompt=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def create_meta_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    return generate_llm_content(_client, project_id, region, model_name, user_input, _generation_config)

@st.cache_data
def json_prompter(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = JSON_PROMPT.format(user_input=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def banana_json_prompter(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = NANO_BANANA_PROMPT.format(user_input=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def run_prompt(_client, project_id, region, model_name, _generation_config, prompt):
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def zero_to_few_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    system_prompt = "You are an assistant designed to convert a zero-shot prompt into a few-shot prompt."
    prompt = f"The zero-shot prompt is: '{user_input}'. Please convert it into a few-shot prompt. Be as elaborate as possible. Make sure to include at least 3 examples."
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config, system_instruction=system_prompt)

@st.cache_data
def chain_of_thought_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    system_prompt = "You are an assistant designed to convert a prompt into a chain of thought prompt."
    prompt = f"The prompt is: '{user_input}'. Please convert it into a chain of thought prompt. Always append 'Let's think step by step.' to the prompt."
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config, system_instruction=system_prompt)

@st.cache_data
def create_video_prompt(_client, project_id, region, model_name, _generation_config, user_input):
    prompt = video_prompt.format(user_idea=user_input)
    return generate_llm_content(_client, project_id, region, model_name, prompt, _generation_config)

@st.cache_data
def dare_it(_client, project_id, region, model_name, _generation_config, query, vision, mission, context):
    template_prompt= dare_prompt
    formatted_prompt = template_prompt.format(vision=vision,mission=mission,context=context,prompt=query)
    return generate_llm_content(_client, project_id, region, model_name, formatted_prompt, _generation_config)

@st.cache_data
def create_dare_artifacts(_client, project_id, region, model_name, temperature, top_p, max_tokens, _safety_settings, user_input):
    system_prompt ="""
                    You are a GenAI expert capable of generating solid prompts.
                    Context: D.A.R.E prompting works by asking the chatbot to remember its mission and vision before answering a question.
                    This helps to keep the chatbot grounded in reality and prevents it from generating responses that are irrelevant or nonsensical.
                    D.A.R.E uses vision and mission statements to check if the response complies with them
    """
    template_prompt= dare_artifacts_generator
    formatted_prompt = template_prompt.format(user_input=user_input)
    config = GenerateContentConfig(temperature=temperature, top_p=top_p, max_output_tokens=max_tokens, safety_settings=_safety_settings)
    return generate_llm_content(_client, project_id, region, model_name, formatted_prompt, config, system_instruction=system_prompt)

@st.cache_data
def run_trim(prompt_to_trim):
    return trim(prompt_to_trim)

@st.cache_data
def GenerateImagePrompt(_client, project_id, region, model_name, temperature, top_p, max_tokens, _safety_settings, user_input):
    system_prompt = GenerateImageSystemPrompt

    prompt= """Please generate 2 prompt(s) about: {description}"""
    formatted_prompt = prompt.format(description=user_input)
    config = GenerateContentConfig(temperature=temperature, top_p=top_p, max_output_tokens=max_tokens, safety_settings=_safety_settings)
    return generate_llm_content(_client, project_id, region, model_name, formatted_prompt, config, system_instruction=system_prompt)

@st.cache_data
def GenerateImageNew(_client, description, num_of_images):
    try:
        images = _client.models.generate_images(
            prompt=description,
            model="imagen-3.0-generate-002", # Using a specific model for image generation
            config=types.GenerateImagesConfig(
                number_of_images=num_of_images,
                output_mime_type='image/jpeg',
                safety_filter_level="BLOCK_ONLY_HIGH",
                person_generation="allow_adult",
                aspect_ratio="9:16",  # "1:1" "16:9" "4:3" "3:4"
                ),
            )
        return images
    except Exception as e:
        st.error(f"An error occurred during image generation: {e}")
        return None

def display_images_new(images):
    if images and images.generated_images:
        # Using st.columns to display images side-by-side
        cols = st.columns(len(images.generated_images))
        for i, image in enumerate(images.generated_images):
            with cols[i]:
                st.image(image.image._pil_image, use_container_width=True)
    else:
        st.warning("No images were generated. This could be due to a safety policy violation or an API error.")