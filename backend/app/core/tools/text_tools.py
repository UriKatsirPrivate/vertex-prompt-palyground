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
from app.core.tools.types import BlockJob, ResultBlock, ToolContext, ToolResult


def _generate(ctx: ToolContext, contents: str, system_instruction: str | None = None) -> str:
    return generate_text(
        ctx.client,
        project_id=ctx.project_id,
        region=ctx.region,
        params=ctx.params,
        contents=contents,
        system_instruction=system_instruction,
    )


def fine_tune_jobs(ctx: ToolContext) -> list[BlockJob]:
    """The four prompt improvements as independent, streamable jobs.

    Each job is one Gemini call described as data (the prompt). The streaming
    endpoint runs them concurrently and emits each block as it lands; the sync
    ``fine_tune`` handler runs the same jobs for the non-streaming path. Single-
    sourced so the prompts and titles never drift between the two.
    """
    task = "improve the prompt"
    return [
        BlockJob("Make (v1)", make_prompt.format(task=task, lazy_prompt=ctx.input)),
        BlockJob("Make (v2)", make_prompt_v2.format(task=task, lazy_prompt=ctx.input)),
        BlockJob("Refine", refine_prompt.format(task=task, lazy_prompt=ctx.input)),
        BlockJob("Improved", prompt_improver.format(text=ctx.input)),
    ]


def fine_tune(ctx: ToolContext) -> ToolResult:
    """Four improvements of the user's prompt (2x2 grid in the UI).

    Runs the jobs sequentially for the plain ``/api/tools/fine_tune`` response;
    the streaming endpoint runs the same jobs concurrently.
    """
    return ToolResult(
        blocks=[
            ResultBlock(
                title=job.title,
                content=_generate(ctx, job.contents, job.system_instruction),
                language=job.language,
            )
            for job in fine_tune_jobs(ctx)
        ]
    )


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
