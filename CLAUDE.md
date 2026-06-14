# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

**The Prompt Playground** — a Streamlit web app exposing a suite of prompt-engineering
tools backed by Google Vertex AI (Gemini for text, Imagen for images). Deployed to
Google Cloud Run; live at https://myprompt.online/.

## Tech stack

- **Language:** Python 3.12 (Dockerfile pins `python:3.12`)
- **Framework:** Streamlit 1.57 (UI + orchestration)
- **AI/ML:** Google Vertex AI via the `google-genai` SDK (Gemini, Imagen)
- **Utilities:** `gptrim` (prompt compression), `python-toon` (TOON encoding)
- **Deploy:** Docker → Cloud Build → Cloud Run

## Architecture

Modular, single-page Streamlit app. Data flows: `app.py` (UI) → `utils.py` (service
layer) → `*_prompt.py` (prompt templates) → Vertex AI.

- **`app.py`** — entry point and the entire UI. A sidebar selectbox chooses a tool;
  a large `if/elif page == ...` block renders each tool's form and calls the matching
  `utils.py` function. Also builds the per-run `GenerateContentConfig` from the
  temperature/top-p/max-tokens sliders.
- **`utils.py`** — functional backbone. Holds `MODEL_NAMES`/`REGIONS`, client init,
  the generic `generate_llm_content(...)` wrapper, and one thin `@st.cache_data`
  function per tool that formats a template and calls the LLM.
- **`initialization.py`** — `safety_settings` (Vertex harm-category thresholds) and a
  legacy `initialize_llm_vertex(...)` helper.
- **`*_prompt.py` / `system_prompts.py` / `placeholders.py`** — prompt template library.
  Each technique's template lives in its own module (e.g. `dare_prompts.py`,
  `meta_prompt.py`, `agent_prompt.py`, `fine_tune_prompt.py`, `image_prompts.py`,
  `video_prompt.py`). `system_prompts.py` holds `SYSTEM_PROMPT`, `JSON_PROMPT`,
  `NANO_BANANA_PROMPT`; `placeholders.py` holds UI placeholder text.
- **`icons/`** — static assets (Vertex AI logo).

## Key conventions

- **Prompt templates stay in dedicated `*_prompt.py` modules** — never inline large
  templates in `app.py` or `utils.py`. They're `.format(...)`-ed in `utils.py`.
- **Caching:** `@st.cache_resource` for the GenAI client (`get_llm_client`),
  `@st.cache_data` for every LLM-calling function. Cached-function args prefixed with
  `_` (e.g. `_client`, `_generation_config`) are excluded from Streamlit's cache key —
  preserve that prefix when the arg is unhashable.
- **Model path format:** Vertex calls use the full resource path
  `projects/{project_id}/locations/{region}/publishers/google/models/{model_name}`.
- **Adding a new technique:** create a `*_prompt.py` template → add a cached wrapper in
  `utils.py` → export it and add an `elif page == "..."` branch + sidebar entry in `app.py`.
- **Region** is fixed to `global` (`REGIONS = ["global"]`); project id resolves from
  `st.secrets["GCP_PROJECT_ID"]`, falling back to `landing-zone-demo-341118`.

## Tools (sidebar pages)

Fine-Tune Prompt · System Prompt · Json Prompt · Nano Banana Json Prompt · Toon Prompt ·
Images (Imagen) · Veo Prompt · Run Prompt · Meta Prompt · Agent Prompt · Zero to Few ·
Chain of Thought · D.A.R.E Prompting · Compress Prompt.

## Setup & run

```bash
pip install -r requirements.txt
# create .streamlit/secrets.toml with: GCP_PROJECT_ID = "your-project-id"
gcloud auth application-default login
streamlit run app.py
```

Helper scripts: `run-venv.sh` (venv launch), `run-claude.sh` / `run.sh` (start Claude
Code against Vertex AI — `run.sh` also runs `setup-data-sharing.sh` to enable Anthropic
data sharing, a prerequisite for gated models like Fable 5).

## Deploy

`./deploy.sh` — builds via Cloud Build and deploys to Cloud Run (project, region
`me-west1`, service `vertex-prompt-playground`). The runtime service account needs the
**Vertex AI User** role.

## Notes

- Models live in `utils.py:MODEL_NAMES`; update there when Gemini versions change.
- Image generation uses `imagen-4.0-fast-generate-001` (hardcoded in
  `utils.py:GenerateImageNew`).
- `GEMINI.md` is being removed in favor of this file.
