from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def strip_json_fences(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return text


SCORING_PROMPT = """You are evaluating a candidate's resume against job requirements, for a recruiter to review — not to make a final decision.

Job requirements:
{criteria}

Resume text:
---
{resume_text}
---

For EACH must-have requirement listed above, decide its status:
- "MET" — the resume clearly demonstrates this
- "MISSING" — the resume clearly does not have this
- "INSUFFICIENT EVIDENCE" — you cannot tell from this resume either way

For "MET" or "INSUFFICIENT EVIDENCE" with partial signal, quote the exact resume text you're basing this on. Do NOT invent or infer evidence that isn't actually written in the resume.

Return ONLY a JSON object with this exact shape, no other text, no markdown fences:

{{
  "overall_score": <integer 0-100>,
  "requirements": [
    {{"requirement": "the requirement text", "status": "MET or MISSING or INSUFFICIENT EVIDENCE", "evidence": "exact quoted resume text, or empty string"}}
  ]
}}

Return only the JSON object."""

def score_resume(resume_text, criteria):
    criteria_text = json.dumps(criteria)

    prompt = SCORING_PROMPT.format(
        criteria=criteria_text,
        resume_text=resume_text
    )

    for attempt in range(2):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            raw_text = response.content[0].text
            cleaned = strip_json_fences(raw_text)
            data = json.loads(cleaned)
            return True, data

        except json.JSONDecodeError:
            if attempt == 0:
                prompt = prompt + "\n\nReminder: respond with ONLY the JSON object, nothing else."
                continue
            return False, "Failed to parse scoring JSON after retry."

    return False, "Unknown failure."