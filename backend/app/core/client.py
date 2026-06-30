"""Vertex AI GenAI client factory.

The genai client's underlying transport/auth context is NOT safe for concurrent
use from multiple threads: when several requests share one client at once, all
but one fail with "Context has already been used to create a Connection, it
cannot be mutated again". FastAPI runs sync endpoints in a threadpool (and Cloud
Run serves with concurrency > 1), so a single process-wide shared client races.

We therefore keep one client per thread. A thread handles a single request at a
time, so its client is never driven concurrently. The async streaming endpoint
runs in the event-loop thread and uses that thread's client via ``client.aio``,
which httpx *does* multiplex safely within one loop.
"""
import threading

from google import genai

_local = threading.local()


def get_client(project_id: str, region: str) -> genai.Client:
    cache: dict | None = getattr(_local, "clients", None)
    if cache is None:
        cache = _local.clients = {}
    key = (project_id, region)
    client = cache.get(key)
    if client is None:
        client = cache[key] = genai.Client(
            vertexai=True, project=project_id, location=region
        )
    return client
