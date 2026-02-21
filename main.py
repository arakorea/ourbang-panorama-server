from flask import Flask, request, send_file, jsonify
from PIL import Image
import io

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify({"ok": True, "service": "ourbang-panorama-light", "endpoints": ["/panorama"]})

@app.post("/panorama")
def panorama():
    # Expect multipart field name: images (repeatable)
    files = request.files.getlist("images")
    if not files:
        return jsonify({"ok": False, "error": "No files. Use multipart field name 'images'."}), 400

    # Load images (RGB)
    imgs = []
    for f in files[:12]:  # limit for demo stability
        try:
            img = Image.open(f.stream).convert("RGB")
            imgs.append(img)
        except Exception:
            continue

    if not imgs:
        return jsonify({"ok": False, "error": "Could not decode any images."}), 400

    # Simple, robust "stitch": resize all to same height, concatenate horizontally.
    target_h = min(img.height for img in imgs)
    resized = []
    for img in imgs:
        if img.height != target_h:
            w = int(img.width * (target_h / img.height))
            img = img.resize((max(1, w), target_h))
        resized.append(img)

    total_w = sum(img.width for img in resized)
    pano = Image.new("RGB", (total_w, target_h))
    x = 0
    for img in resized:
        pano.paste(img, (x, 0))
        x += img.width

    out = io.BytesIO()
    pano.save(out, format="JPEG", quality=85)
    out.seek(0)
    return send_file(out, mimetype="image/jpeg", as_attachment=False, download_name="pano.jpg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
