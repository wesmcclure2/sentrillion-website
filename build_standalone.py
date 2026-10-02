#!/usr/bin/env python3
"""Build preview-standalone.html: a single self-contained file with CSS, JS,
photos, and the hero video all inlined as data URIs, so it renders correctly
in chat previews that don't preserve relative folder structure."""
import base64
import re
from pathlib import Path

root = Path(__file__).parent
html = (root / "index.html").read_text()
css = (root / "css" / "style.css").read_text()

# Stylesheet url() references are relative to css/; inline them as data URIs
# so background images survive when the CSS is embedded in the page.
def inline_css_url(match):
    rel_path = match.group(1)
    full_path = (root / "css" / rel_path).resolve()
    data = full_path.read_bytes()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(full_path.suffix.lower(), "image/jpeg")
    return 'url("data:' + mime + ';base64,' + base64.b64encode(data).decode("ascii") + '")'

css = re.sub(r'url\("(\.\./assets/photos/[^"]+)"\)', inline_css_url, css)
js = (root / "js" / "main.js").read_text()

# Inline the external stylesheet link with a <style> block.
html = re.sub(
    r'<link rel="stylesheet" href="css/style\.css">',
    lambda m: f"<style>\n{css}\n</style>",
    html,
)

# Inline the external script tag with a <script> block.
html = re.sub(
    r'<script src="js/main\.js"></script>',
    lambda m: f"<script>\n{js}\n</script>",
    html,
)

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}

def inline_image(match):
    attr = match.group(1)  # "src" or "poster"
    rel_path = match.group(2)
    full_path = root / rel_path
    data = full_path.read_bytes()
    mime = MIME.get(full_path.suffix.lower(), "image/jpeg")
    b64 = base64.b64encode(data).decode("ascii")
    return f'{attr}="data:{mime};base64,{b64}"'

html = re.sub(r'(src|poster)="(assets/photos/[^"]+\.(?:jpg|jpeg|png|webp))"', inline_image, html)

VIDEO_MIME = {".mp4": "video/mp4", ".webm": "video/webm"}

def inline_video(match):
    rel_path = match.group(1)
    full_path = root / rel_path
    data = full_path.read_bytes()
    mime = VIDEO_MIME.get(full_path.suffix.lower(), "video/mp4")
    b64 = base64.b64encode(data).decode("ascii")
    return f'src="data:{mime};base64,{b64}"'

html = re.sub(r'src="(assets/video/[^"]+\.(?:mp4|webm))"', inline_video, html)

out_path = root / "preview-standalone.html"
out_path.write_text(html)
print(f"Wrote {out_path} ({out_path.stat().st_size:,} bytes)")
