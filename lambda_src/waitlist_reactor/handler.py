import json
from datetime import datetime, timezone


def lambda_handler(event, context):
    """Minimal waitlist reactor placeholder.

    EventBridge will invoke this when the agent emits an appointment.cancelled
    event. Replace this with DynamoDB waitlist matching and SES notification.
    """
    print(
        json.dumps(
            {
                "message": "waitlist reactor invoked",
                "event": event,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"ok": True}),
    }
