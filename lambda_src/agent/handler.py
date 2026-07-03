import json
import os
from datetime import datetime, timezone


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    """Minimal placeholder handler so Terraform can deploy a working Lambda.

    Replace this with the real LangGraph/FastAPI adapter after the agent code is
    added. For now it proves AWS wiring, environment variables, logging, and the
    invocation path.
    """
    try:
        raw_body = event.get("body") or "{}"
        body = json.loads(raw_body) if isinstance(raw_body, str) else raw_body
    except Exception:
        body = {}

    message = body.get("message", "")
    session_id = body.get("session_id", "demo")

    return _response(
        200,
        {
            "session_id": session_id,
            "reply": "Laxora agent infrastructure is running. Agent brain will be wired here next.",
            "echo": message,
            "environment": os.getenv("ENVIRONMENT", "dev"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
