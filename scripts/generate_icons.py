"""Generate SAgentai branded icons for all platforms."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Brand colors
BG_COLOR = (30, 30, 46)        # Dark navy background
ACCENT_COLOR = (0, 180, 216)   # Cyan/teal accent
ACCENT2_COLOR = (114, 9, 183)  # Purple accent
TEXT_COLOR = (255, 255, 255)    # White text


def draw_sagentai_logo(draw, size, offset_x=0, offset_y=0):
    """Draw the SAgentai logo - a stylized 'S' with AI circuit pattern."""
    cx = size // 2 + offset_x
    cy = size // 2 + offset_y
    r = int(size * 0.42)

    # Draw outer circle (gradient effect with concentric circles)
    for i in range(r, r - max(3, size // 40), -1):
        ratio = (r - i) / max(1, max(3, size // 40))
        color = (
            int(ACCENT_COLOR[0] * (1 - ratio) + ACCENT2_COLOR[0] * ratio),
            int(ACCENT_COLOR[1] * (1 - ratio) + ACCENT2_COLOR[1] * ratio),
            int(ACCENT_COLOR[2] * (1 - ratio) + ACCENT2_COLOR[2] * ratio),
        )
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], outline=color, width=max(1, size // 80))

    # Draw inner filled hex/shield shape
    inner_r = int(r * 0.82)
    points = []
    for angle_deg in range(0, 360, 60):
        angle = math.radians(angle_deg - 90)
        px = cx + int(inner_r * math.cos(angle))
        py = cy + int(inner_r * math.sin(angle))
        points.append((px, py))
    draw.polygon(points, fill=BG_COLOR)

    # Draw the stylized "S" letter
    s_size = int(size * 0.38)
    line_w = max(2, size // 20)
    s_left = cx - s_size // 2
    s_top = cy - s_size // 2
    s_right = cx + s_size // 2
    s_mid = cy

    # Top arc of S
    draw.arc(
        [s_left, s_top, s_right, s_mid],
        start=180, end=0,
        fill=ACCENT_COLOR, width=line_w
    )
    # Bottom arc of S
    draw.arc(
        [s_left, s_mid, s_right, s_top + s_size],
        start=0, end=180,
        fill=ACCENT2_COLOR, width=line_w
    )

    # Connection lines (the middle of the S)
    draw.line(
        [(s_right, s_top + s_size // 4), (s_right, s_mid)],
        fill=ACCENT_COLOR, width=line_w
    )
    draw.line(
        [(s_left, s_mid), (s_left, s_top + s_size * 3 // 4)],
        fill=ACCENT2_COLOR, width=line_w
    )

    # Small AI circuit dots at corners
    dot_r = max(2, size // 40)
    dot_positions = [
        (s_left, s_top + s_size // 4),
        (s_right, s_top + s_size // 4),
        (s_left, s_top + s_size * 3 // 4),
        (s_right, s_top + s_size * 3 // 4),
    ]
    for dx, dy in dot_positions:
        draw.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=ACCENT_COLOR)


def create_icon(size):
    """Create a single icon image at the given size."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    margin = max(1, size // 32)
    draw.ellipse([margin, margin, size - margin, size - margin], fill=BG_COLOR)

    draw_sagentai_logo(draw, size)
    return img


