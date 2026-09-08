from ai_engine.data_understanding_agent import (
    DataUnderstandingAgent
)

from ai_engine.schema_manager import (
    SchemaManager
)

from ai_engine.conversation_manager import (
    ConversationManager
)

from ai_engine.openrouter_client import (
    OpenRouterClient
)


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
# FIRST QUERY
# ============================================================

print()
print("=" * 60)
print("FIRST QUERY")
print("=" * 60)

first_query = (
    "Show revenue by department"
)

first_result = agent.understand(
    first_query
)

print()
print("First Result:")
print(first_result)

print()
print("Context After First Query:")
print(
    conversation.get_context()
)


# ============================================================
# VERIFY FIRST CONTEXT
# ============================================================

assert (
    conversation.get_context()
    ["selected_dataset"]
    == "finance"
)

assert (
    "department_total_revenue"
    in conversation.get_context()
    ["metrics"]
)

assert (
    "department_name"
    in conversation.get_context()
    ["dimensions"]
)


print()
print(
    "PASS: First query created context."
)


# ============================================================
# SECOND QUERY
# ============================================================

print()
print("=" * 60)
print("FOLLOW-UP QUERY")
print("=" * 60)

second_query = (
    "Only Cardiology"
)

print()
print("Query:")
print(second_query)

print()
print(
    "Detected Follow-Up:",
    agent.is_follow_up(
        second_query
    )
)


assert (
    agent.is_follow_up(
        second_query
    )
    is True
)


# ============================================================
# RUN FOLLOW-UP
# ============================================================

second_result = agent.understand(
    second_query
)

print()
print("Second Result:")
print(second_result)


# ============================================================
# VERIFY CONTEXT
# ============================================================

context = conversation.get_context()

print()
print("Context After Follow-Up:")
print(context)


# ============================================================
# EXPECTED BEHAVIOR
# ============================================================

assert (
    context["selected_dataset"]
    == "finance"
)

assert (
    "department_total_revenue"
    in context["metrics"]
)

assert (
    "department_name"
    in context["dimensions"]
)


print()
print(
    "PASS: Existing analytical context "
    "was preserved."
)