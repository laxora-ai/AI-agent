import os
import re
from typing import Optional

import boto3

from .state import AgentState, Intent

bedrock = boto3.client("bedrock-runtime")

CLASSIFIER_MODEL_ID = os.getenv(
    "BEDROCK_CLASSIFIER_MODEL_ID",
    "us.anthropic.claude-haiku-4-5-20251001-v1:0",
)

RULE_PATTERNS: dict[Intent, list[str]] = {
    "scheduling": [
        r"\b(appointment|appt|book|schedule|reschedul|cancel|move|availab|opening|slot)\w*\b",
        r"\bwhat time\b",
        r"\bcome in\b",
    ],
    "billing": [
        r"\b(payment|paid|pay|bill|invoice|charge|refund|balance|receipt)\w*\b",
        r"\b(insurance|coverage|copay|co-pay|claim|deductible)\w*\b",
        r"\bno[- ]?show\b",
    ],
    "waitlist": [
        r"\bwait[- ]?list\b",
        r"\bcancellation list\b",
        r"\bif (anything|a spot|something) opens\b",
    ],
}

_COMPILED = {
    intent: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for intent, patterns in RULE_PATTERNS.items()
}

_CLASSIFIER_SYSTEM = (
    "You classify a customer message for a front-desk assistant. "
    "Respond with exactly one word from: scheduling, billing, waitlist, smalltalk."
)


def classify_with_rules(text: str) -> Optional[Intent]:
    hits = {
        intent
        for intent, patterns in _COMPILED.items()
        if any(pattern.search(text) for pattern in patterns)
    }
    return hits.pop() if len(hits) == 1 else None


def classify_with_llm(text: str) -> Intent:
    """Fallback classifier for ambiguous messages.

    For local tests without AWS credentials, this safely returns smalltalk.
    """
    try:
        response = bedrock.converse(
            modelId=CLASSIFIER_MODEL_ID,
            system=[{"text": _CLASSIFIER_SYSTEM}],
            messages=[{"role": "user", "content": [{"text": text[:1000]}]}],
            inferenceConfig={"maxTokens": 8, "temperature": 0},
        )
        word = response["output"]["message"]["content"][0]["text"].strip().lower()
        if word in {"scheduling", "billing", "waitlist", "smalltalk"}:
            return word  # type: ignore[return-value]
    except Exception as exc:
        print(f"LLM routing fallback failed: {exc}")

    return "smalltalk"


def router_node(state: AgentState) -> AgentState:
    text = state.get("message", "")

    intent = classify_with_rules(text)
    if intent:
        return {**state, "intent": intent, "routed_by": "rules"}

    return {**state, "intent": classify_with_llm(text), "routed_by": "llm"}
