import re

html_path = "static/index.html"

try:
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace user facingMode or default camera selection with environment (back camera)
    content = re.sub(
        r'facingMode:\s*["\']user["\']',
        'facingMode: "environment"',
        content
    )
    content = re.sub(
        r'facingMode:\s*\{[^\}]*\}',
        'facingMode: "environment"',
        content
    )

    # Ensure html5QrCode.start requests back camera
    if 'facingMode' not in content:
        content = content.replace(
            'Html5Qrcode.getCameras()',
            '// Using back camera default'
        )
        content = re.sub(
            r'(\.start\(\s*)\{([^\}]*)\}',
            r'\1{ facingMode: "environment" }',
            content
        )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Successfully configured scanner to use the back camera!")
except Exception as e:
    print(f"Error updating file: {e}")
