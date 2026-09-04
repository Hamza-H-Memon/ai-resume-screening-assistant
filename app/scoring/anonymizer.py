import re

EMAIL_PATTERN = re.compile(r"[\w.-]+@[\w.-]+\.\w+")
PHONE_PATTERN = re.compile(r"\+?\d[\d\-\s()]{7,}\d")
NAME_LINE_PATTERN = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,2}$")


def anonymize_text(text):
    text = EMAIL_PATTERN.sub("[EMAIL REDACTED]", text)
    text = PHONE_PATTERN.sub("[PHONE REDACTED]", text)

    lines = text.split("\n")
    for i in range(1):
        if i < len(lines) and NAME_LINE_PATTERN.match(lines[i].strip()):
            lines[i] = "[NAME REDACTED]"

    return "\n".join(lines)
