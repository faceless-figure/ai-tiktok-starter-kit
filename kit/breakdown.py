#!/usr/bin/env python3
"""Send a TikTok link (or a saved video file) and get the full breakdown.

  python3 kit/breakdown.py <tiktok link | video.mp4>

Each step reports on its own, so a blocked step never hides the others.
Output: JSON on screen + work/<video id>/breakdown.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c

PROMPT = """You are breaking down a TikTok Shop fashion video so a different creator can film
their OWN version of the same format with their own character and room.
Watch the whole video and listen to the audio. Return ONLY JSON:
{
 "format": "mirror selfie | tripod full body | close-up | POV looking down | walking | showcase in hand | talking | other",
 "length_sec": number,
 "hook_first_2s": "what happens in the first two seconds that stops the scroll",
 "beats": [{"t": "0-2s", "action": "what the body does", "camera": "what the camera does"}],
 "camera": "angle, distance, phone or tripod, movement",
 "setting": "room, lighting, time of day",
 "talking": true/false,
 "on_screen_text": "exact text burned in, or empty",
 "sound": "music only | voiceover | talking | silent",
 "product": {"type": "", "colour": "", "details": "cut, fit, length, visible features"},
 "rest_of_outfit": "everything worn that is not the product",
 "why_it_works": "one or two sentences",
 "remake_notes": "what must stay the same (motion, framing, pacing) and what must change (person, room, outfit pieces) so it is not a copy",
 "hard_for_ai": "moves an AI video model will likely get wrong, or empty"
}"""


def main():
    src = sys.argv[1]
    c.load_keys()
    out = {"input": src, "steps": {}}
    video_file, vid, url = None, None, None

    if os.path.exists(src):
        video_file, vid = src, os.path.splitext(os.path.basename(src))[0]
        out["steps"]["link"] = "skipped (file given)"
    else:
        try:
            url, vid = c.resolve_link(src)
            out["url"], out["video_id"] = url, vid
            out["steps"]["link"] = "ok" if vid else "no video id found in link"
        except Exception as e:
            out["steps"]["link"] = f"FAILED: {e}"

    work = os.path.join(c.ROOT, "work", vid or "unknown")
    os.makedirs(work, exist_ok=True)

    if vid and url:
        try:
            d = c.kalo("/tiktok/video/detail", {"date_range": "last30Day", "video_id": vid, "need_extra": True})
            out["kalodata_video"] = d
            out["steps"]["kalodata_video"] = "ok" if d else "not in Kalodata yet (new video?)"
        except Exception as e:
            out["steps"]["kalodata_video"] = f"FAILED: {e}"
        try:
            ps = c.kalo("/tiktok/product/rank", {"date_range": "last30Day", "video_id": vid,
                                                 "page_number": 1, "page_size": 3}) or []
            out["products"] = [{"product_id": x.get("product_id"), "name": x.get("product_name"),
                                "image": x.get("image_url") or x.get("master_image_url")} for x in ps]
            out["steps"]["kalodata_product"] = "ok" if ps else "no product found"
        except Exception as e:
            out["steps"]["kalodata_product"] = f"not found ({e}) -> video has no tracked sales yet; send product screenshots instead"
        try:
            video_file = c.download(url, os.path.join(work, "video.mp4"))
            out["steps"]["download"] = "ok"
        except Exception as e:
            out["steps"]["download"] = f"FAILED: {e} -> save the video on your phone and send the file instead"

    if video_file:
        try:
            out["breakdown"] = c.gemini_json([video_file], PROMPT)
            out["steps"]["gemini"] = "ok"
        except Exception as e:
            out["steps"]["gemini"] = f"FAILED: {e}"

    json.dump(out, open(os.path.join(work, "breakdown.json"), "w"), indent=1)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
