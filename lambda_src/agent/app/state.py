from typing import Any, Literal, Optional, TypedDict

Intent = Literal["scheduling", "billing", "waitlist", "smalltalk", "blocked"]
RouteSource = Literal["rules", "llm", "pending_action"]


class AgentState(TypedDict, total=False):
    """State that moves through the POC agent flow.

    Keep this simple for the inexpensive AWS POC. DynamoDB will store this per
    session_id between Lambda invocations.
    """

    session_id: str
    message: str
    reply: str

    intent: Optional[Intent]
    routed_by: Optional[RouteSource]

    caller_verified: bool
    customer_id: Optional[str]

    pending_action: Optional[str]
    pending_data: dict[str, Any]
    retry_count: int

    guardrail_flags: list[str]
    blocked_reason: Optional[str]

    loop_count: int
    token_budget_remaining: int


DEFAULT_STATE: AgentState = {
    "intent": None,
    "routed_by": None,
    "caller_verified": False,
    "customer_id": None,
    "pending_action": None,
    "pending_data": {},
    "retry_count": 0,
    "guardrail_flags": [],
    "blocked_reason": None,
    "loop_count": 0,
    "token_budget_remaining": 8000,
}
