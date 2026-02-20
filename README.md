# Ourbang Panorama Demo Server (Render free)

## What it does
- `POST /panorama` with multipart files named `images` (repeatable).
- Returns a stitched panorama as `image/jpeg` bytes.

## Deploy (Render)
1) Put these files in a GitHub repo:
- main.py
- requirements.txt
- render.yaml
2) Render → New + → Blueprint → select the repo
3) After deploy, your endpoint:
- https://<your-service>.onrender.com/panorama

## Tips
- 8~12 photos, ~30% overlap, move slowly.
- Avoid moving objects (people/TV).
