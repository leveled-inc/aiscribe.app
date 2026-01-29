#!/usr/bin/env python3
"""
Generate blog header images using Hugging Face Inference API (free tier).
Uses FLUX.1-schnell for fast, high-quality image generation.
"""

import os
import requests
import time
from pathlib import Path

# Your HF token
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is required")

# API endpoint for FLUX.1-schnell (new router endpoint)
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Output directory
OUTPUT_DIR = Path("/Users/zackgemmell/aiscribe/assets/images/blog")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Blog posts to generate images for (first batch of 5)
BLOG_POSTS = [
    {
        "filename": "2026-02-05-from-burnout-to-balance-the-ai-scribe-solution",
        "title": "From Burnout to Balance: The AI Scribe Solution",
        "prompt": "A serene medical office scene showing a relaxed physician at a desk with a laptop, warm lighting, peaceful atmosphere, modern healthcare technology, professional medical setting, soft blue and white colors, photorealistic, high quality, wide format banner"
    },
    {
        "filename": "2025-03-28-ai-scribes-for-mental-health",
        "title": "The Ultimate Guide to AI Scribes for Mental Health Professionals",
        "prompt": "A calm therapy office with comfortable seating, soft natural light through windows, subtle technology elements like a tablet, warm earth tones, plants, peaceful mental health setting, professional yet welcoming, photorealistic, wide format banner"
    },
    {
        "filename": "2025-06-05-hipaa-compliance-ai-scribes",
        "title": "HIPAA Compliance and AI Scribes: A Non-Negotiable",
        "prompt": "A secure digital shield protecting medical data, abstract representation of healthcare security, blue and green colors, lock symbols, medical cross, modern technology, clean professional design, digital art style, wide format banner"
    },
    {
        "filename": "2025-08-12-future-is-ambient",
        "title": "The Future is Ambient: How AI Scribes Are Disappearing into the Exam Room",
        "prompt": "A modern medical exam room with subtle ambient technology integrated into walls and ceiling, doctor and patient in conversation with no visible devices, futuristic but warm healthcare setting, soft lighting, photorealistic, wide format banner"
    },
    {
        "filename": "2026-04-27-the-art-of-listening",
        "title": "The Art of Listening: How Ambient AI Scribes are Restoring the Physician-Patient Connection",
        "prompt": "A doctor leaning in attentively listening to a patient, warm eye contact, compassionate healthcare scene, modern medical office, subtle technology in background, warm golden light, human connection in medicine, photorealistic, wide format banner"
    }
]


def generate_image(prompt: str, retries: int = 3) -> bytes | None:
    """Generate an image using HF Inference API."""
    for attempt in range(retries):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json={"inputs": prompt},
                timeout=120
            )

            if response.status_code == 200:
                return response.content
            elif response.status_code == 503:
                # Model loading, wait and retry
                print(f"  Model loading, waiting 30s... (attempt {attempt + 1}/{retries})")
                time.sleep(30)
            else:
                print(f"  Error: {response.status_code} - {response.text}")
                if attempt < retries - 1:
                    time.sleep(10)
        except Exception as e:
            print(f"  Request error: {e}")
            if attempt < retries - 1:
                time.sleep(10)

    return None


def main():
    print("=" * 60)
    print("Blog Image Generator - Hugging Face Inference API")
    print("=" * 60)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print(f"Generating {len(BLOG_POSTS)} images...\n")

    successful = 0
    failed = 0

    for i, post in enumerate(BLOG_POSTS, 1):
        print(f"[{i}/{len(BLOG_POSTS)}] {post['title']}")
        print(f"  Prompt: {post['prompt'][:80]}...")

        image_data = generate_image(post["prompt"])

        if image_data:
            output_path = OUTPUT_DIR / f"{post['filename']}.png"
            output_path.write_bytes(image_data)
            print(f"  ✅ Saved: {output_path}")
            successful += 1
        else:
            print(f"  ❌ Failed to generate image")
            failed += 1

        # Small delay between requests to avoid rate limiting
        if i < len(BLOG_POSTS):
            time.sleep(2)

    print("\n" + "=" * 60)
    print(f"Complete! {successful} successful, {failed} failed")
    print(f"Images saved to: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
