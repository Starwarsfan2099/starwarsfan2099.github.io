#!/usr/bin/env python3

import argparse
import re
from pathlib import Path

from PIL import Image


# The script lives in the Jekyll site root.
SITE_ROOT = Path(__file__).resolve().parent


def update_image_sizes(markdown_path: Path) -> None:
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

    text = markdown_path.read_text(encoding="utf-8")

    # Match a Markdown image followed by a Kramdown width/height attribute:
    #
    # ![Advertisement](/public/2026-09-20/advertisment_5.jpg)
    #   {:.shadow}{:.center}{: width="583" height="543"}{:style="max-width: 90%"}
    #
    # We capture the image URL and the complete width/height attribute separately.
    image_pattern = re.compile(
        r'(?P<prefix>!\[[^\]]*\]\()'
        r'(?P<url>[^)]+)'
        r'(?P<middle>\)'
        r'(?:\{:[^}]*\})*'
        r')'
        r'(?P<size>\{:\s*width="\d+"\s+height="\d+"\})',
        re.MULTILINE
    )

    changed = 0
    skipped = 0

    def replace_image(match: re.Match) -> str:
        nonlocal changed, skipped

        image_url = match.group("url")

        # Ignore remote images.
        if image_url.startswith(("http://", "https://", "//")):
            skipped += 1
            return match.group(0)

        # Remove query strings/fragments if present.
        image_path = image_url.split("?", 1)[0].split("#", 1)[0]

        # Jekyll URLs beginning with / are relative to the site root.
        if image_path.startswith("/"):
            image_file = SITE_ROOT / image_path.lstrip("/")
        else:
            image_file = markdown_path.parent / image_path

        if not image_file.exists():
            print(f"WARNING: Image not found:")
            print(f"         {image_url}")
            print(f"         Expected: {image_file}")
            skipped += 1
            return match.group(0)

        try:
            with Image.open(image_file) as img:
                width, height = img.size
        except Exception as e:
            print(f"WARNING: Could not read image:")
            print(f"         {image_file}")
            print(f"         {e}")
            skipped += 1
            return match.group(0)

        old_size = match.group("size")

        new_size = f'{{: width="{width}" height="{height}"}}'

        if old_size == new_size:
            return match.group(0)

        changed += 1
        print(f"{image_url}: {width}x{height}")

        # Replace ONLY the size attribute.
        return (
            match.group("prefix")
            + image_url
            + match.group("middle")
            + new_size
        )

    new_text = image_pattern.sub(replace_image, text)

    if new_text != text:
        markdown_path.write_text(new_text, encoding="utf-8")

    print()
    print(f"Updated: {changed}")
    print(f"Skipped: {skipped}")

    if changed:
        print(f"Saved:   {markdown_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update image width/height attributes in a Jekyll Markdown post."
    )

    parser.add_argument(
        "markdown_file",
        help="Path to the Markdown file"
    )

    args = parser.parse_args()

    markdown_path = Path(args.markdown_file)

    # Relative paths are relative to the directory you're running from.
    if not markdown_path.is_absolute():
        markdown_path = Path.cwd() / markdown_path

    update_image_sizes(markdown_path)


if __name__ == "__main__":
    main()