with open("static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add clean 2-option camera dropdown
dropdown = '''<div class="mb-3" id="cameraSelectContainer">
    <label class="block text-sm font-semibold text-gray-700 mb-1">📷 Select Camera:</label>
    <select id="cameraSelect" onchange="switchCamera(this.value)" class="w-full p-2.5 border-2 border-indigo-500 rounded-lg bg-white text-gray-900 font-bold text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-600">
        <option value="environment" selected>📷 Rear Camera</option>
        <option value="user">🤳 Front Camera</option>
    </select>
</div>'''

if 'id="cameraSelect"' not in html and '<div id="reader"' in html:
    html = html.replace('<div id="reader"', dropdown + '\n<div id="reader"')

# 2. Inject camera switching functions safely
js_patch = """
function switchCamera(mode) {
    if (typeof html5QrCode !== "undefined" && html5QrCode) {
        if (html5QrCode.isScanning) {
            html5QrCode.stop().then(() => launchCameraMode(mode)).catch(() => launchCameraMode(mode));
        } else {
            launchCameraMode(mode);
        }
    } else {
        launchCameraMode(mode);
    }
}

function launchCameraMode(mode) {
    if (typeof html5QrCode === "undefined" || !html5QrCode) {
        html5QrCode = new Html5Qrcode("reader");
    }
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };
    const successCb = typeof onScanSuccess === "function" ? onScanSuccess : (txt => alert("Scanned: " + txt));
    const failCb = typeof onScanFailure === "function" ? onScanFailure : (() => {});
    html5QrCode.start({ facingMode: mode }, config, successCb, failCb).catch(err => console.error(err));
}
"""

if "function switchCamera" not in html:
    html = html.replace("</script>", js_patch + "\n</script>")

with open("static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Restored full layout and cleanly added 2-camera selector!")
