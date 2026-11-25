# Starter kit (test build)

What it does: send a TikTok link, get the product and a full video breakdown; quality-check a finished video.

Keys needed: `KALODATA_API_KEY`, `GEMINI_API_KEY` (in `.env` on a computer, or as environment secrets in a cloud session).

- `python3 kit/selftest.py [tiktok link]`  checks every connection, one line each
- `python3 kit/breakdown.py <link or file>`  link -> Kalodata -> download -> Gemini breakdown
- `python3 kit/product.py <product id>`  product stats + top videos
- `python3 kit/qc.py <video> <product photo>`  quality gate, reads `character.md`

Not included on purpose: any character, any phone automation.
