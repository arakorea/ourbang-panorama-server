# Ourbang Panorama Demo Server (Render Free, Light)

This is a **very lightweight** panorama demo server designed to deploy reliably on **Render Free**.

## What it does
- `POST /panorama` with multipart files named **images** (repeatable)
- Returns a "panorama" JPEG as **image/jpeg**
- Stitching method: **resize to same height + horizontal concatenation** (robust, fast, deploy-safe)

## Deploy (Render)
1. Push these files to a GitHub repo
2. In Render: **New → Blueprint**
3. Select this repo and deploy

After deploy, your endpoint will be:
- `https://<service-name>.onrender.com/panorama`

## Test (curl)
```bash
curl -X POST https://<service-name>.onrender.com/panorama \
  -F "images=@img1.jpg" -F "images=@img2.jpg" --output pano.jpg
```
