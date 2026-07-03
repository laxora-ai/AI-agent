from .state import AgentState


def waitlist_node(state: AgentState) -> AgentState:
    """POC waitlist path.

    Later this will write preferences to the DynamoDB waitlist table.
    The waitlist reactor Lambda handles fulfillment after cancellations.
    """
    return {
        **state,
        "reply": "I can add you to the waitlist. For the POC, this path will collect service and time preferences, then save them to DynamoDB.",
    }
