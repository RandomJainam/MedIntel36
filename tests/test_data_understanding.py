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
# TEST HELPERS
# ============================================================

def print_section(title):

    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def print_result(result):

    print()
    print("Result:")
    print(result)

    print()
    print("Result Type:")
    print(type(result))

    if isinstance(
        result,
        DataUnderstandingResult
    ):

        print()
        print("Query:")
        print(result.query)

        print()
        print("Intent:")
        print(result.intent)

        print()
        print("Dataset:")
        print(result.selected_dataset)

        print()
        print("Dataset Confidence:")
        print(result.dataset_confidence)

        print()
        print("Metrics:")
        print(result.metrics)

        print()
        print("Dimensions:")
        print(result.dimensions)

        print()
        print("Filters:")
        print(result.filters)

        print()
        print("Requires Clarification:")
        print(result.requires_clarification)

        print()
        print("Clarification Question:")
        print(result.clarification_question)


# ============================================================
# TEST 1
# AGENT INITIALIZATION
# ============================================================

print_section(
    "TEST 1 — AGENT INITIALIZATION"
)

print(
    "Agent:",
    type(agent).__name__
)

print(
    "Schema:",
    type(schema).__name__
)

print(
    "Conversation:",
    type(conversation).__name__
)

print(
    "LLM Client:",
    type(openrouter).__name__
)

print("PASS: Agent initialized successfully.")


# ============================================================
# TEST 2
# SCHEMA METADATA RETRIEVAL
# ============================================================

print_section(
    "TEST 2 — SCHEMA METADATA RETRIEVAL"
)

query = "Show revenue by department"

metadata = agent._search_metadata(
    query
)

print()
print("Query:")
print(query)

print()
print("Datasets:")
print(metadata["datasets"])

print()
print("Metrics:")
print(metadata["metrics"])

print()
print("Dimensions:")
print(metadata["dimensions"])

print()
print("Glossary:")
print(metadata["glossary"])

print()
print("PASS: Metadata retrieval completed.")


# ============================================================
# TEST 3
# DIRECT LLM CALL
# ============================================================

print_section(
    "TEST 3 — DIRECT LLM CALL"
)

response = agent._call_llm(
    query,
    metadata
)

print()
print("Raw LLM Response:")
print(response)

print()
print("PASS: LLM response received.")


# ============================================================
# TEST 4
# JSON PARSING
# ============================================================

print_section(
    "TEST 4 — JSON PARSING"
)

parsed = agent._parse_llm_response(
    response
)

print()
print("Parsed Type:")
print(type(parsed))

print()
print("Parsed Response:")
print(parsed)

print()
print("PASS: LLM response parsed successfully.")


# ============================================================
# TEST 5
# NORMALIZATION
# ============================================================

print_section(
    "TEST 5 — RESULT NORMALIZATION"
)

normalized = agent._normalize_llm_result(
    query,
    parsed
)

print_result(
    normalized
)

print()
print("PASS: LLM result normalized successfully.")


# ============================================================
# TEST 6
# VALIDATION
# ============================================================

print_section(
    "TEST 6 — VALID LLM RESULT VALIDATION"
)

try:

    valid = agent._validate_llm_result(
        normalized
    )

    print(
        "Validation:",
        valid
    )

    print()
    print(
        "PASS: Valid LLM result accepted."
    )

except ValueError as exc:

    print()
    print(
        "FAIL: Valid result was rejected."
    )

    print(
        "Error:",
        exc
    )


# ============================================================
# TEST 7
# HALLUCINATION REJECTION
# ============================================================

print_section(
    "TEST 7 — HALLUCINATION REJECTION"
)

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
        "FAIL: Invalid metric was accepted!"
    )

except ValueError as exc:

    print(
        "PASS: Hallucinated metric rejected."
    )

    print(
        "Error:",
        exc
    )


# ============================================================
# TEST 8
# FULL UNDERSTAND() PIPELINE
# ============================================================

print_section(
    "TEST 8 — FULL UNDERSTAND PIPELINE"
)

query = "Show revenue by department"

result = agent.understand(
    query
)

print_result(
    result
)

print()
print("PASS: Full understanding pipeline completed.")


# ============================================================
# TEST 9
# SECOND REAL QUERY
# ============================================================

print_section(
    "TEST 9 — SECOND QUERY"
)

query = (
    "Show average length of stay "
    "for patients"
)

result = agent.understand(
    query
)

print_result(
    result
)

print()
print("PASS: Second query completed.")


# ============================================================
# TEST 10
# EMPTY QUERY
# ============================================================

print_section(
    "TEST 10 — EMPTY QUERY VALIDATION"
)

try:

    agent.understand(
        "   "
    )

    print(
        "FAIL: Empty query was accepted!"
    )

except ValueError as exc:

    print(
        "PASS: Empty query rejected."
    )

    print(
        "Error:",
        exc
    )


# ============================================================
# TEST 11
# NON-STRING QUERY
# ============================================================

print_section(
    "TEST 11 — NON-STRING QUERY VALIDATION"
)

try:

    agent.understand(
        12345
    )

    print(
        "FAIL: Non-string query was accepted!"
    )

except TypeError as exc:

    print(
        "PASS: Non-string query rejected."
    )

    print(
        "Error:",
        exc
    )


# ============================================================
# COMPLETE
# ============================================================

print_section(
    "ALL DATA UNDERSTANDING TESTS COMPLETED"
)