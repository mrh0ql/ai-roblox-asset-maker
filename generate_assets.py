"""
ai-roblox-asset-maker
Turn text prompts into game art (icons, decals, GUI buttons) for Roblox.

Usage:
    python generate_assets.py "a glowing blue sword icon, flat style"
    python generate_assets.py "cartoon coin" --count 4 --size 512x512

Needs OPENAI_API_KEY in your environment (or a .env file).
Generated PNGs land in ./assets and are ready to upload as Roblox decals.
"""
import os
import base64
import argparse
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ROBLOX_STYLE = (
    "Game asset for Roblox. Clean, high-contrast, centered subject on a "
    "transparent or plain background. No text, no watermark. Style: "
)


def slugify(text: str) -> str:
    keep = [c if c.isalnum() else "-" for c in text.lower()]
    return "".join(keep).strip("-")[:40] or "asset"


def generate(prompt: str, count: int, size: str, out_dir: str) -> None:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    full_prompt = ROBLOX_STYLE + prompt
    print(f"Generating {count} asset(s) for: {prompt!r}")
    result = client.images.generate(
        model="gpt-image-1",
        prompt=full_prompt,
        size=size,
        n=count,
    )
    base = slugify(prompt)
    for i, item in enumerate(result.data):
        png = base64.b64decode(item.b64_json)
        path = Path(out_dir) / f"{base}-{i+1}.png"
        path.write_bytes(png)
        print(f"  wrote {path}")
    print("Done. Upload these in Studio: Asset Manager -> Images, or as Decals.")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Roblox asset generator")
    parser.add_argument("prompt", help="what to draw, e.g. 'a fire sword icon'")
    parser.add_argument("--count", type=int, default=1, help="how many variations")
    parser.add_argument("--size", default="1024x1024", help="image size WxH")
    parser.add_argument("--out", default="assets", help="output folder")
    args = parser.parse_args()
    generate(args.prompt, args.count, args.size, args.out)


if __name__ == "__main__":
    main()
