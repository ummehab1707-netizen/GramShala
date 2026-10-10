import re

html_path = "static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Insert Camera Selection Dropdown directly above the reader element if not present
dropdown_html = '''<div class="mb-3" id="cameraSelectContainer">
    <label class="block text-sm font-semibold text-gray-700 mb-1">📷 Select Camera:</label>
    <select id="cameraSelect" onchange="switchCamera(this.value)" class="w-full p-2.5 border-2 border-indigo-500 rounded-lg bg-white text-gray-900 font-bold text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-600">
        <option value="">Detecting phone cameras...</option>
    </select>
</div>'''

if 'id="cameraSelect"' not in content:
    content = content.replace('<div id="reader"', dropdown_html + '\n<div id="reader"')

# 2. Inject rock-solid Camera Dropdown & Rear Camera Auto-Select JS Logic
js_code = """
let html5QrCode = null;

function startCameraStream() {
    if (!html5QrCode) {
        html5QrCode = new Html5Qrcode("reader");
    }

    Html5Qrcode.getCameras().then(devices => {
        const selectEl = document.getElementById("cameraSelect");
        if (devices && devices.length > 0) {
            if (selectEl) {
                selectEl.innerHTML = "";
                devices.forEach((device, idx) => {
                    const opt = document.createElement("option");
                    opt.value = device.id;
                    opt.text = device.label || `Camera ${idx + 1}`;
                    selectEl.appendChild(opt);
                });
            }

            // Find camera with 'back', 'rear', 'environment', '0', or 'main' in label
            let backCam = devices.find(d => /back|rear|environment|main|0,/i.test(d.label));
            
            // If labels are generic (Camera 1, Camera 2), pick the LAST device in array (rear camera on Android)
            if (!backCam && devices.length > 1) {
                backCam = devices[devices.length - 1];
            }

            const chosenId = backCam ? backCam.id : devices[0].id;
            if (selectEl) selectEl.value = chosenId;

            launchScanner(chosenId);
        } else {
            launchScanner({ facingMode: "environment" });
        }
    }).catch(err => {
        console.warn("getCameras failed, attempting environment constraint:", err);
        launchScanner({ facingMode: "environment" });
    });
}

function switchCamera(selectedCameraId) {
    if (!html5QrCode) return;
    if (html5QrCode.isScanning) {
        html5QrCode.stop().then(() => {
            launchScanner(selectedCameraId);
        }).catch(() => launchScanner(selectedCameraId));
    } else {
        launchScanner(selectedCameraId);
    }
}

function launchScanner(cameraSource) {
    const config = { fps: 10, qrbox: { width: 250, height: 250 } };
    const successCb = typeof onScanSuccess === "function" ? onScanSuccess : (txt => alert("Scanned: " + txt));
    const failCb = typeof onScanFailure === "function" ? onScanFailure : (() => {});

    html5QrCode.start(cameraSource, config, successCb, failCb)
        .catch(err => console.error("Error launching camera:", err));
}
"""

# Replace existing camera start logic with new function calls
if 'function startCameraStream' in content:
    content = re.sub(r'function startCameraStream\(\)[\s\S]*?\}\n\}', js_code, content)
else:
    content = content.replace('</script>', js_code + '\n</script>')

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Added Camera Dropdown and multi-camera switcher!")
