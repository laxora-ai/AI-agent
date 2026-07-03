import re

from .state import AgentState

MEDICAL_REDIRECT = (
    "I'm not able to answer medical questions, but I can have the office call you back "
    "or help you book an appointment. Which would you prefer?"
)

IDENTITY_PROMPT = (
    "I can help with that. First I need to verify your identity. "
    "Please provide your full name and date of birth."
)

IDENTITY_REQUIRED = {"scheduling", "billing"}

_MEDICAL_ADVICE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in [
        r"\bshould i (take|stop|use|get|be worried|be concerned)\b",
        r"\b(is|are) (it|this|that|my|the)\b.{0,30}?\b(normal|safe|okay|ok|infected|serious)\b",
        r"\bwhat (medication|antibiotic|dosage|dose)\b",
        r"\b(diagnos|prescri)\w*\b",
        r"\bdo i (need|have) (a|an) (root canal|crown|filling|extraction|surgery)\b",
        r"\bside effects?\b",
    ]
]


def input_guardrails_node(state: AgentState) -> AgentState:
    text = state.get("message", "")

    if any(pattern.search(text) for pattern in _MEDICAL_ADVICE_PATTERNS):
        return {
            **state,
            "intent": "blocked",
            "blocked_reason": "medical_question",
            "guardrail_flags": state.get("guardrail_flags", []) + ["medical_question"],
            "reply": MEDICAL_REDIRECT,
        }

    return state


def needs_identity(state: AgentState) -> bool:
    return state.get("intent") in IDENTITY_REQUIRED and not state.get("caller_verified", False)


def identity_gate_node(state: AgentState) -> AgentState:
    """POC identity gate.

    Next implementation step: parse the user's name and DOB, look up the
    customer in DynamoDB by session_id/phone, compare values, then set:
      caller_verified=True
      customer_id=<customer id>
    """
    return {
        **state,
        "pending_action": "verify_identity",
        "pending_data": {"original_intent": state.get("intent")},
        "reply": IDENTITY_PROMPT,
    }


def output_guardrails_node(state: AgentState) -> AgentState:
    """Very small output scrub for the POC.

    Keep managed Bedrock Guardrails off until the basic app flow works.
    """
    reply = state.get("reply", "")
    reply = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "***-**-****", reply)
    return {**state, "reply": reply}
