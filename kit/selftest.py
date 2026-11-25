#!/usr/bin/env python3
"""Check that this machine can reach everything the kit needs. Prints one line per check.

  python3 kit/selftest.py [tiktok link]
"""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c

LINK = sys.argv[1] if len(sys.argv) > 1 else None


def check(name, fn):
    try:
        print(f"PASS  {name}: {fn()}")
        return True
    except Exception as e:
        print(f"FAIL  {name}: {str(e)[:220]}")
        return False


def main():
    c.load_keys()
    check("Kalodata key + network", lambda: f"{len(c.kalo('/tiktok/product/rank', {'date_range': 'last7Day', 'page_number': 1, 'page_size': 1}) or [])} row")
    tmp = os.path.join(tempfile.mkdtemp(), "t.png")
    import base64
    open(tmp, "wb").write(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="))
    check("Gemini key + network", lambda: "answered with " + c.gemini_json([tmp], 'Return JSON {"ok": true}')["_model"])
    if LINK:
        state = {}
        def link():
            state["url"], state["vid"] = c.resolve_link(LINK)
            return f"video id {state['vid']}"
        if check("TikTok link opens", link) and state.get("vid"):
            out = os.path.join(tempfile.mkdtemp(), "v.mp4")
            check("TikTok video downloads", lambda: f"{os.path.getsize(c.download(state['url'], out)) // 1024} KB")


if __name__ == "__main__":
    main()
