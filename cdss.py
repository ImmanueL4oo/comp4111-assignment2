"""Educational rule-based CDSS for COMP 4111 Assignment 2.

AI assistance: This initial implementation was generated with Codex.
Review, understand, and describe your actual use of AI in your submission.
These simplified assignment rules are not medical advice.
"""

import argparse


SYMPTOMS = {
    "thirst": "Increased thirst/frequent urination",
    "hunger": "Extreme hunger",
    "weight_loss": "Unintended weight loss",
    "fatigue": "Persistent fatigue",
    "blurred_vision": "Blurred vision",
    "irritability": "Increased irritability",
    "infection": "Slow-healing sores/frequent infections",
}
PRIORITIES = {"LOW RISK": 1, "MODERATE RISK": 2, "HIGH RISK": 3}


# KNOWLEDGE BASE: rule data is separate from the evaluation algorithm.
def make_rule(rule_id, risk, symptoms=(), count=None):
    return {
        "id": rule_id,
        "conditions": tuple(symptoms),
        "symptom_count": count,
        "conclusion": risk,
        "priority": PRIORITIES[risk],
    }


BASE_RULES = [
    make_rule("R1", "HIGH RISK", ("thirst", "weight_loss", "fatigue")),
    make_rule("R2", "HIGH RISK", ("thirst", "hunger", "fatigue")),
    make_rule("R3", "HIGH RISK", ("hunger", "blurred_vision", "infection")),
    make_rule("R4", "MODERATE RISK", ("fatigue", "blurred_vision")),
    make_rule("R5", "MODERATE RISK", ("thirst", "infection")),
    make_rule("R6", "MODERATE RISK", ("weight_loss", "fatigue")),
    make_rule("R7", "LOW RISK", count=1),
    make_rule("R8", "LOW RISK", count=0),
]

# Proposed educational extensions, not clinical diagnostic guidelines.
ADDITIONAL_RULES = [
    make_rule("R9", "HIGH RISK", ("fatigue", "blurred_vision")),
    make_rule("R10", "MODERATE RISK", ("hunger", "irritability")),
    make_rule("R11", "MODERATE RISK", ("weight_loss", "infection")),
]


# INFERENCE ENGINE: the same algorithm evaluates both rule sets.
def infer(patient_id, facts, rules):
    if set(facts) != set(SYMPTOMS):
        raise ValueError("Provide exactly the seven supported symptom attributes.")
    if any(type(value) is not bool for value in facts.values()):
        raise ValueError("Every symptom must be True or False.")
    working_memory = dict(facts)
    symptom_count = sum(working_memory.values())
    fired = []
    for rule in rules:
        conditions_match = all(working_memory[key] for key in rule["conditions"])
        count_matches = (
            rule["symptom_count"] is None
            or symptom_count == rule["symptom_count"]
        )
        if conditions_match and count_matches:
            fired.append(rule)
    highest_priority = max((rule["priority"] for rule in fired), default=None)
    winners = [rule for rule in fired if rule["priority"] == highest_priority]
    risk = winners[0]["conclusion"] if winners else "UNDETERMINED"
    explanations = []
    for rule in fired:
        if rule["symptom_count"] is not None:
            evidence = f"exactly {symptom_count} symptom(s) are present"
        else:
            evidence = " AND ".join(SYMPTOMS[key] for key in rule["conditions"])
        explanations.append(f"{rule['id']} fired because {evidence}; it concludes {rule['conclusion']}.")
    if fired:
        explanations.append(
            "Highest-priority matching rule(s): "
            + ", ".join(rule["id"] for rule in winners)
            + ". Priority order: HIGH RISK > MODERATE RISK > LOW RISK."
        )
    else:
        explanations.append("No rule matched these facts. The knowledge base provides no assessment for this combination.")
    return {
        "patient_id": patient_id,
        "facts": working_memory,
        "evaluated": len(rules),
        "fired": fired,
        "risk": risk,
        "recommendation": f"Educational rule-based assessment: {risk}.",
        "explanation": "\n".join(explanations),
    }


def show_result(result):
    print(f"\nPatient ID: {result['patient_id']}")
    for key, label in SYMPTOMS.items():
        print(f"  {label}: {result['facts'][key]}")
    print(f"Rules Evaluated: {result['evaluated']}")
    print("Rules Fired: " + (", ".join(rule["id"] for rule in result["fired"]) or "None"))
    for rule in result["fired"]:
        print(f"  {rule['id']}: {rule['conclusion']}")
    print(f"Final Risk Level: {result['risk']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Explanation:\n{result['explanation']}")


TEST_PATIENTS = {
    "P1": (True, False, True, True, False, False, False),
    "P2": (False, False, False, True, True, False, False),
    "P3": (True, False, False, False, False, False, True),
    "P4": (False, True, False, False, False, False, False),
    "P5": (False, False, False, False, False, False, False),
}


def run_examples():
    print("CLINICAL DECISION SUPPORT SYSTEM - educational assignment")
    print("\nORIGINAL KNOWLEDGE BASE")
    original_results = {}
    for patient_id, values in TEST_PATIENTS.items():
        facts = dict(zip(SYMPTOMS, values))
        original_results[patient_id] = infer(patient_id, facts, BASE_RULES)
        show_result(original_results[patient_id])
    print("\nEXTENDED KNOWLEDGE BASE")
    for patient_id, original in original_results.items():
        extended = infer(patient_id, original["facts"], BASE_RULES + ADDITIONAL_RULES)
        show_result(extended)
        print(f"Comparison: {original['risk']} -> {extended['risk']}")


def read_patient():
    patient_id = input("\nNew patient ID: ").strip() or "UserPatient"
    facts = {}
    for key, label in SYMPTOMS.items():
        while True:
            response = input(f"{label}? (Y/N): ").strip().lower()
            if response in ("y", "yes", "n", "no"):
                facts[key] = response in ("y", "yes")
                break
            print("Please enter Y or N.")
    return patient_id, facts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples-only", action="store_true", help="Run P1-P5 without prompting.")
    parser.add_argument("--extended", action="store_true", help="Use additional rules for interactive input.")
    args = parser.parse_args()
    run_examples()
    if not args.examples_only:
        patient_id, facts = read_patient()
        rules = BASE_RULES + ADDITIONAL_RULES if args.extended else BASE_RULES
        show_result(infer(patient_id, facts, rules))


if __name__ == "__main__":
    main()
