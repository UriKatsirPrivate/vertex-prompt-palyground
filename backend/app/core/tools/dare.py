"""D.A.R.E prompting — multi-field tool (Vision / Mission / Context / Prompt)
plus an artifacts generator. Ported from ``utils.py:dare_it`` /
``create_dare_artifacts``.
"""
from app.core.generation import generate_text
from app.core.prompts.dare_prompts import dare_artifacts_generator, dare_prompt
from app.core.tools.types import ToolContext

_ARTIFACTS_SYSTEM = """
                    You are a GenAI expert capable of generating solid prompts.
                    Context: D.A.R.E prompting works by asking the chatbot to remember its mission and vision before answering a question.
                    This helps to keep the chatbot grounded in reality and prevents it from generating responses that are irrelevant or nonsensical.
                    D.A.R.E uses vision and mission statements to check if the response complies with them
    """


def dare_it(ctx: ToolContext, *, vision: str, mission: str, context: str, prompt: str) -> str:
    formatted = dare_prompt.format(vision=vision, mission=mission, context=context, prompt=prompt)
    return generate_text(
        ctx.client,
        project_id=ctx.project_id,
        region=ctx.region,
        params=ctx.params,
        contents=formatted,
    )


def dare_artifacts(ctx: ToolContext, *, user_input: str) -> str:
    formatted = dare_artifacts_generator.format(user_input=user_input)
    return generate_text(
        ctx.client,
        project_id=ctx.project_id,
        region=ctx.region,
        params=ctx.params,
        contents=formatted,
        system_instruction=_ARTIFACTS_SYSTEM,
    )
