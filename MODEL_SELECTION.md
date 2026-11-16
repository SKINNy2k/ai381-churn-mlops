# Model selection

Fill this in after you have trained your candidates in MLflow. Short sentences are fine. Use numbers from your runs.

## The question
What does this model decide, and who is hurt by a wrong answer? (One or two sentences.)
This model decides whether a telecom customer will churn. A false negative hurts the company by missing a departing customer, while a false positive wastes retention budget on a loyal customer.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| logreg | Baseline linear model for speed and simplicity | 0.495[cite: 1, 3] | 0.543[cite: 1, 3] | 0.250[cite: 1, 3] | 2.959[cite: 1, 3] | 3.548[cite: 1, 3] | e5bfa86e42ea45bf99d49f73a1bf49f[cite: 3] |
| random_forest | Non-linear ensemble to capture feature interactions | 0.454[cite: 1, 3] | 0.494[cite: 1, 3] | 0.222[cite: 1, 3] | 13.81[cite: 1, 3] | 3160.1[cite: 1, 3] | 2acf90cda2ec4c6d981dc8c1a44873[cite: 3] |
| gradient_boosting | Boosting algorithm for higher tabular predictive power | 0.417[cite: 1, 3] | 0.436[cite: 1, 3] | 0.222[cite: 1, 3] | 3.18[cite: 1, 3] | 141.6[cite: 1, 3] | 826d7a8f25b843f8966b539451e8a57f[cite: 3] |

## The champion
Which one did I pick, and what decided it? (Name the numbers that mattered and the ones I accepted losing.)
I picked **logreg**. It was decided by having the highest overall F1 score (0.543)[cite: 1, 3], the fastest p95 latency (2.959 ms)[cite: 1, 3], and the smallest model size (3.548 KB)[cite: 1, 3]. I accepted having a lower month-to-month slice F1 (0.250)[cite: 1, 3] compared to gradient boosting's month-to-month slice F1 (0.444)[cite: 1, 3], prioritizing overall performance and latency bounds instead.

## My promotion rules
- Latency budget (p95): 5 ms, because real-time inference requires sub-5ms response times.
- Minimum gain to replace the champion (F1 points): 0.05, because any new model must substantially improve overall F1 (evaluated as an absolute delta) to justify larger size and latency.

## What I would check next
One thing that could make this choice wrong in production (for example a slice with few customers, or data that changes):
All candidates have an AUC below 0.50 (0.495 for logreg)[cite: 1, 3], indicating weak probability ranking across thresholds; I would investigate label encoding, feature leakage, or class imbalance alongside monitoring drift on minority contract slices (such as month-to-month and two-year contracts)[cite: 1].