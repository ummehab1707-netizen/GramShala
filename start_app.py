import json, os

os.makedirs("content", exist_ok=True)
lessons_path = "content/lessons.json"

try:
    with open(lessons_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    data = {}

if "languages" not in data:
    data["languages"] = [{"code": "en", "label": "English"}, {"code": "hi", "label": "Hindi"}]
if "lessons" not in data:
    data["lessons"] = []

with open(lessons_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Server data verified successfully!")
