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
# NO CONTEXT
# ============================================================

print()
print("=" * 60)
print("FOLLOW-UP DETECTION — NO CONTEXT")
print("=" * 60)

assert (
    agent.is_follow_up(
        "Only Cardiology"
    )
    is False
)

print(
    "PASS: Query without context "
    "is not treated as follow-up."
)


# ============================================================
# CREATE CONTEXT
# ============================================================

conversation.update_from_result(

    DataUnderstandingResult(

        query="Show revenue by department",

        intent="Show revenue by department",

        selected_dataset="finance",

        dataset_confidence=0.9,

        metrics=[
            "department_total_revenue"
        ],

        dimensions=[
            "department_name"
        ],

        filters=[]
    )
)


# ============================================================
# FOLLOW-UP QUERIES
# ============================================================

print()
print("=" * 60)
print("FOLLOW-UP DETECTION — WITH CONTEXT")
print("=" * 60)


follow_ups = [

    "Only Cardiology",

    "Just Neurology",

    "Exclude Orthopedics",

    "Sort descending",

    "Limit to 5",

    "Top 5"

]


for query in follow_ups:

    result = agent.is_follow_up(
        query
    )

    print(
        f"{query!r} -> {result}"
    )

    assert result is True


print()
print(
    "PASS: Follow-up queries detected."
)


# ============================================================
# NEW / INDEPENDENT QUERIES
# ============================================================

print()
print("=" * 60)
print("INDEPENDENT QUERY DETECTION")
print("=" * 60)


independent_queries = [

    "Show average length of stay",

    "Show patients by city",

    "Show disease distribution",

    "Show bed occupancy"

]


for query in independent_queries:

    result = agent.is_follow_up(
        query
    )

    print(
        f"{query!r} -> {result}"
    )

    assert result is False


print()
print(
    "PASS: Independent queries "
    "are not treated as follow-ups."
)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("FOLLOW-UP DETECTION TEST COMPLETE")
print("=" * 60)