from ai_engine.conversation_manager import (
    ConversationManager
)

from ai_engine.data_understanding_agent import (
    DataUnderstandingResult
)


# ============================================================
# SETUP
# ============================================================

conversation = ConversationManager()


# ============================================================
# CREATE DATA UNDERSTANDING RESULT
# ============================================================

result = DataUnderstandingResult(

    query="Show revenue by department",

    intent="Show revenue by department",

    selected_dataset="finance",

    dataset_confidence=0.95,

    metrics=[
        "department_total_revenue"
    ],

    dimensions=[
        "department_name"
    ],

    filters=[]
)


# ============================================================
# UPDATE CONVERSATION CONTEXT
# ============================================================

print()
print("=" * 60)
print("CONVERSATION CONTEXT UPDATE TEST")
print("=" * 60)

conversation.update_from_result(
    result
)


# ============================================================
# DISPLAY CONTEXT
# ============================================================

context = conversation.get_context()

print()
print("Context:")
print(context)


# ============================================================
# ASSERTIONS
# ============================================================

assert (
    context["selected_dataset"]
    == "finance"
)

assert (
    context["dataset_confidence"]
    == 0.95
)

assert (
    context["metrics"]
    == ["department_total_revenue"]
)

assert (
    context["dimensions"]
    == ["department_name"]
)

assert (
    context["filters"]
    == []
)


print()
print("PASS: Conversation context updated correctly.")