"""Text generation against Vertex AI.

Pure port of the Streamlit app's ``generate_llm_content`` — no ``st.*``. Builds a
``GenerateContentConfig`` per call from the request's model params plus the shared
safety settings, and raises typed errors instead of writing to ``st.error``.
"""
from dataclasses import dataclass

from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig

from app.config import get_settings
from app.core.errors import SafetyBlockedError, UpstreamError
from app.core.safety import safety_settings


@dataclass
class GenerationParams:
    """Per-request model configuration (was the Streamlit sliders)."""

    model_name: str
    temperature: float = 1.0
    top_p: float = 0.8
    max_tokens: int = 65535


def _model_path(project_id: str, region: str, model_name: str) -> str:
    return (
        f"projects/{project_id}/locations/{region}"
        f"/publishers/google/models/{model_name}"
    )


def _build_call(
    params: GenerationParams, contents: str, system_instruction: str | None
) -> tuple[GenerateContentConfig, list[types.Part]]:
    """Shared request assembly for the sync and async generation paths."""
    config = GenerateContentConfig(
        temperature=params.temperature,
        top_p=params.top_p,
        max_output_tokens=params.max_tokens,
        safety_settings=safety_settings,
    )
    parts: list[types.Part] = []
    if system_instruction:
        parts.append(types.Part(text=system_instruction))
    parts.append(types.Part(text=contents))
    return config, parts


def _require_text(text: str | None) -> str:
    if not text:
        raise SafetyBlockedError(
            "The model returned no content. It may have been blocked by safety filters."
        )
    return text


def generate_text(
    client: genai.Client,
    *,
    project_id: str,
    region: str,
    params: GenerationParams,
    contents: str,
    system_instruction: str | None = None,
) -> str:
    """Generate text and return ``response.text``.

    Raises ``UpstreamError`` on API failure and ``SafetyBlockedError`` when the
    model returns no text (the usual signature of a safety-filtered response).
    """
    config, parts = _build_call(params, contents, system_instruction)
    try:
        response = client.models.generate_content(
            model=_model_path(project_id, region, params.model_name),
            contents=parts,
            config=config,
        )
    except Exception as e:  # noqa: BLE001 - surface any SDK/transport error uniformly
        raise UpstreamError(str(e)) from e
    return _require_text(response.text)


async def generate_text_async(
    client: genai.Client,
    *,
    project_id: str,
    region: str,
    params: GenerationParams,
    contents: str,
    system_instruction: str | None = None,
) -> str:
    """Async counterpart of :func:`generate_text`.

    Uses the client's async API (``client.aio``), which is safe to drive
    concurrently from one event loop — unlike sharing the sync client across
    threads, which races on its transport/auth context. This is what lets the
    streaming endpoint run a tool's blocks in parallel on the shared client.
    """
    config, parts = _build_call(params, contents, system_instruction)
    try:
        response = await client.aio.models.generate_content(
            model=_model_path(project_id, region, params.model_name),
            contents=parts,
            config=config,
        )
    except Exception as e:  # noqa: BLE001 - surface any SDK/transport error uniformly
        raise UpstreamError(str(e)) from e
    return _require_text(response.text)


def default_params() -> GenerationParams:
    s = get_settings()
    return GenerationParams(
        model_name=s.default_model,
        temperature=s.default_temperature,
        top_p=s.default_top_p,
        max_tokens=s.default_max_tokens,
    )
