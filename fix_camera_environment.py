import re

html_path = "static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace device ID camera selection or facingMode with explicit environment facingMode constraint
pattern = r'html5QrCode\.start\s*\(\s*([^,]+),'
replacement = r'html5QrCode.start({ facingMode: "environment" },'

if re.search(pattern, content):
    new_content = re.sub(pattern, replacement, content)
else:
    # General replacement if pattern differs
    new_content = content.replace('facingMode: "user"', 'facingMode: "environment"')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✅ Updated scanner configuration to enforce rear camera!")
