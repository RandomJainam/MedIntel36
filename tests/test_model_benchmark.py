import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")

MODELS = [
    "minimax/minimax-m3:free",
    "inclusionai/ling-3.0-flash-fin:free",
    "liquid/lfm-2.5-2.6b:free",
]


SYSTEM_PROMPT = """
You are the Insight Generator for MedIntel360.

You analyze structured database results for hospital
and healthcare decision-makers.

STRICT RULES:

1. Use ONLY the supplied data.
2. Never invent missing information.
3. Never infer patient volume from revenue.
4. Never infer profitability from revenue.
5. Never infer clinical quality from revenue.
6. Perform numerical calculations carefully.
7. If a requested conclusion cannot be established
   from the supplied data, explicitly say so.
8. Challenge unsupported assumptions in the question.
9. Distinguish facts from interpretation.
10. Do not use outside knowledge or statistics.
11. Do not manufacture values for missing metrics.
12. Keep the final response concise but complete.

The database result is the source of truth.
"""


USER_PROMPT = """
TEST 8 — ADVERSARIAL ANALYTICAL REASONING

Analyze the following hospital department data.

DATABASE RESULTS:

Department | Total Revenue | Patient Count

Emergency | 900,000 | 300
ICU | 600,000 | 100
Internal Medicine | 800,000 | 400
Orthopedics | 700,000 | 200
Pediatrics | 500,000 | 500
Surgery | 1,000,000 | 250


Answer the following:

1. Which department generated the highest revenue?

2. Which department generated the lowest revenue?

3. What is the absolute revenue difference between
   the highest and lowest departments?

4. What percentage higher is the highest-revenue
   department than the lowest-revenue department?

5. Which department had the highest patient volume?

6. Which department generated the highest revenue
   per patient?

7. What is the total revenue across all departments?

8. What percentage of total revenue came from Surgery?

9. The hospital manager says:
   "Surgery is clearly the most efficient department
   because it has the highest revenue."

   Is this conclusion supported by the data?
   Explain briefly.

10. The hospital manager then says:
    "Pediatrics must be the least profitable department
    because it has the lowest revenue."

    Is this conclusion supported by the data?
    Explain briefly.

11. Give ONE concise decision-useful insight that is
    supported by the supplied data.

IMPORTANT:

Revenue is NOT the same as profit.

Revenue is NOT the same as efficiency.

Do not claim profitability unless profitability data
is explicitly supplied.

Return exactly this structure:

Highest revenue department:
Highest revenue:
Lowest revenue department:
Lowest revenue:
Revenue difference:
Percentage higher:
Highest patient volume:
Highest revenue per patient:
Total revenue:
Surgery percentage of total:
Surgery efficiency claim:
Pediatrics profitability claim:
Decision-useful insight:

Show calculations for the numerical answers.

Do not add unsupported conclusions.
"""


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "MedIntel360 Test 8"
}


results = []


print("=" * 100)
print("MEDINTEL360 — TEST 8")
print("ADVERSARIAL ANALYTICAL REASONING BENCHMARK")
print("=" * 100)


for model in MODELS:

    print("\n")
    print("-" * 100)
    print("MODEL:", model)
    print("-" * 100)

    payload = {
        "model": model,

        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_PROMPT
            }
        ],

        "temperature": 0,

        "max_tokens": 1000
    }

    start = time.time()

    try:

        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            json=payload,
            timeout=180
        )

        elapsed = round(
            time.time() - start,
            2
        )

        print("STATUS:", response.status_code)
        print("TIME:", elapsed, "seconds")

        data = response.json()

        # --------------------------------------------------
        # API ERROR
        # --------------------------------------------------

        if response.status_code != 200:

            error_data = data.get(
                "error",
                {}
            )

            error_message = error_data.get(
                "message",
                str(data)
            )

            print("ERROR:", error_message)

            results.append({
                "model": model,
                "time": elapsed,
                "status": response.status_code,
                "finish": "ERROR",
                "answer": "",
                "error": error_message
            })

            continue


        # --------------------------------------------------
        # RESPONSE
        # --------------------------------------------------

        choice = data["choices"][0]

        message = choice["message"]

        answer = message.get("content")

        finish_reason = choice.get(
            "finish_reason"
        )

        print("FINISH:", finish_reason)

        print("\nANSWER:")

        if answer:
            print(answer)
        else:
            print("[NO CONTENT RETURNED]")


        results.append({
            "model": model,
            "time": elapsed,
            "status": response.status_code,
            "finish": finish_reason,
            "answer": answer or "",
            "error": ""
        })


    except Exception as error:

        elapsed = round(
            time.time() - start,
            2
        )

        print("EXCEPTION:", str(error))

        results.append({
            "model": model,
            "time": elapsed,
            "status": "EXCEPTION",
            "finish": "ERROR",
            "answer": "",
            "error": str(error)
        })


