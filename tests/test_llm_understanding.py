from ai_engine.data_understanding_agent import (
    DataUnderstandingAgent,
    DataUnderstandingResult
)

from ai_engine.schema_manager import SchemaManager
from ai_engine.conversation_manager import ConversationManager
from ai_engine.openrouter_client import OpenRouterClient


# ============================================================
# SETUP
# ============================================================

schema = SchemaManager()

conversation = ConversationManager()

openrouter = OpenRouterClient()

agent = DataUnderstandingAgent(
    schema_manager=schema,
    conversation_manager=conversation,
    llm_client=openrouter
)


# ============================================================
# TEST 1 — BASIC LLM UNDERSTANDING
# ============================================================

print()
print("=" * 60)
print("TEST 1 — BASIC LLM UNDERSTANDING")
print("=" * 60)

query = "Show revenue by department"

metadata = agent._search_metadata(
    query
)

result = agent._get_llm_result(
    query=query,
    metadata=metadata
)

print()
print("Result:")
print(result)


# ============================================================
# TEST 2 — VALIDATION
# ============================================================

print()
print("=" * 60)
print("TEST 2 — LLM VALIDATION")
print("=" * 60)

try:

    valid = agent._validate_llm_result(
        result
    )

    print(
        "Validation:",
        valid
    )

except ValueError as exc:

    print(
        "Validation FAILED:",
        exc
    )


# ============================================================
# TEST 3 — HALLUCINATION PROTECTION
# ============================================================

print()
print("=" * 60)
print("TEST 3 — HALLUCINATION PROTECTION")
print("=" * 60)

fake_result = DataUnderstandingResult(

    query="Show revenue by department",

    intent="test",

    selected_dataset="finance",

    dataset_confidence=0.99,

    metrics=[
        "fake_metric"
    ],

    dimensions=[
        "department_name"
    ],

    filters=[]
)

try:

    agent._validate_llm_result(
        fake_result
    )

    print(
        "ERROR: Invalid result was accepted!"
    )

except ValueError as exc:

    print(
        "PASS:",
        exc
    )


# ============================================================
# TEST 4 — CONVERSATION-AWARE LLM
# ============================================================

print()
print("=" * 60)
print("TEST 4 — CONVERSATION-AWARE LLM")
print("=" * 60)


conversation_context = {
    "selected_dataset": "finance",

    "dataset_confidence": 0.95,

    "metrics": [
        "department_total_revenue"
    ],

    "dimensions": [
        "department_name"
    ],

    "filters": [],

    "group_by": [],

    "sort_by": None,

    "limit": None
}


follow_up_query = "Sort it by highest revenue"


metadata = agent._search_metadata(
    follow_up_query
)

result = agent._get_llm_result(
    query=follow_up_query,
    metadata=metadata,
    conversation_context=conversation_context
)

print()
print("Follow-up Query:")
print(follow_up_query)

print()
print("Result:")
print(result)


# ============================================================
# TEST COMPLETE
# ============================================================

print()
print("=" * 60)
print("ALL STEP 3 TESTS COMPLETED")
print("=" * 60)