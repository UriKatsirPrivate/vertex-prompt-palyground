"""Shared types for the tool registry."""
from dataclasses import dataclass, field
from typing import Callable

from google import genai

from app.core.generation import GenerationParams


@dataclass
class ToolContext:
    """Everything a tool handler needs for one invocation."""

    client: genai.Client
    project_id: str
    region: str
    params: GenerationParams
    input: str = ""
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class ResultBlock:
    content: str
    title: str | None = None
    language: str | None = None  # e.g. "json" → frontend syntax highlighting


@dataclass
class ToolResult:
    blocks: list[ResultBlock]
    meta: dict = field(default_factory=dict)


Handler = Callable[[ToolContext], ToolResult]


@dataclass
class ToolSpec:
    id: str
    label: str
    category: str
    handler: Handler
    placeholder: str = ""
    help_url: str | None = None
    output_kind: str = "text"  # "text" | "json" | "toon" | "stats"
    multi_result: bool = False
