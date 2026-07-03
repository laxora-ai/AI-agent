import json
import os
from datetime import datetime, timezone

from app.graph import run_agent


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }


def _parse_body(event: dict) -> dict:
    raw_body = event.get("body") or "{}"
    if isinstance(raw_body, dict):
        return raw_body
    try:
        return json.loads(raw_body)
    except Exception:
        return {}


def lambda_handler(event, context):
    body = _parse_body(event)
    message = body.get("message", "")
    session_id = body.get("session_id", "demo")

    state = run_agent(session_id=session_id, message=message)

    return _response(
        200,
        {
            "session_id": session_id,
            "intent": state.get("intent"),
            "routed_by": state.get("routed_by"),
            "caller_verified": state.get("caller_verified", False),
            "pending_action": state.get("pending_action"),
            "reply": state.get("reply", ""),
            "environment": os.getenv("ENVIRONMENT", "dev"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
