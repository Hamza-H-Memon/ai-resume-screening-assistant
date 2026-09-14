# Case Study: AI Resume Screening Assistant

## Problem

Recruiters manually screening large resume batches face two problems: it's slow, and it's inconsistent, screener fatigue and unconscious bias can affect who gets a second look. This tool speeds up the first pass and makes the reasoning behind each score visible and auditable, with an anonymization toggle so results can be compared with and without identifying details.

## Approach

I chose an LLM-based scoring approach (Claude) over a hybrid deterministic system (keyword matching + TF-IDF/BM25 + embeddings) after weighing the two directly. A hybrid system is more defensible in theory reproducible scores, no LLM non-determinism, but building and properly evaluating it (baseline comparisons, ranking metrics like NDCG/MRR) was a significantly larger project than the timeline justified for a first portfolio piece. I chose to be honest about this tradeoff rather than overbuild: the LLM-only approach is simpler to implement and reason about, at the cost of the non-determinism documented in Failure Cases below.

I structured scoring around evidence-grounded status categories (MET / MISSING / INSUFFICIENT EVIDENCE) instead of a single free-text rationale, specifically to reduce hallucination risk the prompt requires the model to quote resume text for any "MET" judgment, rather than generating a plausible-sounding paragraph disconnected from the actual resume content. This was a direct response to the most common failure mode in AI screening tools: confident-sounding explanations that aren't actually tied to real evidence.

The anonymization toggle was built specifically to enable a bias-audit comparison, not as a checkbox feature, it lets the same resume be scored with and without identifying details (name, email, phone, institution), which is what made the controlled-pair testing in Phase 7 possible. I used a regex/heuristic approach rather than a trained NER model, since a heuristic is transparent and explainable (I can point to exactly which pattern matched), even though it's less robust the false positive I found during testing (a job title "Amazon Associate" briefly matching the name pattern) is a direct, honest consequence of that choice, and worth being upfront about rather than claiming the anonymizer is more reliable than it is.

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

With more time, the most valuable next step would be finer-grained evidence scoring, moving from a three-way status (MET / MISSING / INSUFFICIENT EVIDENCE) to something like a 0-3 evidence-strength scale per requirement. The Phase 7 evaluation showed this three-way system genuinely collapses meaningful differences (e.g. "partial evidence" vs "no evidence at all") into the same bucket, which directly caused an incorrect tie between two candidates in testing.

I'd also address the score non-determinism found during testing the same resume scored twice, unchanged, returned different scores in separate runs. A straightforward fix would be averaging multiple scoring calls per candidate rather than trusting a single call, at the cost of extra API spend and latency. This matters most for the bias-audit use case specifically, since single-run comparisons currently can't cleanly separate a real bias effect from ordinary model variance.

Given more time, I'd replace the regex-based anonymizer with a real NER (Named Entity Recognition) model, which would handle the job-title-vs-name ambiguity that the current heuristic gets wrong, and would generalize better across resume formats that don't put the name on line one.

Finally, I'd build a proper evaluation harness with a larger, more deliberately constructed labelled dataset (more resumes, more JDs, ideally a second human rater to check inter-rater agreement) rather than the smaller manual review done in Phase 7 the current evaluation is real and honest, but a larger sample would make the recruiter-agreement percentage more statistically meaningful.