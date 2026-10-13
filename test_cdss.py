"""Check assignment examples, conflict handling, and uncovered inputs."""

import unittest
from itertools import product

from cdss import ADDITIONAL_RULES, BASE_RULES, SYMPTOMS, TEST_PATIENTS, infer


class InferenceTests(unittest.TestCase):
    def test_provided_patients(self):
        expected = {
            "P1": ("HIGH RISK", ["R1", "R6"]),
            "P2": ("MODERATE RISK", ["R4"]),
            "P3": ("MODERATE RISK", ["R5"]),
            "P4": ("LOW RISK", ["R7"]),
            "P5": ("LOW RISK", ["R8"]),
        }
        for patient_id, values in TEST_PATIENTS.items():
            with self.subTest(patient_id=patient_id):
                result = infer(patient_id, dict(zip(SYMPTOMS, values)), BASE_RULES)
                self.assertEqual(result["risk"], expected[patient_id][0])
                self.assertEqual([r["id"] for r in result["fired"]], expected[patient_id][1])

    def test_extensions_change_p2_only(self):
        changed = []
        for patient_id, values in TEST_PATIENTS.items():
            facts = dict(zip(SYMPTOMS, values))
            old = infer(patient_id, facts, BASE_RULES)
            new = infer(patient_id, facts, BASE_RULES + ADDITIONAL_RULES)
            if old["risk"] != new["risk"]:
                changed.append(patient_id)
        self.assertEqual(changed, ["P2"])

    def test_uncovered_combination_is_not_low_risk(self):
        facts = {key: key in ("hunger", "irritability") for key in SYMPTOMS}
        self.assertEqual(infer("Gap", facts, BASE_RULES)["risk"], "UNDETERMINED")

    def test_all_128_inputs_against_independent_rule_definition(self):
        for values in product((False, True), repeat=7):
            thirst, hunger, loss, fatigue, blurred, irritability, infection = values
            high = (thirst and loss and fatigue) or (thirst and hunger and fatigue) or (hunger and blurred and infection)
            moderate = (fatigue and blurred) or (thirst and infection) or (loss and fatigue)
            expected = "HIGH RISK" if high else "MODERATE RISK" if moderate else "LOW RISK" if sum(values) <= 1 else "UNDETERMINED"
            result = infer("AllInputs", dict(zip(SYMPTOMS, values)), BASE_RULES)
            self.assertEqual(result["risk"], expected)

    def test_reject_non_boolean_input(self):
        facts = dict.fromkeys(SYMPTOMS, False)
        facts["thirst"] = "False"
        with self.assertRaises(ValueError):
            infer("Invalid", facts, BASE_RULES)


if __name__ == "__main__":
    unittest.main()
