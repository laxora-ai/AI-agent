from .billing import billing_node
from .guardrails import input_guardrails_node, needs_identity, identity_gate_node, output_guardrails_node
from .router import router_node
from .scheduling import scheduling_node
from .smalltalk import smalltalk_node
from .state import AgentState, DEFAULT_STATE
from .waitlist import waitlist_node

PATHS = {
    "scheduling": scheduling_node,
    "billing": billing_node,
    "waitlist": waitlist_node,
    "smalltalk": smalltalk_node,
}


def run_agent(session_id: str, message: str, saved_state: AgentState | None = None) -> AgentState:
    """Simple graph runner for the cheap AWS POC.

    This intentionally avoids LangGraph for the first deploy. The goal is to make
    the flow easy to understand and easy to run inside Lambda.
    """
    state: AgentState = {
        **DEFAULT_STATE,
        **(saved_state or {}),
        "session_id": session_id,
        "message": message,
    }

    state = input_guardrails_node(state)
    if state.get("intent") == "blocked":
        return output_guardrails_node(state)

    state = router_node(state)

    if needs_identity(state):
        state = identity_gate_node(state)
        return output_guardrails_node(state)

    path = PATHS.get(state.get("intent") or "smalltalk", smalltalk_node)
    state = path(state)
    return output_guardrails_node(state)
