# SSC CGL — 500-Question Practice Sets

Hard, CGL-standard practice sets: **500 questions per topic**, all questions first, then **all answers + explanations at the end**. Difficulty skew **~20% Medium / 60% Hard / 20% Very-Hard (Tier-II trap level)**.

Every set is **machine-verified for zero answer errors** — Quant/Reasoning answers are *computed by a generator script* and then *independently re-solved by a separate verifier* that re-parses the rendered file. Curated sets (English/GA) are structurally verified and fact/grammar spot-checked.

## Completed (Priority Block — 13 topics · 6,500 questions)

| File | Topic | Verification |
|---|---|---|
| [Quant_01_Percentage_500.md](Quant_01_Percentage_500.md) | Percentage | PASS — 124 re-solved |
| [Quant_02_Ratio_Proportion_500.md](Quant_02_Ratio_Proportion_500.md) | Ratio & Proportion | PASS — 124 re-solved, 6 types |
| [Quant_03_Profit_Loss_500.md](Quant_03_Profit_Loss_500.md) | Profit & Loss + Discount | PASS — 117 re-solved |
| [Quant_04_Time_Work_500.md](Quant_04_Time_Work_500.md) | Time & Work + Pipes | PASS — 118 re-solved |
| [Quant_05_Time_Speed_Distance_500.md](Quant_05_Time_Speed_Distance_500.md) | TSD + Trains + Boats | PASS — 248 re-solved, 10 types |
| [Quant_06_Algebra_500.md](Quant_06_Algebra_500.md) | Algebra | PASS — 224 re-solved, 12 types |
| [Quant_07_Geometry_500.md](Quant_07_Geometry_500.md) | Geometry + Coordinate | PASS — 295 re-solved, 13 types |
| [Quant_08_Mensuration_500.md](Quant_08_Mensuration_500.md) | Mensuration 2D/3D | PASS — 324 re-solved, 23 types |
| [Quant_09_Data_Interpretation_500.md](Quant_09_Data_Interpretation_500.md) | Data Interpretation (100 sets) | PASS — 250 re-derived |
| [Reasoning_01_Coding_Decoding_500.md](Reasoning_01_Coding_Decoding_500.md) | Coding-Decoding | PASS — 210 re-derived, 13 types |
| [Reasoning_02_Syllogism_500.md](Reasoning_02_Syllogism_500.md) | Syllogism | PASS — all 500 re-solved (model-checker) |
| [English_01_Error_Spotting_500.md](English_01_Error_Spotting_500.md) | Error Spotting | PASS — grammar spot-checked |
| [GA_01_Polity_500.md](GA_01_Polity_500.md) | Polity & Constitution | PASS — facts spot-checked |

See [MASTER_CHECKLIST.md](MASTER_CHECKLIST.md) for the full plan and the remaining ~45 syllabus topics queued next.

## How these are built (repeatable process)
1. A Python generator in [_generators/](_generators/) computes each question's exact answer and builds 4 distinct options (1 correct + 3 common-mistake distractors), randomising the correct position.
2. The generator self-checks (500 unique, 4 distinct options, one correct) and writes the markdown.
3. A separate verifier re-parses the *written file* and independently re-solves a large sample, asserting the keyed option equals the computed answer. Only a `RESULT: PASS` with 0 mismatches counts as done.

To regenerate any set deterministically: `python _generators/gen_<topic>.py && python _generators/verify_<topic>.py`.
