from .notifications import send_appointment_confirmation
from .state import AgentState


def scheduling_node(state: AgentState) -> AgentState:
    """POC scheduling path.

    This is where real booking logic will live:
      1. read open slots from DynamoDB
      2. propose 2-3 slots
      3. store user's choice as pending_action
      4. create/update appointment
      5. send SES confirmation
      6. write audit event
    """
    message = state.get("message", "")

    if "cancel" in message.lower():
        return {
            **state,
            "reply": "I can help cancel the appointment. For the POC, cancellation logic will update DynamoDB and emit an EventBridge waitlist event next.",
        }

    sent = send_appointment_confirmation(
        to_email="",
        subject="Laxora appointment confirmation",
        body="Your appointment is confirmed.",
    )

    return {
        **state,
        "reply": (
            "I can help with scheduling. For the POC, the next step is to connect this "
            "path to the DynamoDB slots table, then send SES confirmation. "
            f"Email sent now: {sent}."
        ),
    }
