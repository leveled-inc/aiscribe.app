#!/usr/bin/env python3
"""
Update blog post front matter to include image references.
"""

import re
from pathlib import Path

POSTS_DIR = Path("/Users/zackgemmell/aiscribe/_posts")
IMAGES_DIR = Path("/Users/zackgemmell/aiscribe/assets/images/blog")

def get_image_filename(post_filename: str) -> str:
    """Convert post filename to image filename."""
    # Remove .markdown extension and return
    return post_filename.replace(".markdown", "")

def update_post_frontmatter(post_path: Path, image_path: str) -> bool:
    """Add image to post front matter if not already present."""
    content = post_path.read_text()

    # Check if image is already in front matter
    if "image:" in content[:500]:
        return False

    # Find the end of front matter (second ---)
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False

    frontmatter = match.group(1)

    # Add image line before the closing ---
    new_frontmatter = frontmatter.rstrip() + f"\nimage: {image_path}\n"
    new_content = f"---\n{new_frontmatter}---" + content[match.end():]

    post_path.write_text(new_content)
    return True

def main():
    print("Updating blog post front matter with image references...")
    print("=" * 60)

    # Get all images
    images = {img.stem: img for img in IMAGES_DIR.glob("*.png")}
    print(f"Found {len(images)} images\n")

    updated = 0
    skipped = 0
    no_image = 0

    for post_path in sorted(POSTS_DIR.glob("*.markdown")):
        post_stem = post_path.stem

        if post_stem in images:
            image_web_path = f"/assets/images/blog/{post_stem}.png"
            if update_post_frontmatter(post_path, image_web_path):
                print(f"✅ Updated: {post_path.name}")
                updated += 1
            else:
                print(f"⏭️  Skipped (already has image): {post_path.name}")
                skipped += 1
        else:
            print(f"⚠️  No image found: {post_path.name}")
            no_image += 1

    print("\n" + "=" * 60)
    print(f"Updated: {updated}")
    print(f"Skipped (already had image): {skipped}")
    print(f"No matching image: {no_image}")
    print("=" * 60)

if __name__ == "__main__":
    main()
