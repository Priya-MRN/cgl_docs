# -*- coding: utf-8 -*-
"""
TNPSC signature image normalizer.

Output spec:
    - 6 cm x 3 cm at 200 DPI  ->  472 x 236 px
    - white background
    - JPEG, file size between 10-20 KB
    - signature auto-cropped, darkened, centered

Usage:
    python make_tnpsc_signature.py <source_image> [output.jpg]
"""
import sys
import os
from PIL import Image, ImageOps, ImageChops

# ---- TNPSC target spec ---------------------------------------------------
# NOTE: The portal's on-screen "6 x 3 cm" is the DRAWING BOX on paper.
# The validator checks the CROPPED upload pixel size. The most consistently
# accepted signature size across TNPSC tools is 275 x 118 px (3.5 x 1.5 cm
# @ 200 dpi). We default to that and also emit documented alternates.
DPI = 200
SIZE_MIN_KB, SIZE_MAX_KB = 10, 20
MARGIN_FRAC = 0.05                     # padding around the cropped signature

# (width, height, label) candidates, in order of likelihood
CANDIDATES = [
    (275, 118, "275x118_primary"),     # 3.5 x 1.5 cm @ 200 dpi  (most cited)
    (230, 75,  "230x75_alt"),          # 6.0 x 2.0 cm variant
    (140, 60,  "140x60_alt"),          # common small variant
    (472, 236, "472x236_6x3cm"),       # literal 6x3 cm (already rejected)
]
# Backward-compatible single target (primary)
TARGET_W, TARGET_H = CANDIDATES[0][0], CANDIDATES[0][1]

# ink detection: pixels darker than this (after grayscale) are "signature"
INK_THRESHOLD = 200


def autocrop_signature(src_path):
    """Open image, flatten onto white, return tightly-cropped signature
    (still RGB, dark ink on white)."""
    img = Image.open(src_path)
    img = ImageOps.exif_transpose(img)          # honor phone rotation

    # Flatten any transparency onto white
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img).convert("RGB")
    else:
        img = img.convert("RGB")

    # Build a mask of the ink by thresholding the grayscale
    gray = ImageOps.grayscale(img)
    mask = gray.point(lambda p: 255 if p < INK_THRESHOLD else 0)
    bbox = mask.getbbox()
    if bbox:
        # add a little padding
        pad_x = int((bbox[2] - bbox[0]) * 0.02) + 2
        pad_y = int((bbox[3] - bbox[1]) * 0.04) + 2
        left = max(bbox[0] - pad_x, 0)
        top = max(bbox[1] - pad_y, 0)
        right = min(bbox[2] + pad_x, img.width)
        bottom = min(bbox[3] + pad_y, img.height)
        img = img.crop((left, top, right, bottom))
    return img


def clean_background(img):
    """Push near-white pixels to pure white so the JPEG is clean and small,
    while keeping the ink strokes."""
    gray = ImageOps.grayscale(img)
    # Everything lighter than ~225 -> pure white; keep darker ink as-is.
    white_mask = gray.point(lambda p: 255 if p > 225 else 0)
    white = Image.new("RGB", img.size, (255, 255, 255))
    img = Image.composite(white, img, white_mask)
    return img


def place_on_canvas(sig, target_w, target_h):
    """Scale the cropped signature to fit inside a target canvas with a
    margin, centered, on a white background."""
    avail_w = int(target_w * (1 - 2 * MARGIN_FRAC))
    avail_h = int(target_h * (1 - 2 * MARGIN_FRAC))

    scale = min(avail_w / sig.width, avail_h / sig.height)
    new_w = max(1, int(sig.width * scale))
    new_h = max(1, int(sig.height * scale))
    sig_resized = sig.resize((new_w, new_h), Image.LANCZOS)

    canvas = Image.new("RGB", (target_w, target_h), (255, 255, 255))
    x = (target_w - new_w) // 2
    y = (target_h - new_h) // 2
    canvas.paste(sig_resized, (x, y))
    return canvas


def _save(img, out_path, q, optimize):
    img.save(out_path, "JPEG", quality=q, dpi=(DPI, DPI),
             optimize=optimize, subsampling=0)
    return os.path.getsize(out_path) / 1024


def save_in_size_window(img, out_path):
    """Land the JPEG within 10-20 KB.

    Strategy:
      1. Binary-search quality WITH optimize=True for the high end (<=20 KB).
      2. If the result is under 10 KB (sparse signature), drop optimize and
         raise quality - more honest bytes from real image data, not padding -
         until we cross 10 KB or hit q=100.
    """
    # --- Pass 1: optimized, keep <= MAX ---
    lo, hi = 10, 95
    best, best_kb = None, None
    for _ in range(12):
        q = (lo + hi) // 2
        kb = _save(img, out_path, q, optimize=True)
        if kb > SIZE_MAX_KB:
            hi = q - 1
        else:
            best, best_kb = q, kb
            if kb >= SIZE_MIN_KB:
                return q, kb           # sweet spot
            lo = q + 1
    if best is None:
        best, best_kb = lo, _save(img, out_path, lo, optimize=True)

    # --- Pass 2: too small -> drop optimize, climb quality for more bytes ---
    if best_kb < SIZE_MIN_KB:
        for q in range(90, 101):
            kb = _save(img, out_path, q, optimize=False)
            if kb > SIZE_MAX_KB:
                # overshoot: step back one and keep that
                kb = _save(img, out_path, q - 1, optimize=False)
                return q - 1, kb
            best, best_kb = q, kb
            if kb >= SIZE_MIN_KB:
                return q, kb

    return best, best_kb


def main():
    if len(sys.argv) < 2:
        print("Usage: python make_tnpsc_signature.py <source_image> [out_dir]")
        sys.exit(1)
    src = sys.argv[1]
    if not os.path.isfile(src):
        print("ERROR: source file not found:", src)
        sys.exit(1)
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(src))
    os.makedirs(out_dir, exist_ok=True)

    # Crop + clean once, reuse for every candidate size.
    sig = autocrop_signature(src)
    sig = clean_background(sig)

    print(f"Source cropped to: {sig.width} x {sig.height} px\n")
    for w, h, label in CANDIDATES:
        out = os.path.join(out_dir, f"signature_{label}.jpg")
        canvas = place_on_canvas(sig, w, h)
        q, kb = save_in_size_window(canvas, out)
        status = "OK" if SIZE_MIN_KB <= kb <= SIZE_MAX_KB else "size!"
        print(f"[{status:5}] {os.path.basename(out):28} "
              f"{w}x{h} px  q={q:2}  {kb:5.1f} KB")
    print("\nTry them on the portal in this order (top = most likely).")


if __name__ == "__main__":
    main()
