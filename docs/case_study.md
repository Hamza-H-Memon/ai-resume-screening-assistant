# Case Study: AI Resume Screening Assistant

## Problem

Recruiters manually screening large resume batches face two problems: it's slow, and it's inconsistent, screener fatigue and unconscious bias can affect who gets a second look. This tool speeds up the first pass and makes the reasoning behind each score visible and auditable, with an anonymization toggle so results can be compared with and without identifying details.

## Approach

_To fill in during Phase 8: why Claude over a local embedding model, why evidence-grounded status categories, why an anonymization toggle specifically, what alternatives were considered and rejected._

## Tradeoffs

- Deliberately kept scoring LLM-based rather than building a hybrid deterministic/embedding matching system. The added complexity of TF-IDF/BM25/embeddings and a formal evaluation harness (Precision@K, NDCG, etc.) was judged too large for the project timeline versus the learning value.
- Anonymization is regex/heuristic based (name-line pattern, email/phone patterns, institution keywords), not a trained NER model, a known, accepted limitation given project scope.

## Metrics

- **Recruiter agreement rate:** For `sample_jd.txt` (generic Business Analyst), reviewed all 7 scored candidates. Agreed with the AI's relative placement for 5 of 7 (71%) — the top 3 tied candidates correctly ranked above the rest, and the bottom 2 (clearly unrelated roles) correctly ranked lowest. Disagreed on 1 point: the AI tied `business-intelligence-analyst` and `business-systems-analyst` at 75 each, but manual review of both resumes places the BI-flavored candidate clearly above the systems-flavored one for this generic BA role, the AI failed to differentiate two candidates a human reviewer could distinguish.
- **Parse success rate:** 7 of 7 sample resumes (PDF and DOCX) parsed successfully across testing.
- **Anonymized vs. non-anonymized score comparison:** Controlled name-swap pair (identical resume text, only candidate name changed) scored identically (85 vs 85) across two independent runs. However, per-requirement status judgments showed inconsistency between runs even on identical text, see Failure Cases below for why this makes the comparison inconclusive on its own.

## Failure Cases

1. **Score non-determinism:** The same resume, scored twice against the same criteria with zero input changes, returned different scores in separate runs (e.g. one resume scored 25 in one run, 35 in another). This means single-run score comparisons including bias-audit pair tests, cannot fully separate genuine bias effects from ordinary model variance without multiple repeated trials per case. A production system would need to either average multiple scoring calls per candidate or explicitly communicate this uncertainty to recruiters.

2. **Intermittent JSON parsing failure:** During evaluation, one scoring call failed even after the built-in retry (malformed JSON both times) confirmed across separate test runs. The failure is correctly caught and reported rather than silently defaulting to a wrong score, but it demonstrates that even well-prompted LLM calls have a non-zero failure rate that any production version of this tool would need to handle (e.g. a second automatic retry, or flagging the candidate for manual review instead of silently omitting them).

3. **Insufficient status granularity causing incorrect ties:** The scoring system's three-way status (MET / MISSING / INSUFFICIENT EVIDENCE) is too coarse to always produce correct rankings. For a generic Business Analyst JD, the system tied `business-intelligence-analyst` and `business-systems-analyst` at 75 each. A more detailed manual review distinguishing "partial evidence" from "weak/no evidence" per criterion showed the BSA candidate's client-facing evidence was meaningfully weaker than the BI candidate's, a real difference the three-status system collapsed into the same bucket. A future version could use a finer-grained scale (e.g. a 0-3 evidence-strength score per requirement) to avoid this.

## What I'd do differently

_To fill in during Phase 8: with more time/budget, what's next — e.g. finer-grained evidence scoring, real NER for anonymization, averaging multiple scoring calls to address non-determinism, a proper eval harness._