def create_ico(output_path, sizes=None):
    """Create a Windows .ico file with multiple sizes."""
    if sizes is None:
        sizes = [16, 24, 32, 48, 64, 128, 256]
    images = [create_icon(s) for s in sizes]
    images[0].save(output_path, format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
    print(f"  Created ICO: {output_path}")


def create_png(output_path, size):
    """Create a PNG icon at the given size."""
    img = create_icon(size)
    img.save(output_path, format='PNG')
    print(f"  Created PNG: {output_path} ({size}x{size})")


def create_inno_bmp(output_path, width, height, is_big=True):
    """Create BMP for Inno Setup installer wizard."""
    img = Image.new('RGB', (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    if is_big:
        # Big image: logo on left side
        logo_size = min(width, height) - 40
        logo_img = create_icon(logo_size)
        # Convert RGBA to RGB for BMP
        bg = Image.new('RGB', logo_img.size, BG_COLOR)
        bg.paste(logo_img, mask=logo_img.split()[3])
        x_pos = (width - logo_size) // 2
        y_pos = (height - logo_size) // 2
        img.paste(bg, (x_pos, y_pos))
    else:
        # Small image: just the icon
        logo_size = min(width, height) - 4
        logo_img = create_icon(logo_size)
        bg = Image.new('RGB', logo_img.size, BG_COLOR)
        bg.paste(logo_img, mask=logo_img.split()[3])
        x_pos = (width - logo_size) // 2
        y_pos = (height - logo_size) // 2
        img.paste(bg, (x_pos, y_pos))

    # Add subtle gradient bar at bottom for big images
    if is_big:
        bar_height = 4
        for x in range(width):
            ratio = x / width
            color = (
                int(ACCENT_COLOR[0] * (1 - ratio) + ACCENT2_COLOR[0] * ratio),
                int(ACCENT_COLOR[1] * (1 - ratio) + ACCENT2_COLOR[1] * ratio),
                int(ACCENT_COLOR[2] * (1 - ratio) + ACCENT2_COLOR[2] * ratio),
            )
            for y in range(height - bar_height, height):
                img.putpixel((x, y), color)

    img.save(output_path, format='BMP')
    print(f"  Created BMP: {output_path} ({width}x{height})")


def main():
    win32_dir = os.path.join(REPO_ROOT, 'resources', 'win32')
    linux_dir = os.path.join(REPO_ROOT, 'resources', 'linux')
    darwin_dir = os.path.join(REPO_ROOT, 'resources', 'darwin')

    print("=== Generating SAgentai Icons ===\n")

    # Windows main icon
    print("[Windows ICO]")
    create_ico(os.path.join(win32_dir, 'code.ico'))

    # Windows tile PNGs
    print("\n[Windows Tile PNGs]")
    create_png(os.path.join(win32_dir, 'code_70x70.png'), 70)
    create_png(os.path.join(win32_dir, 'code_150x150.png'), 150)

    # Inno Setup big wizard images (scales: 100-250%)
    # Big: 164x314 at 100%, scales up proportionally
    print("\n[Inno Setup Big Images]")
    big_scales = {
        100: (164, 314),
        125: (205, 392),
        150: (246, 471),
        175: (287, 549),
        200: (328, 628),
        225: (369, 706),
        250: (410, 785),
    }
    for scale, (w, h) in big_scales.items():
        create_inno_bmp(
            os.path.join(win32_dir, f'inno-big-{scale}.bmp'),
            w, h, is_big=True
        )

    # Inno Setup small wizard images (scales: 100-250%)
    # Small: 55x55 at 100%, scales up proportionally
    print("\n[Inno Setup Small Images]")
    small_scales = {
        100: (55, 55),
        125: (68, 68),
        150: (83, 83),
        175: (97, 97),
        200: (110, 110),
        225: (124, 124),
        250: (138, 138),
    }
    for scale, (w, h) in small_scales.items():
        create_inno_bmp(
            os.path.join(win32_dir, f'inno-small-{scale}.bmp'),
            w, h, is_big=False
        )

    # Linux icon
    print("\n[Linux PNG]")
    create_png(os.path.join(linux_dir, 'code.png'), 512)

    # Darwin icns - create as PNG (can be converted to icns later)
    print("\n[Darwin ICNS]")
    # Create multiple sizes and save as icns
    # macOS .icns requires specific tool, so we create PNGs
    # The build process uses iconutil on macOS
    darwin_icon = create_icon(1024)
    icns_path = os.path.join(darwin_dir, 'code.icns')
    # Save as PNG temporarily - actual icns conversion needs macOS
    darwin_icon.save(icns_path.replace('.icns', '_1024.png'), format='PNG')
    print(f"  Created PNG for Darwin: {icns_path.replace('.icns', '_1024.png')} (1024x1024)")
    print("  Note: .icns files need macOS iconutil for proper conversion")

    print("\n=== Icon Generation Complete ===")


if __name__ == '__main__':
    main()
