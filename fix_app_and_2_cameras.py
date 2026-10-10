import re

html_path = "static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean 2-option Camera Select Dropdown HTML
dropdown_html = '''<div class="mb-3" id="cameraSelectContainer">
    <label class="block text-sm font-semibold text-gray-700 mb-1">📷 Select Camera:</label>
    <select id="cameraSelect" onchange="switchCamera(this.value)" class="w-full p-2.5 border-2 border-indigo-500 rounded-lg bg-white text-gray-900 font-bold text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-600">
        <option value="environment" selected>📷 Rear Camera</option>
        <option value="user">🤳 Front Camera</option>
    </select>
</div>'''

# Replace or insert dropdown cleanly above camera reader
if 'id="cameraSelectContainer"' in content:
    content = re.sub(r'<div class="mb-3" id="cameraSelectContainer">[\s\S]*?</div>', dropdown_html, content)
elif '<div id="reader"' in content:
    content = content.replace('<div id="reader"', dropdown_html + '\n<div id="reader"')

# 2. Direct, clean JS logic forcing browser-native Rear vs Front mode
js_code = """
let html5QrCode = null;

function startCameraStream() {
    if (!html5QrCode) {
        html5QrCode = new Html5Qrcode("reader");
    }

    const selectEl = document.getElementById("cameraSelect");
    const mode = selectEl ? selectEl.value : "environment";
    launchScanner({ facingMode: mode });
}

function switchCamera(selectedMode) {
    if (!html5QrCode) return;
    if (html5QrCode.isScanning) {
        html5QrCode.stop().then(() => {
            launchScanner({ facingMode: selectedMode });
        }).catch(() => launchScanner({ facingMode: selectedMode }));
    } else {
        launchScanner({ facingMode: selectedMode });
    }
}

function launchScanner(cameraConstraint) {
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };
    const successCb = typeof onScanSuccess === "function" ? onScanSuccess : (txt => alert("Scanned: " + txt));
    const failCb = typeof onScanFailure === "function" ? onScanFailure : (() => {});

    html5QrCode.start(cameraConstraint, config, successCb, failCb)
        .catch(err => console.error("Error launching camera:", err));
}
"""

if 'function startCameraStream' in content:
    content = re.sub(r'function startCameraStream\(\)[\s\S]*?\}\n\}', js_code, content)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Configured dropdown to exactly 2 camera options (Rear Camera & Front Camera)!")
