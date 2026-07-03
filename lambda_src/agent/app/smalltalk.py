from .state import AgentState


def smalltalk_node(state: AgentState) -> AgentState:
    return {
        **state,
        "reply": "Hi, I’m the Laxora front-desk assistant. I can help with appointments, billing questions, insurance questions, or waitlist requests.",
    }
