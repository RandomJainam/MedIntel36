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
# UNDERSTAND QUERY
# ============================================================

print()
print("=" * 60)
print("UNDERSTANDING + CONVERSATION INTEGRATION")
print("=" * 60)

query = "Show revenue by department"

result = agent.understand(
    query
)


# ============================================================
# RESULT
# ============================================================

print()
print("Data Understanding Result:")
print(result)


# ============================================================
# CONVERSATION CONTEXT
# ============================================================

context = conversation.get_context()

print()
print("Conversation Context:")
print(context)


# ============================================================
# ASSERTIONS
# ============================================================

assert (
    context["selected_dataset"]
    == result.selected_dataset
)

assert (
    context["dataset_confidence"]
    == result.dataset_confidence
)

assert (
    context["metrics"]
    == result.metrics
)

assert (
    context["dimensions"]
    == result.dimensions
)

assert (
    context["filters"]
    == result.filters
)


print()
print(
    "PASS: DataUnderstandingAgent "
    "updated ConversationManager automatically."
)