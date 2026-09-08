"""
============================================================
MedIntel360
LLM Output Guardrail Tests
============================================================
"""

from ai_engine.llm_output_guardrail import (
    LLMOutputGuardrail
)


# ============================================================
# Mock Schema Manager
# ============================================================

class MockSchemaManager:

    def get_dataset_names(self):

        return [
            "finance",
            "clinical"
        ]

    def get_metrics(self, dataset):

        if dataset == "finance":

            return [
                {
                    "name": "department_total_revenue"
                },
                {
                    "name": "total_revenue"
                }
            ]

        if dataset == "clinical":

            return [
                {
                    "name": "patient_count"
                }
            ]

        return []

    def get_dimensions(self, dataset):

        if dataset == "finance":

            return [
                {
                    "name": "department_name"
                },
                {
                    "name": "region"
                }
            ]

        if dataset == "clinical":

            return [
                {
                    "name": "department_name"
                }
            ]

        return []


# ============================================================
# Test Helper
# ============================================================

def run_test(
    name,
    data,
    expected
):

    guardrail = LLMOutputGuardrail()

    schema = MockSchemaManager()

    result = guardrail.validate(
        data,
        schema
    )

    passed = (
        result["valid"] == expected
    )

    print(
        f"{'PASS' if passed else 'FAIL'}: "
        f"{name}"
    )

    if not passed:

        print(
            "Result:",
            result
        )

    return passed


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 70)
    print("MEDINTEL360 — PHASE 4.8")
    print("LLM OUTPUT GUARDRAIL TEST")
    print("=" * 70)

    results = []

    # --------------------------------------------------------
    # 1. Valid output
    # --------------------------------------------------------

    results.append(
        run_test(
            "Valid LLM output",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.95,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": [],
                "requires_clarification": False,
                "clarification_question": None
            },
            True
        )
    )

    # --------------------------------------------------------
    # 2. Invalid dataset
    # --------------------------------------------------------

    results.append(
        run_test(
            "Invalid dataset",
            {
                "selected_dataset": "fake_database",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 3. Invalid metric
    # --------------------------------------------------------

    results.append(
        run_test(
            "Invalid metric",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "fake_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 4. Invalid dimension
    # --------------------------------------------------------

    results.append(
        run_test(
            "Invalid dimension",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "fake_department"
                ],
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 5. Invalid filter column
    # --------------------------------------------------------

    results.append(
        run_test(
            "Invalid filter column",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": [
                    {
                        "column": "password",
                        "operator": "=",
                        "value": "123"
                    }
                ]
            },
            False
        )
    )

    # --------------------------------------------------------
    # 6. Invalid filter operator
    # --------------------------------------------------------

    results.append(
        run_test(
            "Invalid filter operator",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": [
                    {
                        "column": "department_name",
                        "operator": "DROP",
                        "value": "Surgery"
                    }
                ]
            },
            False
        )
    )

    # --------------------------------------------------------
    # 7. Missing filter value
    # --------------------------------------------------------

    results.append(
        run_test(
            "Missing filter value",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": [
                    {
                        "column": "department_name",
                        "operator": "="
                    }
                ]
            },
            False
        )
    )

    # --------------------------------------------------------
    # 8. Invalid confidence
    # --------------------------------------------------------

    results.append(
        run_test(
            "Confidence outside valid range",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 5.0,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 9. Invalid metrics structure
    # --------------------------------------------------------

    results.append(
        run_test(
            "Metrics must be a list",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": "department_total_revenue",
                "dimensions": [
                    "department_name"
                ],
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 10. Invalid dimension structure
    # --------------------------------------------------------

    results.append(
        run_test(
            "Dimensions must be a list",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": "department_name",
                "filters": []
            },
            False
        )
    )

    # --------------------------------------------------------
    # 11. Invalid filter structure
    # --------------------------------------------------------

    results.append(
        run_test(
            "Filter must be an object",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.9,
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ],
                "filters": [
                    "department_name = Surgery"
                ]
            },
            False
        )
    )

    # --------------------------------------------------------
    # 12. Missing required field
    # --------------------------------------------------------

    results.append(
        run_test(
            "Missing required field",
            {
                "selected_dataset": "finance",
                "metrics": [
                    "department_total_revenue"
                ],
                "dimensions": [
                    "department_name"
                ]
            },
            False
        )
    )

    # --------------------------------------------------------
    # 13. Invalid clarification state
    # --------------------------------------------------------

    results.append(
        run_test(
            "Clarification without question",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.4,
                "metrics": [],
                "dimensions": [],
                "filters": [],
                "requires_clarification": True,
                "clarification_question": None
            },
            False
        )
    )

    # --------------------------------------------------------
    # 14. Valid clarification state
    # --------------------------------------------------------

    results.append(
        run_test(
            "Valid clarification state",
            {
                "selected_dataset": "finance",
                "dataset_confidence": 0.4,
                "metrics": [],
                "dimensions": [],
                "filters": [],
                "requires_clarification": True,
                "clarification_question":
                    "Which department would you like to analyze?"
            },
            True
        )
    )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("PHASE 4.8 VALIDATION")
    print("=" * 70)

    passed = sum(results)

    total = len(results)

    print(
        f"PASSED: {passed}/{total}"
    )

    if passed == total:

        print()
        print(
            "PHASE 4.8 LLM OUTPUT GUARDRAIL COMPLETE"
        )

    else:

        print()
        print(
            "PHASE 4.8 LLM OUTPUT GUARDRAIL FAILED"
        )


if __name__ == "__main__":

    main()