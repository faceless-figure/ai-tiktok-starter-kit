#!/usr/bin/env python3
"""Quality check a finished AI video before posting.

  python3 kit/qc.py <render.mp4> <product photo> [more product photos...]

Reads your character from memory/character.md. Exit code 0 = PASS, 1 = FAIL.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c

PROMPT = """You are the quality gate for an AI fashion video for TikTok Shop.
Inputs, in order: the RENDER to judge, then product photo(s) of the item being sold.
Watch the WHOLE render frame by frame.
The person in the render must match this character sheet (hairstyle may change between videos):
---
{character}
---
Judge strictly and return ONLY JSON:
{{
 "product_match": 1-10,
 "product_issues": "",
 "character_ok": true/false,
 "character_issues": "",
 "anatomy_ok": true/false,
 "anatomy_issues": "hands, fingers, feet, limbs, melting or merging",
 "scale_ok": true/false,
 "setting_stable": true/false,
 "object_continuity_ok": true/false,
 "continuity_issues": "objects that vanish, appear, duplicate or change; a phone or bag switching hands",
 "product_detail_placement_ok": true/false,
 "ai_tells": "anything that reads as AI to someone scrolling",
 "noticeable": true/false,
 "on_screen_text_or_watermark": true/false,
 "verdict": "PASS" or "FAIL",
 "fix_for_retry": "one or two concrete prompt changes if FAIL, else empty"
}}
FAIL only for problems a normal person scrolling on a phone would NOTICE: product_match under 7,
a noticeable anatomy, scale, continuity or detail-placement problem, or text/watermark.
Minor issues nobody would see = PASS, but list them in ai_tells."""


def main():
    render, *prods = sys.argv[1:]
    c.load_keys()
    p = os.path.join(c.ROOT, "memory", "character.md")
    character = open(p).read().strip() if os.path.exists(p) else "No character sheet yet: judge one consistent realistic person."
    out = c.gemini_json([render] + prods, PROMPT.format(character=character), temperature=0.1)
    print(json.dumps(out, indent=1, ensure_ascii=False))
    sys.exit(0 if out.get("verdict") == "PASS" else 1)


if __name__ == "__main__":
    main()
