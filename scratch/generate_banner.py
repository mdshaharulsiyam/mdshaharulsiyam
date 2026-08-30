import os
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def generate_clean_binary_banner():
    # 2x supersampling for ultra-crisp anti-aliased rendering
    scale = 2
    banner_w, banner_h = 2240 * scale, 528 * scale
    out_w, out_h = 2240, 528
    
    # 1. Base dark background with very subtle cyber gradient / glow
    canvas = Image.new("RGBA", (banner_w, banner_h), (6, 10, 19, 255))
    
    # Subtle background ambient lighting near the right avatar circle
    circle_r = int(210 * scale)
    circle_cx = int((2240 - 210 - 120) * scale)
    circle_cy = int((528 // 2) * scale)
    
    # Ambient radial glow behind the avatar
    glow_layer = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)
    glow_draw.ellipse(
        [(circle_cx - circle_r - 70 * scale, circle_cy - circle_r - 70 * scale),
         (circle_cx + circle_r + 70 * scale, circle_cy + circle_r + 70 * scale)],
        fill=(0, 180, 240, 30)
    )
    # Subtle accent glow on the left name area
    glow_draw.ellipse(
        [(int(80 * scale), int(60 * scale)),
         (int(850 * scale), int(350 * scale))],
        fill=(0, 140, 220, 18)
    )
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=50 * scale))
    canvas = Image.alpha_composite(canvas, glow_layer)

    # -------------------------------------------------------------------------
    # RIGHT SIDE: AVATAR PORTRAIT IN BINARY MATRIX
    # -------------------------------------------------------------------------
    step_x = 8 * scale
    step_y = 12 * scale
    font_size = 12 * scale
    
    font_mono = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", font_size)
    font_mono_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", font_size)
    
    # Process avatar image
    avatar_img = Image.open("avatar.png").convert("RGB")
    arr = np.array(avatar_img, dtype=np.float32)
    rc, gc, bc = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    
    skin = (rc > 95) & (gc > 48) & (bc > 25) & (rc > gc) & (gc > bc) & ((rc - bc) > 18)
    dark = (rc < 85) & (gc < 85) & (bc < 85)
    
    H, W = skin.shape
    yg, xg = np.indices((H, W))
    roi = (xg >= 85) & (xg <= 385) & (yg >= 22)
    person = (skin | dark) & roi
    
    pm = Image.fromarray((person * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=2.0))
    mask_np = np.array(pm, dtype=np.float32) / 255.0

    gray = 0.299 * rc + 0.587 * gc + 0.114 * bc
    pg = Image.fromarray(gray.astype(np.uint8))
    gray_np = np.array(ImageEnhance.Contrast(pg).enhance(1.9), dtype=np.float32) / 255.0
    edge_np = np.array(pg.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(radius=0.4)), dtype=np.float32) / 255.0

    fbs = int(circle_r * 2.2)
    s_mask = np.array(Image.fromarray((mask_np*255).astype(np.uint8)).resize((fbs,fbs), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    s_gray = np.array(Image.fromarray((gray_np*255).astype(np.uint8)).resize((fbs,fbs), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    s_edge = np.array(Image.fromarray((edge_np*255).astype(np.uint8)).resize((fbs,fbs), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    s_skin = np.array(Image.fromarray((skin*255).astype(np.uint8)).resize((fbs,fbs), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
    s_dark = np.array(Image.fromarray((dark*255).astype(np.uint8)).resize((fbs,fbs), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0

    ftlx = circle_cx - fbs // 2
    ftly = circle_cy - fbs // 2 + int(15 * scale)

    # Render binary inside circle
    binary_layer = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(binary_layer)
    
    bloom_layer = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    bloom_draw = ImageDraw.Draw(bloom_layer)

    random.seed(31337)
    
    # Calculate bounding box for the circle grid
    min_x = circle_cx - circle_r - 20 * scale
    max_x = circle_cx + circle_r + 20 * scale
    min_y = circle_cy - circle_r - 20 * scale
    max_y = circle_cy + circle_r + 20 * scale
    
    for y in range(min_y, max_y, step_y):
        for x in range(min_x, max_x, step_x):
            char = random.choice(['0', '1'])
            sx = x + step_x // 2
            sy = y + step_y // 2
            
            dx = sx - circle_cx
            dy = sy - circle_cy
            dist = math.sqrt(dx*dx + dy*dy)
            
            if dist <= circle_r:
                ix = sx - ftlx
                iy = sy - ftly
                in_face = (0 <= ix < fbs) and (0 <= iy < fbs)
                mv = s_mask[iy, ix] if in_face else 0.0
                ev = max(0.0, min(1.0, (circle_r - dist) / (8.0 * scale)))
                
                if in_face and mv > 0.18:
                    is_skin = s_skin[iy, ix] > 0.25
                    is_dark = s_dark[iy, ix] > 0.25
                    gv = s_gray[iy, ix]
                    edv = s_edge[iy, ix]
                    
                    if is_skin:
                        lum = (gv * 0.72 + edv * 0.4) * ev
                        if lum > 0.50:
                            b_draw.text((x,y), char, font=font_mono_bold, fill=(255,255,255,255))
                            bloom_draw.text((x,y), char, font=font_mono_bold, fill=(0,255,240,255))
                        elif lum > 0.30:
                            b_draw.text((x,y), char, font=font_mono, fill=(15,248,228,245))
                            bloom_draw.text((x,y), char, font=font_mono, fill=(0,218,218,175))
                        elif lum > 0.16:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,198,188,205))
                            bloom_draw.text((x,y), char, font=font_mono, fill=(0,145,162,85))
                        else:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,148,158,185))
                    elif is_dark:
                        if edv > 0.15:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,192,188,215))
                            bloom_draw.text((x,y), char, font=font_mono, fill=(0,142,162,95))
                        elif mv > 0.45:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,122,138,165))
                        else:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,78,95,115))
                    else:
                        gray_val = s_gray[iy, ix]
                        if gray_val > 0.5:
                            b_draw.text((x,y), char, font=font_mono_bold, fill=(255,255,255,255))
                        else:
                            b_draw.text((x,y), char, font=font_mono, fill=(0,200,200,255))
                else:
                    # Inside circle background subtle binary
                    b_draw.text((x,y), char, font=font_mono, fill=(0,110,140,160))

    # Cyber rings and ticks around avatar
    orbit_layer = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(orbit_layer)
    
    # Outer rings
    for offset in range(-2 * scale, 3 * scale, scale):
        o_draw.ellipse(
            [(circle_cx - circle_r + offset, circle_cy - circle_r + offset),
             (circle_cx + circle_r - offset, circle_cy + circle_r - offset)],
            outline=(0, 240, 255, 255), width=2 * scale
        )
    
    r_out = circle_r + int(16 * scale)
    o_draw.ellipse(
        [(circle_cx - r_out, circle_cy - r_out), (circle_cx + r_out, circle_cy + r_out)],
        outline=(0, 180, 230, 200), width=2 * scale
    )
    
    # Orbital ticks
    for i in range(60):
        angle = 2 * math.pi * i / 60
        tick_len = int(14 * scale if i % 5 == 0 else 8 * scale)
        tx1 = circle_cx + (circle_r + int(16 * scale)) * math.cos(angle)
        ty1 = circle_cy + (circle_r + int(16 * scale)) * math.sin(angle)
        tx2 = circle_cx + (circle_r + int(16 * scale) + tick_len) * math.cos(angle)
        ty2 = circle_cy + (circle_r + int(16 * scale) + tick_len) * math.sin(angle)
        w = 3 * scale if i % 5 == 0 else 2 * scale
        o_draw.line([(tx1, ty1), (tx2, ty2)], fill=(0, 255, 220, 255), width=w)
    
    # Circle cyber pill tags
    f_badge_xs = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", int(13 * scale))
    
    o_draw.rounded_rectangle(
        [(circle_cx - 95 * scale, circle_cy - circle_r - 22 * scale),
         (circle_cx + 95 * scale, circle_cy - circle_r + 6 * scale)],
        radius=4 * scale, fill=(0, 240, 255, 255)
    )
    o_draw.text((circle_cx - 82 * scale, circle_cy - circle_r - 18 * scale), "[ 01001101 01000100 ]", font=f_badge_xs, fill=(5, 12, 24, 255))
    
    o_draw.rounded_rectangle(
        [(circle_cx - 85 * scale, circle_cy + circle_r - 6 * scale),
         (circle_cx + 85 * scale, circle_cy + circle_r + 22 * scale)],
        radius=4 * scale, fill=(0, 255, 180, 255)
    )
    o_draw.text((circle_cx - 72 * scale, circle_cy + circle_r - 3 * scale), "IDENTITY: VERIFIED", font=f_badge_xs, fill=(5, 12, 24, 255))

    # Apply neon bloom for the right side
    g1 = bloom_layer.filter(ImageFilter.GaussianBlur(radius=2 * scale))
    g2 = bloom_layer.filter(ImageFilter.GaussianBlur(radius=6 * scale))
    g3 = bloom_layer.filter(ImageFilter.GaussianBlur(radius=14 * scale))
    
    canvas = Image.alpha_composite(canvas, g3)
    canvas = Image.alpha_composite(canvas, g2)
    canvas = Image.alpha_composite(canvas, g1)
    canvas = Image.alpha_composite(canvas, binary_layer)
    canvas = Image.alpha_composite(canvas, orbit_layer)

    # -------------------------------------------------------------------------
    # LEFT SIDE: CLEAN, CRISP, MODERN TYPOGRAPHY & DESIGNATION
    # -------------------------------------------------------------------------
    left_layer = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(left_layer)

    # Fonts with clean scaling
    f_name = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", int(72 * scale))
    f_role = ImageFont.truetype("C:\\Windows\\Fonts\\bahnschrift.ttf", int(30 * scale))
    f_tagline = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", int(19 * scale))
    f_pill = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", int(14 * scale))
    f_badge_font = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", int(14 * scale))
    f_section_title = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", int(13 * scale))
    f_meta = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", int(14 * scale))

    start_x = int(105 * scale)
    
    # 1. Status Pill
    badge_y = int(48 * scale)
    badge_w = int(245 * scale)
    badge_h = int(32 * scale)
    
    ld.rounded_rectangle(
        [(start_x, badge_y), (start_x + badge_w, badge_y + badge_h)],
        radius=int(16 * scale),
        fill=(0, 240, 255, 25),
        outline=(0, 240, 255, 130),
        width=int(1.5 * scale)
    )
    
    dot_r = int(5 * scale)
    dot_cx = start_x + int(18 * scale)
    dot_cy = badge_y + badge_h // 2
    ld.ellipse([(dot_cx - dot_r, dot_cy - dot_r), (dot_cx + dot_r, dot_cy + dot_r)], fill=(0, 255, 170, 255))
    ld.text((start_x + int(34 * scale), badge_y + int(6 * scale)), "FULL STACK DEVELOPER", font=f_pill, fill=(0, 240, 255, 255))
    
    ld.text((start_x + badge_w + int(24 * scale), badge_y + int(7 * scale)), "// DHAKA, BANGLADESH  •  OPEN TO OPPORTUNITIES", font=f_meta, fill=(135, 180, 205, 220))

    # 2. Main Name - Extra crisp and bold
    name_y = int(98 * scale)
    ld.text((start_x, name_y), "MD SHAHARUL SIYAM", font=f_name, fill=(255, 255, 255, 255))
    
    # 3. Glowing Accent Line
    line_y = name_y + int(94 * scale)
    line_w1 = int(620 * scale)
    line_w2 = int(140 * scale)
    line_h = int(4.5 * scale)
    
    # Cyan gradient bar
    ld.rounded_rectangle([(start_x, line_y), (start_x + line_w1, line_y + line_h)], radius=int(2*scale), fill=(0, 230, 255, 255))
    # Emerald accent
    ld.rounded_rectangle([(start_x + line_w1 + int(12*scale), line_y), (start_x + line_w1 + int(12*scale) + line_w2, line_y + line_h)], radius=int(2*scale), fill=(0, 255, 180, 255))
    # Tech dot
    ld.ellipse([(start_x + line_w1 + line_w2 + int(26*scale), line_y - int(1*scale)), 
                (start_x + line_w1 + line_w2 + int(33*scale), line_y + line_h + int(1*scale))], fill=(0, 240, 255, 255))

    # 4. Designation / Role Title
    role_y = line_y + int(20 * scale)
    ld.text((start_x, role_y), "Full Stack Developer  |  React & Node.js Expert", font=f_role, fill=(0, 240, 255, 255))

    # 5. Clean Feature Highlights
    desc_y = role_y + int(50 * scale)
    bullet_items = [
        "Delivering high-quality, full-stack solutions with clean, maintainable code.",
        "Experienced in designing efficient APIs, optimizing frontend performance, and leveraging AWS infrastructure."
    ]
    for idx, text in enumerate(bullet_items):
        by = desc_y + idx * int(28 * scale)
        # Custom sleek circular bullet
        b_dot_r = int(3.5 * scale)
        b_dot_cy = by + int(12 * scale)
        ld.ellipse([(start_x, b_dot_cy - b_dot_r), (start_x + b_dot_r * 2, b_dot_cy + b_dot_r)], fill=(0, 255, 180, 255))
        ld.text((start_x + int(18 * scale), by), text, font=f_tagline, fill=(205, 228, 245, 245))

    # 6. Tech Badges / Stack Pills
    skills_start_y = desc_y + int(68 * scale)
    curr_x = start_x
    curr_y = skills_start_y
    
    ld.text((curr_x, curr_y), "CORE TECH STACK:", font=f_section_title, fill=(110, 175, 205, 230))
    curr_y += int(24 * scale)
    
    skills = [
        "REACT", "NEXT.JS", "NODE.JS", "EXPRESS", "MONGODB", 
        "REACT NATIVE", "AWS", "DOCKER", "TYPESCRIPT", "TAILWIND CSS"
    ]
    
    badge_height = int(30 * scale)
    
    for skill in skills:
        bbox = f_badge_font.getbbox(skill)
        tw = bbox[2] - bbox[0]
        bw = tw + int(24 * scale)
        
        # Sleek dark pill with bright cyan border
        ld.rounded_rectangle(
            [(curr_x, curr_y), (curr_x + bw, curr_y + badge_height)],
            radius=int(6 * scale),
            fill=(10, 22, 38, 235),
            outline=(0, 200, 240, 160),
            width=int(1.5 * scale)
        )
        ld.text((curr_x + int(12 * scale), curr_y + int(6 * scale)), skill, font=f_badge_font, fill=(235, 250, 255, 255))
        
        curr_x += bw + int(10 * scale)

    # 7. Subtle Corner Brackets for Clean Modern Tech Aesthetic
    cb_pad = int(22 * scale)
    cb_len = int(38 * scale)
    cb_w = int(2.5 * scale)
    cb_col = (0, 210, 240, 120)
    
    corners = [
        # Top-left
        [(cb_pad, cb_pad, cb_pad + cb_len, cb_pad), (cb_pad, cb_pad, cb_pad, cb_pad + cb_len)],
        # Bottom-left
        [(cb_pad, banner_h - cb_pad, cb_pad + cb_len, banner_h - cb_pad), (cb_pad, banner_h - cb_pad - cb_len, cb_pad, banner_h - cb_pad)],
    ]
    for corner in corners:
        for line in corner:
            ld.line([(line[0], line[1]), (line[2], line[3])], fill=cb_col, width=cb_w)

    # Composite layers
    canvas = Image.alpha_composite(canvas, left_layer)

    # Downsample with Lanczos for crystal-clear antialiasing
    final_banner = canvas.resize((out_w, out_h), Image.Resampling.LANCZOS)
    final_banner.save("binary-face-banner.png", "PNG", quality=95)
    print("Clean, modern banner successfully generated at binary-face-banner.png!")

if __name__ == "__main__":
    generate_clean_binary_banner()
