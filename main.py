from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, Response
from PIL import Image
import io

app = FastAPI(title="ourbang-panorama-demo")

@app.get("/")
def health():
    return {"ok": True, "service": "ourbang-panorama-demo"}

def _read_image(upload: UploadFile) -> Image.Image:
    data = upload.file.read()
    if not data:
        raise ValueError("empty file")
    img = Image.open(io.BytesIO(data))
    return img.convert("RGB")

@app.post("/panorama")
async def panorama(images: list[UploadFile] = File(...)):
    try:
        if not images or len(images) < 2:
            return JSONResponse({"ok": False, "error": "Need at least 2 images."}, status_code=400)

        # Read all images
        pil_images = []
        for up in images:
            try:
                pil_images.append(_read_image(up))
            finally:
                try:
                    up.file.close()
                except Exception:
                    pass

        # Normalize height to smallest to reduce memory
        min_h = min(im.height for im in pil_images)
        resized = []
        for im in pil_images:
            if im.height != min_h:
                w = int(im.width * (min_h / im.height))
                resized.append(im.resize((max(1, w), min_h)))
            else:
                resized.append(im)

        total_w = sum(im.width for im in resized)
        pano = Image.new("RGB", (total_w, min_h))
        x = 0
        for im in resized:
            pano.paste(im, (x, 0))
            x += im.width

        out = io.BytesIO()
        pano.save(out, format="JPEG", quality=90)
        return Response(content=out.getvalue(), media_type="image/jpeg")
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
