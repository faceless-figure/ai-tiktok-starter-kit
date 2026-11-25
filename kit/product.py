#!/usr/bin/env python3
"""Look up a product on Kalodata and list its top recent videos.

  python3 kit/product.py <product id> [last7Day|last30Day]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as c


def main():
    pid = sys.argv[1]
    rng = sys.argv[2] if len(sys.argv) > 2 else "last7Day"
    c.load_keys()
    out = {"product_id": pid}
    try:
        out["product"] = c.kalo("/tiktok/product/detail", {"date_range": rng, "product_id": pid})
    except Exception as e:
        out["product_error"] = str(e)
    try:
        vids = c.kalo("/tiktok/video/rank", {"date_range": rng, "product_id": pid, "need_extra": True,
                                             "page_number": 1, "page_size": 10,
                                             "sort_field": {"field": "revenue", "type": "DESC"}}) or []
        out["top_videos"] = [{"url": f"https://www.tiktok.com/@{v.get('belonged_creator_handle') or 'x'}/video/{v['video_id']}",
                              "views": v.get("views"), "revenue": v.get("revenue"), "ad": v.get("ad"),
                              "title": v.get("video_title")} for v in vids]
    except Exception as e:
        out["videos_error"] = str(e)
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
