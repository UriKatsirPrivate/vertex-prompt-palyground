"""Pydantic request/response models for the API."""
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from app.config import get_settings

# Requests carry the model config under the JSON key "modelConfig". We expose it
# on a Python attribute named ``cfg`` (avoiding Pydantic's protected ``model_``
# namespace) and accept the field by either name.
_REQUEST_CONFIG = ConfigDict(populate_by_name=True)


class ModelConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    model_name: str
    temperature: float = 1.0
    top_p: float = 0.8
    max_tokens: int = 65535


def default_model_config() -> ModelConfig:
    s = get_settings()
    return ModelConfig(
        model_name=s.default_model,
        temperature=s.default_temperature,
        top_p=s.default_top_p,
        max_tokens=s.default_max_tokens,
    )


# ---- Generic tool endpoint ----
class ToolRequest(BaseModel):
    model_config = _REQUEST_CONFIG

    input: str = ""
    cfg: Annotated[ModelConfig, Field(alias="modelConfig")]
    fields: dict[str, str] = {}


class ResultBlockOut(BaseModel):
    content: str
    title: str | None = None
    language: str | None = None


class ToolResponse(BaseModel):
    tool_id: str
    blocks: list[ResultBlockOut]
    meta: dict = {}


# ---- D.A.R.E ----
class DareRequest(BaseModel):
    model_config = _REQUEST_CONFIG

    vision: str = ""
    mission: str = ""
    context: str = ""
    prompt: str
    cfg: Annotated[ModelConfig, Field(alias="modelConfig")]


class DareArtifactsRequest(BaseModel):
    model_config = _REQUEST_CONFIG

    input: str
    cfg: Annotated[ModelConfig, Field(alias="modelConfig")]


class TextResponse(BaseModel):
    content: str


# ---- Images ----
class ImagePromptsRequest(BaseModel):
    model_config = _REQUEST_CONFIG

    description: str
    count: int = 2
    cfg: Annotated[ModelConfig, Field(alias="modelConfig")]


class ImagePromptsResponse(BaseModel):
    prompts: str


class ImagesRequest(BaseModel):
    description: str
    count: int = 2


class ImageOut(BaseModel):
    mime_type: str
    data_b64: str


class ImagesResponse(BaseModel):
    images: list[ImageOut]


# ---- Config ----
class ToolMeta(BaseModel):
    id: str
    label: str
    category: str
    route: str
    placeholder: str = ""
    help_url: str | None = None
    output_kind: str = "text"
    multi_result: bool = False


class ConfigDefaults(BaseModel):
    temperature: float
    top_p: float
    max_tokens: int
    temperature_range: list[float]
    top_p_range: list[float]
    max_tokens_range: list[int]


class ConfigResponse(BaseModel):
    models: list[str]
    default_model: str
    regions: list[str]
    defaults: ConfigDefaults
    tools: list[ToolMeta]


class ErrorResponse(BaseModel):
    detail: str
    code: str
