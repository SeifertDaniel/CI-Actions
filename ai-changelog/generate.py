import os
import json
import urllib.request
from urllib.error import HTTPError

# ------------------------------------------------------------
# 1. Eingaben lesen und validieren
# ------------------------------------------------------------

RAW_CHANGELOG_FILE = "raw_commits.txt"

if not os.path.exists(RAW_CHANGELOG_FILE):
    raise RuntimeError("raw_commits.txt not found")

with open(RAW_CHANGELOG_FILE, "r", encoding="utf-8") as f:
    raw = f.read().strip()

if not raw:
    raise RuntimeError("raw_changelog.md is empty – no commits found between tags")

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is missing")

# Optional konfigurierbar (z. B. später als Action-Input)
model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# ------------------------------------------------------------
# 2. Prompt bauen
# ------------------------------------------------------------

prompt = f"""
You are generating a changelog entry following https://keepachangelog.com.

Rules:
- Audience: software developers
- Use sections: Added, Changed, Fixed, Removed
- Be concise and technical
- Group related changes
- Do NOT invent changes
- Output valid Markdown only
- Do NOT add explanations outside the changelog

Commit messages between the two releases:
{raw}
""".strip()

# ------------------------------------------------------------
# 3. OpenAI API Payload
# ------------------------------------------------------------

payload = {
    "model": model,
    "messages": [
        {
            "role": "system",
            "content": "You generate Keep a Changelog compliant release notes."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 1,
    "max_completion_tokens": 800
}

data = json.dumps(payload).encode("utf-8")

request = urllib.request.Request(
    url="https://api.openai.com/v1/chat/completions",
    data=data,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

print("=== OpenAI request debug ===")
print(f"Model: {model}")
print(f"Prompt length: {len(prompt)} characters")
print("Prompt preview:")
print(prompt[:500])
print("=== End prompt preview ===")

# ------------------------------------------------------------
# 4. Request ausführen + Fehler sauber ausgeben
# ------------------------------------------------------------

try:
    with urllib.request.urlopen(request) as response:
        status = response.status
        body = response.read().decode("utf-8")

        print("=== OpenAI response debug ===")
        print(f"HTTP status: {status}")
        print(body)
        print("=== End response debug ===")

        result = json.loads(body)
except HTTPError as e:
    print("❌ OpenAI API error")
    print(e.read().decode("utf-8"))
    raise

# ------------------------------------------------------------
# 5. Ergebnis ausgeben (STDOUT → Workflow kann es weiterverarbeiten)
# ------------------------------------------------------------

content = result["choices"][0]["message"]["content"].strip()
print(content)

if not content.strip():
    raise RuntimeError("AI returned empty changelog content")

with open("changelog_entry.md", "w", encoding="utf-8") as f:
    f.write(content)

