"""Typed errors for the service layer.

The Streamlit app swallowed failures into ``st.error`` and returned ``""``.
Here the core raises typed exceptions and FastAPI maps them to HTTP responses
(see ``app.main``).
"""


class PlaygroundError(Exception):
    """Base class for all expected service-layer errors."""

    code = "error"
    http_status = 500


class ValidationError(PlaygroundError):
    """Bad input (e.g. empty prompt)."""

    code = "validation_error"
    http_status = 400


class SafetyBlockedError(PlaygroundError):
    """The model returned no content — typically a safety-filter block."""

    code = "safety_blocked"
    http_status = 422


class UpstreamError(PlaygroundError):
    """The Vertex AI call itself failed."""

    code = "upstream_error"
    http_status = 502
