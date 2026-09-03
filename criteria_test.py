from dotenv import load_dotenv
import os
import json
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with open("sample_jd.txt", "r", encoding="utf-8") as f:
    jd_text = f.read()

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

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=500,
    messages=[{"role": "user", "content": prompt}]
)


def strip_json_fences(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        lines = [line for line in lines if not line.strip().startswith("```")]
        text = "\n".join(lines).strip()
    return text


raw_text = response.content[0].text
cleaned = strip_json_fences(raw_text)
data = json.loads(cleaned)

print("Must have:", data["must_have"])
print("Nice to have:", data["nice_to_have"])
print("Min experience:", data["min_experience_years"])
print("Education:", data["education_requirements"])