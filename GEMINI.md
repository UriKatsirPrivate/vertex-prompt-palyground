# Project Instructions: Vertex Prompt Playground

## Tech Stack
- **Language:** Python 3.x
- **Framework:** Streamlit (Frontend/Orchestration)
- **AI/ML:** Google Vertex AI (Gemini, Imagen, Veo)
- **Utilities:** `google-genai`, `gptrim`, `python-toon`

## Architecture
The project follows a modular, hierarchical architecture:
- **UI & Coordination (`app.py`):** Multi-tool dashboard using Streamlit. Routes requests to utility functions based on user selection.
- **Service Layer (`utils.py`):** Functional backbone. Manages GenAI client initialization, content generation, and prompt compression.
- **Prompt Library (`*_prompt.py`):** Specialized modules containing complex prompt templates (e.g., D.A.R.E, Meta-Prompting).
- **Initialization (`initialization.py`):** Centralizes model safety settings and basic client setup.

## Coding Standards
- **Prompt Management:** Keep complex prompt templates in dedicated `*_prompt.py` files.
- **Performance:** Use Streamlit's `@st.cache_data` for LLM responses and `@st.cache_resource` for the GenAI client.
- **Modularity:** New prompt engineering techniques should be added as a new `*_prompt.py` file and integrated via `utils.py`.

## Key Workflows
1. **Setup:** 
   - Install dependencies: `pip install -r requirements.txt`
   - Configure secrets: Create `.streamlit/secrets.toml` with `GCP_PROJECT_ID`.
2. **Development:** Run the app locally using `streamlit run app.py`.
3. **Deploy:** Use `./deploy.sh` to deploy to Google Cloud Run.

## Directory Structure
- `app.py`: Entry point and UI.
- `utils.py`: Core logic and GenAI integration.
- `*_prompt.py`: Prompt template library.
- `icons/`: Static assets (logos).
