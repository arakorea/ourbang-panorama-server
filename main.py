from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response, JSONResponse
import numpy as np

app = FastAPI(title="ourbang-panorama-demo")

def _read_image(upload: UploadFile):
    import cv2
    data = upload.file.read()
    if not data:
        return None
    arr = np.frombuffer(data, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

@app.get("/")
def root():
    return {"ok": True, "service": "ourbang-panorama-demo"}

@app.post("/panorama")
async def panorama(images: list[UploadFile] = File(...)):
    """Accepts multipart form with repeated field name 'images'.
    Returns JPEG bytes (stitched panorama) on success."""
    try:
        import cv2
    except Exception as e:
        return JSONResponse({"ok": False, "error": f"cv2 import failed: {e}"}, status_code=500)

    imgs = []
    for up in images:
        img = _read_image(up)
        if img is not None:
            imgs.append(img)

    if len(imgs) < 2:
        return JSONResponse({"ok": False, "error": "Need at least 2 images."}, status_code=400)

    try:
        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    except Exception:
        stitcher = cv2.Stitcher_create()

    status, pano = stitcher.stitch(imgs)

    if status != 0 or pano is None:
        return JSONResponse(
            {"ok": False, "error": f"stitch failed (status={status}). Try more overlap / consistent exposure."},
            status_code=422
        )

    ok, buf = cv2.imencode(".jpg", pano, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
    if not ok:
        return JSONResponse({"ok": False, "error": "JPEG encode failed."}, status_code=500)

    return Response(content=buf.tobytes(), media_type="image/jpeg")
