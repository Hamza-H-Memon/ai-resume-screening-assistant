# AI Resume Screening Assistant

A recruiter pastes a job description, uploads a batch of resumes, and gets back a ranked shortlist with match scores and evidence-grounded explanations for each candidate with an optional anonymization toggle to test for bias in scoring.

Built as a hands-on learning project and portfolio piece, from scratch, with a focus on explainability, honest evaluation, and responsible AI design, not just wiring up an LLM call.

## What this is (and isn't)

This is a **decision-support tool for recruiters, not an automated hiring system.** It never rejects a candidate, it surfaces evidence-grounded scores and explanations so a human can review, compare, and decide. Every score comes with the specific resume text it's based on, and the system is explicitly designed to say "insufficient evidence" rather than guess when a resume doesn't clearly support a judgment either way.

## How it works

1. **Parse** - extract raw text from PDF/DOCX resumes (`app/parsing/`)
2. **Extract criteria** - Claude reads the job description and returns structured must-have / nice-to-have / experience / education requirements (`app/scoring/criteria_extraction.py`)
3. **Score** - each resume is scored 0–100 against those criteria. For every requirement, the system returns a status (`MET` / `MISSING` / `INSUFFICIENT EVIDENCE`) and the exact resume text it's grounded in the model is instructed not to invent evidence (`app/scoring/scorer.py`)
4. **Anonymize (optional)** - name, email, phone, and institution are redacted before scoring, so results can be compared with and without identifying details (`app/scoring/anonymizer.py`)
5. **Serve** - a FastAPI backend (`app/api/main.py`) with endpoints for JD parsing, resume parsing, and batch scoring, plus a Streamlit UI (`app/ui/main.py`) for the actual recruiter-facing experience

## Tech stack

| Layer | Tool |
|---|---|
| Backend/API | FastAPI |
| Resume parsing | pdfplumber, python-docx |
| Scoring/rationale | Claude API (Anthropic) |
| Frontend | Streamlit |

## Running locally

```bash
git clone https://github.com/Hamza-H-Memon/AIResumeScreener.git
cd AIResumeScreener

python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

Create a `.env` file in the project root with your own Anthropic API key (free to start at console.anthropic.com):

```
ANTHROPIC_API_KEY=your-key-here
```

**Run the UI:**
```bash
streamlit run app/ui/main.py
```

**Run the API standalone** (auto-generated docs at `/docs`):
```bash
uvicorn app.api.main:app --reload
```

## Evaluation

This project includes a real evaluation, not just a working demo:

- `evaluate.py` - runs every sample resume against every sample job description and prints ranked results, used to calculate a recruiter-agreement rate (manually comparing AI rankings against my own judgment)
- `bias_audit.py` - a controlled-pair bias test: two resumes with byte-identical content except a name, scored both with and without anonymization

Full findings — including a genuine recruiter-agreement percentage, three documented failure cases (score non-determinism, an intermittent JSON parsing failure, and a status-granularity limitation that caused an incorrect tie), and an honest discussion of what a single-run bias test can and can't prove are in [`docs/case_study.md`](docs/case_study.md).

## Known limitations

- PDF parsing struggles with heavily columned/multi-section resume layouts. Text can interleave between columns.
- Scanned/image-only PDFs have no extractable text layer and are flagged rather than silently scored as empty.
- Anonymization is regex/heuristic-based (pattern matching on the first line, email/phone formats, institution keywords), not a trained NER model, it can produce false positives (e.g. briefly matching a job title as a name) and will miss identity signals in less common resume layouts.
- Scoring is LLM-based and not perfectly deterministic, the same resume scored twice can return slightly different scores. This is documented and discussed in the case study, including why it matters specifically for bias-audit comparisons.

## Project structure

```
app/
  parsing/    resume + JD text extraction
  scoring/    criteria extraction, scoring, anonymization
  api/        FastAPI routes
  ui/         Streamlit app
data/
  sample_resumes/   test resumes (not real people's data)
  sample_jds/       test job descriptions
docs/
  case_study.md     full write-up: approach, tradeoffs, metrics, failure cases
evaluate.py         multi-JD, multi-resume evaluation script
bias_audit.py       controlled-pair bias audit script
```
