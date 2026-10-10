import re

html_path = "static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Enhanced JavaScript logic for friendly camera labeling and smart rear camera auto-select
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
            }

            let defaultCamId = null;

            devices.forEach((device, idx) => {
                const labelLower = (device.label || "").toLowerCase();
                let cleanName = `Camera ${idx + 1}`;

                // Categorize camera types based on browser hardware labels
                if (labelLower.includes("front") || labelLower.includes("user") || labelLower.includes("selfie")) {
                    cleanName = `🤳 Front Camera ${devices.length > 2 ? `(${idx + 1})` : ""}`;
                } else if (labelLower.includes("back") || labelLower.includes("rear") || labelLower.includes("environment") || labelLower.includes("0")) {
                    cleanName = `📷 Rear Camera ${idx + 1}`;
                    if (!defaultCamId) defaultCamId = device.id;
                } else {
                    cleanName = `📷 Camera ${idx + 1} (${device.label || 'Rear/Aux'})`;
                }

                if (selectEl) {
                    const opt = document.createElement("option");
                    opt.value = device.id;
                    opt.text = cleanName;
                    selectEl.appendChild(opt);
                }
            });

            // If no explicit 'back' label was matched, default to the last camera in list (usually main rear camera on Android)
            if (!defaultCamId) {
                defaultCamId = devices.length > 1 ? devices[devices.length - 1].id : devices[0].id;
            }

            if (selectEl) selectEl.value = defaultCamId;
            launchScanner(defaultCamId);
        } else {
            launchScanner({ facingMode: "environment" });
        }
    }).catch(err => {
        console.warn("getCameras failed, using default environment constraint:", err);
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

# Replace existing startCameraStream logic
if 'function startCameraStream' in content:
    content = re.sub(r'function startCameraStream\(\)[\s\S]*?\}\n\}', js_code, content)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully updated camera labels and rear camera auto-selection!")
