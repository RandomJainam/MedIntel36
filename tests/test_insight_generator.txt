from ai_engine.insight_generator import (
    InsightGenerator
)

from database.executor import (
    DatabaseExecutionResult
)


print()
print("=" * 60)
print("INSIGHT GENERATOR — PHASE 4.4")
print("=" * 60)


# ============================================================
# MOCK LLM
# ============================================================

class MockLLM:

    def __init__(
        self,
        response="Mock analytical answer."
    ):

        self.response = response

        self.last_system_prompt = None

        self.last_user_prompt = None

    def chat(
        self,
        system_prompt,
        user_prompt,
        temperature=0.1,
        max_tokens=1000
    ):

        self.last_system_prompt = (
            system_prompt
        )

        self.last_user_prompt = (
            user_prompt
        )

        return self.response


# ============================================================
# TEST 1 — Successful Insight Generation
# ============================================================

print()
print("TEST 1 — Successful Insight Generation")
print()


llm = MockLLM(
    "Emergency has the highest total revenue."
)

generator = InsightGenerator(
    llm_client=llm
)


execution_result = DatabaseExecutionResult(

    success=True,

    columns=[
        "department_name",
        "department_total_revenue"
    ],

    rows=[
        {
            "department_name": "Emergency",
            "department_total_revenue": 5836589304000
        },
        {
            "department_name": "ICU",
            "department_total_revenue": 2329039633998
        }
    ],

    row_count=2,

    truncated=False
)


result = generator.generate(

    query=(
        "Which department has the highest "
        "total revenue?"
    ),

    execution_result=execution_result
)


print("Result:")
print(result)


if result.has_data:

    print()
    print("PASS: Data detected.")

else:

    print()
    print("FAIL: Data was not detected.")

    raise SystemExit(1)


if result.answer:

    print()
    print("PASS: Analytical answer generated.")

else:

    print()
    print("FAIL: No analytical answer generated.")

    raise SystemExit(1)


if result.error is None:

    print()
    print("PASS: No generation error.")

else:

    print()
    print("FAIL:", result.error)

    raise SystemExit(1)


# ============================================================
# TEST 2 — Empty Result
# ============================================================

print()
print("TEST 2 — Empty Result")
print()


execution_result = DatabaseExecutionResult(

    success=True,

    columns=[
        "department_name",
        "department_total_revenue"
    ],

    rows=[],

    row_count=0,

    truncated=False
)


result = generator.generate(

    query="Show revenue for Cardiology.",

    execution_result=execution_result
)


print("Result:")
print(result)


if not result.has_data:

    print()
    print("PASS: Empty result detected.")

else:

    print()
    print("FAIL: Empty result incorrectly marked as data.")

    raise SystemExit(1)


if result.answer:

    print()
    print("PASS: Empty-result response generated.")

else:

    print()
    print("FAIL: Empty-result response missing.")

    raise SystemExit(1)


# ============================================================
# TEST 3 — Database Execution Failure
# ============================================================

print()
print("TEST 3 — Database Execution Failure")
print()


execution_result = DatabaseExecutionResult(

    success=False,

    error="Database connection failed."
)


result = generator.generate(

    query="Show total revenue.",

    execution_result=execution_result
)


print("Result:")
print(result)


if not result.has_data:

    print()
    print("PASS: Database failure correctly handled.")

else:

    print()
    print("FAIL: Database failure marked as data.")

    raise SystemExit(1)


if result.error == "Database connection failed.":

    print()
    print("PASS: Database error preserved.")

else:

    print()
    print("FAIL: Database error was not preserved.")

    raise SystemExit(1)


# ============================================================
# TEST 4 — Truncated Result
# ============================================================

print()
print("TEST 4 — Truncated Result")
print()


execution_result = DatabaseExecutionResult(

    success=True,

    columns=[
        "department_name",
        "department_total_revenue"
    ],

    rows=[
        {
            "department_name": "Emergency",
            "department_total_revenue": 100000
        },
        {
            "department_name": "ICU",
            "department_total_revenue": 90000
        }
    ],

    row_count=2,

    truncated=True
)


result = generator.generate(

    query="Show department revenue.",

    execution_result=execution_result
)


print("Result:")
print(result)


if result.truncated:

    print()
    print("PASS: Truncation state preserved.")

else:

    print()
    print("FAIL: Truncation state lost.")

    raise SystemExit(1)


# ============================================================
# TEST 5 — LLM Failure
# ============================================================

print()
print("TEST 5 — LLM Failure")
print()


class FailingLLM:

    def chat(
        self,
        system_prompt,
        user_prompt,
        temperature=0.1,
        max_tokens=1000
    ):

        raise RuntimeError(
            "Mock LLM failure."
        )


generator = InsightGenerator(
    llm_client=FailingLLM()
)


execution_result = DatabaseExecutionResult(

    success=True,

    columns=["department_name"],

    rows=[
        {
            "department_name": "Emergency"
        }
    ],

    row_count=1,

    truncated=False
)


result = generator.generate(

    query="Show departments.",

    execution_result=execution_result
)


print("Result:")
print(result)


if result.error == "Mock LLM failure.":

    print()
    print("PASS: LLM failure handled.")

else:

    print()
    print("FAIL: LLM failure not handled.")

    raise SystemExit(1)


# ============================================================
# COMPLETE
# ============================================================

print()
print("=" * 60)
print("PHASE 4.4 VALIDATION COMPLETE")
print("=" * 60)

print()
print("PASS: Successful insight generation")
print("PASS: Empty-result handling")
print("PASS: Database-error handling")
print("PASS: Truncation propagation")
print("PASS: LLM-error handling")
print()
print("PHASE 4.4 COMPLETE")
print()