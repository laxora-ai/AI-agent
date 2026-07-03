from .state import AgentState


def billing_node(state: AgentState) -> AgentState:
    """POC billing path.

    Later this will split into:
      - live status lookup from DynamoDB/payments table
      - insurance/policy question through RAG
    """
    return {
        **state,
        "reply": "I can help with billing or insurance. For the POC, this path will use verified identity before showing account-specific payment information.",
    }
