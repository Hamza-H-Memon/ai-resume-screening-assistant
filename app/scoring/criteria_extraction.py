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


def extract_criteria(jd_text):
    prompt = f"""You are extracting structured hiring criteria from a job description.

Return ONLY a JSON object with this exact shape, no other text, no markdown fences:

{{
  "must_have": ["skill or requirement", ...],
  "nice_to_have": ["skill or requirement", ...],
  "min_experience_years": <integer, use 0 if not specified>,
  "education_requirements": "string, empty string if not specified"
}}

Job description:
---
{jd_text}
---

Return only the JSON object."""

    for attempt in range(2):
        try:
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=500,
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
            return False, "Failed to parse criteria JSON after retry."

    return False, "Unknown failure."