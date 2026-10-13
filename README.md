# COMP 4111 Assignment 2: Rule-Based CDSS

Educational Python implementation. No external packages are required.
The rules are assignment examples, not clinical diagnostic guidelines.

## Run

```console
python cdss.py
python cdss.py --examples-only
python cdss.py --extended
python -m unittest -v
```

The default run displays P1-P5 with the original eight rules, repeats them
with three additional rules, then requests a new patient's symptoms.
Interactive input uses the original rules unless `--extended` is supplied.

## How it works

1. `BASE_RULES` is the knowledge base. Each dictionary stores a rule ID,
   required symptoms or an exact symptom count, conclusion, and priority.
2. `infer()` copies patient facts into working memory and loops through rules.
3. `all()` evaluates AND conditions; a count condition implements R7 and R8.
4. Every matching rule is retained. The maximum priority determines the final
   risk, so P1 retains R1 and R6 while its final assessment is HIGH RISK.
5. Explanations use matched rule IDs and symptom descriptions dynamically.

Some combinations of two or more symptoms match no original rule. These return
UNDETERMINED rather than inventing a low-risk conclusion.

## Expected original results

| Patient | Fired rules | Final risk |
| --- | --- | --- |
| P1 | R1, R6 | HIGH RISK |
| P2 | R4 | MODERATE RISK |
| P3 | R5 | MODERATE RISK |
| P4 | R7 | LOW RISK |
| P5 | R8 | LOW RISK |

## Proposed additional rules

- R9: Fatigue AND blurred vision -> HIGH RISK.
- R10: Hunger AND irritability -> MODERATE RISK.
- R11: Weight loss AND infection -> MODERATE RISK.

These are invented educational extensions. R9 deliberately creates a conflict
with R4 to demonstrate extensibility: P2 changes to HIGH RISK, and both rules
are reported. P1, P3, P4, and P5 keep their original final assessments.
Adding these rules requires no changes to `infer()`.

## Submission still to prepare

- Review the implementation and choose your additional educational rules.
- Rename `cdss.py` to your first-name-A2.py for submission.
- Prepare `4111-FA-A2-[STUDENT-FIRST-NAME].pdf` in the required deliverable order:
  code sections, P1-P5 screenshots and explanations, interactive example,
  conflict resolution, and the three additional rules with screenshots.
- Include your name and an accurate AI disclaimer at the beginning. This
  initial code and guide were generated with Codex; describe the actual
  assistance and your own subsequent contributions accurately.

## GitHub

Proposed repository: `ImmanueL4oo/comp4111-assignment2`.
Use a private repository unless you deliberately choose public visibility.
Do not include the instructor's assignment PDF in the repository.
