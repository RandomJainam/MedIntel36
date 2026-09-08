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
# RUN QUERY
# ============================================================

print()
print("=" * 60)
print("CONVERSATION HISTORY TEST")
print("=" * 60)

query = "Show revenue by department"

result = agent.understand(
    query
)


# ============================================================
# GET HISTORY
# ============================================================

history = conversation.get_history()

print()
print("Conversation History:")
print(history)


# ============================================================
# ASSERT USER MESSAGE
# ============================================================

assert len(history) == 2

assert history[0]["role"] == "user"

assert (
    history[0]["content"]
    == "Show revenue by department"
)


# ============================================================
# ASSERT ASSISTANT MESSAGE
# ============================================================

assert history[1]["role"] == "assistant"

assert (
    "finance"
    in history[1]["content"]
)

assert (
    "department_total_revenue"
    in history[1]["content"]
)

assert (
    "department_name"
    in history[1]["content"]
)


print()
print(
    "PASS: Conversation history "
    "stored correctly."
)


# ============================================================
# DISPLAY STRUCTURED CONTEXT
# ============================================================

print()
print("=" * 60)
print("STRUCTURED CONTEXT")
print("=" * 60)

print(
    conversation.get_context()
)