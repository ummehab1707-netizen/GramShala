import re

html_path = "static/index.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# JavaScript replacement for smart camera detection
new_camera_logic = """
Html5Qrcode.getCameras().then(devices => {
    if (devices && devices.length > 0) {
        // Find camera with 'back', 'rear', or 'environment' in its label
        let selectedCam = devices.find(d => /back|rear|environment|main|0,/i.test(d.label));
        
        // If not found by label, pick the last camera in the list (usually rear camera on Android)
        if (!selectedCam) {
            selectedCam = devices[devices.length - 1];
        }
        
        console.log("Selected camera:", selectedCam.label || selectedCam.id);
        
        html5QrCode.start(
            selectedCam.id,
            { fps: 10, qrbox: { width: 250, height: 250 } },
            onScanSuccess,
            onScanFailure
        ).catch(err => {
            // Fallback to facingMode constraint if ID fails
            html5QrCode.start({ facingMode: "environment" }, { fps: 10, qrbox: { width: 250, height: 250 } }, onScanSuccess, onScanFailure);
        });
    } else {
        html5QrCode.start({ facingMode: "environment" }, { fps: 10, qrbox: { width: 250, height: 250 } }, onScanSuccess, onScanFailure);
    }
}).catch(err => {
    html5QrCode.start({ facingMode: "environment" }, { fps: 10, qrbox: { width: 250, height: 250 } }, onScanSuccess, onScanFailure);
});
"""

# Replace existing camera start blocks
pattern = r'Html5Qrcode\.getCameras\(\)[\s\S]*?\)\;\s*\}'
if re.search(pattern, content):
    content = re.sub(pattern, new_camera_logic.strip(), content)
else:
    # Replace direct facingMode calls
    content = re.sub(
        r'html5QrCode\.start\([^\)]+\)',
        new_camera_logic.strip(),
        content
    )

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Applied smart back-camera detection script!")
