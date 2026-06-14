"""Handlers for the simple text-in / text-out tools.

Each is a direct port of the matching ``utils.py`` wrapper, minus the Streamlit
caching/error decorators.
"""
from app.core.generation import generate_text
from app.core.prompts.agent_prompt import agent_prompt
from app.core.prompts.fine_tune_prompt import (
    make_prompt,
    make_prompt_v2,
    prompt_improver,
    refine_prompt,
)
from app.core.prompts.meta_prompt import metaprompt
from app.core.prompts.system_prompts import NANO_BANANA_PROMPT, SYSTEM_PROMPT
from app.core.prompts.video_prompt import video_prompt
from app.core.tools.types import ResultBlock, ToolContext, ToolResult


def _generate(ctx: ToolContext, contents: str, system_instruction: str | None = None) -> str:
    return generate_text(
        ctx.client,
        project_id=ctx.project_id,
        region=ctx.region,
        params=ctx.params,
        contents=contents,
        system_instruction=system_instruction,
    )


def fine_tune(ctx: ToolContext) -> ToolResult:
    """Four parallel improvements of the user's prompt (2x2 grid in the UI)."""
    task = "improve the prompt"
    blocks = [
        ResultBlock(
            title="Make (v1)",
            content=_generate(ctx, make_prompt.format(task=task, lazy_prompt=ctx.input)),
        ),
        ResultBlock(
            title="Make (v2)",
            content=_generate(ctx, make_prompt_v2.format(task=task, lazy_prompt=ctx.input)),
        ),
        ResultBlock(
            title="Refine",
            content=_generate(ctx, refine_prompt.format(task=task, lazy_prompt=ctx.input)),
        ),
        ResultBlock(
            title="Improved",
            content=_generate(ctx, prompt_improver.format(text=ctx.input)),
        ),
    ]
    return ToolResult(blocks=blocks)


def system_prompt(ctx: ToolContext) -> ToolResult:
    out = _generate(ctx, SYSTEM_PROMPT.format(user_input=ctx.input))
    return ToolResult(blocks=[ResultBlock(content=out)])


def agent(ctx: ToolContext) -> ToolResult:
    out = _generate(ctx, agent_prompt.format(prompt=ctx.input))
    return ToolResult(blocks=[ResultBlock(content=out)])


def meta(ctx: ToolContext) -> ToolResult:
    prompt = metaprompt.replace("{{TASK}}", ctx.input)
    out = _generate(ctx, prompt)
    return ToolResult(blocks=[ResultBlock(content=out)])


def nano_banana(ctx: ToolContext) -> ToolResult:
    out = _generate(ctx, NANO_BANANA_PROMPT.format(user_input=ctx.input))
    return ToolResult(blocks=[ResultBlock(content=out, language="json")])


def run(ctx: ToolContext) -> ToolResult:
    """Run the prompt verbatim against the model."""
    out = _generate(ctx, ctx.input)
    return ToolResult(blocks=[ResultBlock(content=out)])


def zero_to_few(ctx: ToolContext) -> ToolResult:
    system = "You are an assistant designed to convert a zero-shot prompt into a few-shot prompt."
    prompt = (
        f"The zero-shot prompt is: '{ctx.input}'. Please convert it into a few-shot prompt. "
        "Be as elaborate as possible. Make sure to include at least 3 examples."
    )
    out = _generate(ctx, prompt, system_instruction=system)
    return ToolResult(blocks=[ResultBlock(content=out)])


def chain_of_thought(ctx: ToolContext) -> ToolResult:
    system = "You are an assistant designed to convert a prompt into a chain of thought prompt."
    prompt = (
        f"The prompt is: '{ctx.input}'. Please convert it into a chain of thought prompt. "
        "Always append 'Let's think step by step.' to the prompt."
    )
    out = _generate(ctx, prompt, system_instruction=system)
    return ToolResult(blocks=[ResultBlock(content=out)])


def veo(ctx: ToolContext) -> ToolResult:
    out = _generate(ctx, video_prompt.format(user_idea=ctx.input))
    return ToolResult(blocks=[ResultBlock(content=out)])