# ==========================================================
# EXPECTED ANSWERS
# ==========================================================

print("\n")
print("=" * 100)
print("EXPECTED VALUES")
print("=" * 100)


revenues = {
    "Emergency": 900_000,
    "ICU": 600_000,
    "Internal Medicine": 800_000,
    "Orthopedics": 700_000,
    "Pediatrics": 500_000,
    "Surgery": 1_000_000
}


patients = {
    "Emergency": 300,
    "ICU": 100,
    "Internal Medicine": 400,
    "Orthopedics": 200,
    "Pediatrics": 500,
    "Surgery": 250
}


total_revenue = sum(
    revenues.values()
)


highest_revenue = max(
    revenues.values()
)


lowest_revenue = min(
    revenues.values()
)


highest_department = max(
    revenues,
    key=revenues.get
)


lowest_department = min(
    revenues,
    key=revenues.get
)


revenue_difference = (
    highest_revenue
    - lowest_revenue
)


percentage_higher = (
    revenue_difference
    / lowest_revenue
) * 100


highest_patient_department = max(
    patients,
    key=patients.get
)


revenue_per_patient = {
    department:
        revenues[department] / patients[department]

    for department in revenues
}


highest_revenue_per_patient_department = max(
    revenue_per_patient,
    key=revenue_per_patient.get
)


surgery_percentage = (
    revenues["Surgery"]
    / total_revenue
) * 100


print(
    "Highest revenue department:",
    highest_department
)

print(
    "Highest revenue:",
    highest_revenue
)

print(
    "Lowest revenue department:",
    lowest_department
)

print(
    "Lowest revenue:",
    lowest_revenue
)

print(
    "Revenue difference:",
    revenue_difference
)

print(
    "Percentage higher:",
    round(percentage_higher, 2),
    "%"
)

print(
    "Highest patient volume:",
    highest_patient_department
)

print(
    "Highest revenue per patient:",
    highest_revenue_per_patient_department
)

print(
    "Total revenue:",
    total_revenue
)

print(
    "Surgery percentage:",
    round(surgery_percentage, 2),
    "%"
)


# ==========================================================
# COMPARISON TABLE
# ==========================================================

print("\n")
print("=" * 120)
print("TEST 8 — MODEL COMPARISON")
print("=" * 120)

print(
    f"{'MODEL':45} "
    f"{'TIME':>10} "
    f"{'STATUS':>10} "
    f"{'FINISH':>12} "
    f"{'CONTENT':>12}"
)

print("-" * 120)


for result in results:

    content_status = (
        "YES"
        if result["answer"]
        else "NO"
    )

    print(
        f"{result['model'][:45]:45} "
        f"{result['time']:>9.2f}s "
        f"{str(result['status']):>10} "
        f"{str(result['finish']):>12} "
        f"{content_status:>12}"
    )


# ==========================================================
# FULL ANSWERS
# ==========================================================

print("\n")
print("=" * 120)
print("FULL MODEL RESPONSES")
print("=" * 120)


for result in results:

    print("\n")
    print("-" * 120)
    print(result["model"])
    print("-" * 120)

    if result["error"]:

        print("ERROR:")
        print(result["error"])

    else:

        print(
            result["answer"]
            if result["answer"]
            else "[NO CONTENT RETURNED]"
        )


print("\n")
print("=" * 100)
print("TEST 8 COMPLETE")
print("=" * 100)