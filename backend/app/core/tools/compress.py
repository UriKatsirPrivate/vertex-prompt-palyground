"""Compress Prompt — local prompt trimming via gptrim (no LLM call)."""
from gptrim import trim

from app.core.tools.types import ResultBlock, ToolContext, ToolResult


def compress(ctx: ToolContext) -> ToolResult:
    original = ctx.input
    trimmed = trim(original)
    original_len = len(original)
    compressed_len = len(trimmed)
    reduction_pct = (
        round((original_len - compressed_len) / original_len * 100, 2)
        if original_len
        else 0.0
    )
    return ToolResult(
        blocks=[ResultBlock(content=trimmed)],
        meta={
            "original_len": original_len,
            "compressed_len": compressed_len,
            "reduction_pct": reduction_pct,
        },
    )
