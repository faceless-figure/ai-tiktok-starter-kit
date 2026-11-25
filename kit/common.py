"""Shared helpers for the starter kit: keys, Kalodata, Gemini, downloads."""
import base64, json, os, re, socket, subprocess, sys, time, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
GEMINI_MODELS = ["gemini-3-flash-preview", "gemini-3.8-flash", "gemini-2.5-flash"]


def load_keys():
    """Keys come from the environment first (cloud), then a .env file beside this kit."""
    p = os.path.join(ROOT, ".env")
    if os.path.exists(p):
        for line in open(p):
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


def key_header(header, name):
    """Send the key if this machine has it. In a cloud session the key is a network
    secret instead: the cloud adds the header itself, so the kit never sees the key."""
    v = os.environ.get(name)
    return {header: v} if v else {}


def kalo(path, body):
    b = {"region": "US", "language": "en-US", "currency": "USD"}
    b.update(body)
    req = urllib.request.Request(
        "https://www.kalodata.com/openapi/v1" + path, json.dumps(b).encode(),
        dict({"source-type": "SKILL", "Content-Type": "application/json;charset=UTF-8"},
             **key_header("secret-key", "KALODATA_API_KEY")))
    d = json.load(urllib.request.urlopen(req, timeout=60))
    if not d.get("success"):
        raise RuntimeError(f"Kalodata: {d.get('message')} (code {d.get('code')})")
    return d.get("data")


def resolve_link(url):
    """Follow a short share link to the full TikTok URL and pull out the video id."""
    m = re.search(r"/(?:video|photo)/(\d{8,})", url)
    final = url
    if not m:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            final = r.geturl()
        m = re.search(r"/(?:video|photo)/(\d{8,})", final)
    return final.split("?")[0], (m.group(1) if m else None)


def download(url, out):
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "--no-warnings", "-f", "mp4/best",
                        "-o", out, url], capture_output=True, text=True, timeout=240)
    if not os.path.exists(out):
        raise RuntimeError("download blocked or failed: " + (r.stderr.strip().splitlines() or ["no detail"])[-1][:200])
    return out


def _part(path):
    ext = path.rsplit(".", 1)[-1].lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp",
            "mp4": "video/mp4", "mov": "video/quicktime"}[ext]
    return {"inline_data": {"mime_type": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}}


def gemini_json(files, prompt, temperature=0.2):
    parts = [_part(f) for f in files] + [{"text": prompt}]
    body = json.dumps({"contents": [{"parts": parts}],
                       "generationConfig": {"response_mime_type": "application/json",
                                            "temperature": temperature}}).encode()
    last = None
    for model in [m for _ in range(3) for m in GEMINI_MODELS]:
        for attempt in range(3):
            req = urllib.request.Request(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                body, dict({"Content-Type": "application/json"},
                           **key_header("x-goog-api-key", "GEMINI_API_KEY")))
            try:
                d = json.load(urllib.request.urlopen(req, timeout=300))
                t = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"]
                            if not p.get("thought"))
                out, _ = json.JSONDecoder().raw_decode(t[t.find("{"):])
                out["_model"] = model
                return out
            except urllib.error.HTTPError as e:
                last = f"{model}: HTTP {e.code}"
                if e.code in (400, 403, 404, 429):
                    break
                time.sleep(6 * (attempt + 1))
            except (socket.timeout, TimeoutError, urllib.error.URLError):
                last = f"{model}: network"
                time.sleep(3)
    raise RuntimeError(f"Gemini failed ({last})")
