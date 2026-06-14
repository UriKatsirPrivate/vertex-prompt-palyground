"""Tool endpoints: the generic tool runner plus the special D.A.R.E and Images routes."""
from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    DareArtifactsRequest,
    DareRequest,
    ImageOut,
    ImagePromptsRequest,
    ImagePromptsResponse,
    ImagesRequest,
    ImagesResponse,
    ResultBlockOut,
    TextResponse,
    ToolRequest,
    ToolResponse,
)
from app.core.errors import ValidationError
from app.core.tools import get_tool
from app.core.tools.dare import dare_artifacts, dare_it
from app.core.tools.images import generate_image_prompts, generate_images
from app.deps import build_context

router = APIRouter()


@router.post("/tools/{tool_id}", response_model=ToolResponse)
def run_tool(tool_id: str, req: ToolRequest) -> ToolResponse:
    spec = get_tool(tool_id)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"Unknown tool: {tool_id}")
    if not req.input.strip():
        raise ValidationError("Please enter a prompt.")

    ctx = build_context(req.cfg, input=req.input, fields=req.fields)
    result = spec.handler(ctx)
    return ToolResponse(
        tool_id=tool_id,
        blocks=[
            ResultBlockOut(content=b.content, title=b.title, language=b.language)
            for b in result.blocks
        ],
        meta=result.meta,
    )


@router.post("/dare", response_model=TextResponse)
def run_dare(req: DareRequest) -> TextResponse:
    if not req.prompt.strip():
        raise ValidationError("Please enter a prompt.")
    ctx = build_context(req.cfg)
    content = dare_it(
        ctx,
        vision=req.vision,
        mission=req.mission,
        context=req.context,
        prompt=req.prompt,
    )
    return TextResponse(content=content)


@router.post("/dare/artifacts", response_model=TextResponse)
def run_dare_artifacts(req: DareArtifactsRequest) -> TextResponse:
    if not req.input.strip():
        raise ValidationError("Please enter a prompt.")
    ctx = build_context(req.cfg)
    return TextResponse(content=dare_artifacts(ctx, user_input=req.input))


@router.post("/images/prompts", response_model=ImagePromptsResponse)
def run_image_prompts(req: ImagePromptsRequest) -> ImagePromptsResponse:
    if not req.description.strip():
        raise ValidationError("Please enter a description.")
    ctx = build_context(req.cfg, input=req.description)
    return ImagePromptsResponse(prompts=generate_image_prompts(ctx, count=req.count))


@router.post("/images/generate", response_model=ImagesResponse)
def run_image_generate(req: ImagesRequest) -> ImagesResponse:
    if not req.description.strip():
        raise ValidationError("Please enter a description.")
    # Image generation uses Imagen directly; only the client/project are needed.
    from app.config import get_settings
    from app.core.client import get_client

    s = get_settings()
    client = get_client(s.gcp_project_id, s.gcp_region)
    images = generate_images(client, description=req.description, count=req.count)
    return ImagesResponse(
        images=[ImageOut(mime_type=i.mime_type, data_b64=i.data_b64) for i in images]
    )
