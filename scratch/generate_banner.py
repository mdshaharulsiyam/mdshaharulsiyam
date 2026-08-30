import os
import random
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def generate_ultimate_binary_banner():
    banner_w, banner_h = 2240, 528
    
    # Fine grid with good balance of density and readability
    step_x = 8
    step_y = 12
    font_size = 12
    
    cols = banner_w // step_x
    rows = banner_h // step_y
    
    font_mono = ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", font_size)
    font_mono_bold = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", font_size)
    
    # =========================================================================
    # MASTER DESIGN MAP - Everything rasterized for binary sampling
    # =========================================================================
    master_map = Image.new("RGBA", (banner_w, banner_h), (0, 0, 0, 0))
    md = ImageDraw.Draw(master_map)
    
    f_title = ImageFont.truetype("C:\\Windows\\Fonts\\ariblk.ttf", 72)
    f_sub = ImageFont.truetype("C:\\Windows\\Fonts\\bahnschrift.ttf", 28)
    f_tag = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 16)
    f_badge = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 15)
    f_xs = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf", 13)

    # --- Corner brackets (thicker for visibility) ---
    bp, bl = 16, 44
    for corners in [
        [(bp, bp, bp+bl, bp), (bp, bp, bp, bp+bl)],
        [(banner_w-bp-bl, bp, banner_w-bp, bp), (banner_w-bp, bp, banner_w-bp, bp+bl)],
        [(bp, banner_h-bp, bp+bl, banner_h-bp), (bp, banner_h-bp-bl, bp, banner_h-bp)],
        [(banner_w-bp-bl, banner_h-bp, banner_w-bp, banner_h-bp), (banner_w-bp, banner_h-bp-bl, banner_w-bp, banner_h-bp)],
    ]:
        for c in corners:
            md.line([(c[0], c[1]), (c[2], c[3])], fill=(0, 255, 240, 255), width=5)

    # --- Top Status Bar ---
    md.rectangle([(85, 40), (370, 78)], outline=(0, 250, 255, 255), width=3, fill=(0, 210, 250, 200))
    md.ellipse([(104, 52), (120, 68)], fill=(0, 255, 180, 255))
    md.text((132, 48), "SYSTEM.INIT // ONLINE", font=f_badge, fill=(255, 255, 255, 255))
    md.text((395, 50), "[ LOC: 23.7771°N 90.3994°E | DHAKA, BANGLADESH ]", font=f_tag, fill=(0, 240, 255, 245))
    md.text((950, 50), "[ 0x7F // UPLINK: ACTIVE ]", font=f_xs, fill=(0, 220, 240, 220))

    # --- MAIN NAME (extra bold, extra large for maximum binary density) ---
    name_x, name_y = 85, 92
    # Draw it twice offset for extra boldness
    md.text((name_x+1, name_y+1), "MD SHAHARUL SIYAM", font=f_title, fill=(200, 255, 255, 255))
    md.text((name_x, name_y), "MD SHAHARUL SIYAM", font=f_title, fill=(255, 255, 255, 255))
    
    # Glowing underline accent bars
    md.rectangle([(name_x, name_y + 82), (name_x + 740, name_y + 88)], fill=(0, 255, 240, 255))
    md.rectangle([(name_x + 748, name_y + 82), (name_x + 850, name_y + 88)], fill=(0, 255, 180, 255))

    # --- Subtitle / Role ---
    md.text((name_x, 192), "FULL-STACK DEVELOPER  •  MERN & CLOUD SPECIALIST", font=f_sub, fill=(0, 250, 235, 255))

    # --- Descriptive Bullets ---
    desc = [
        "> Scalable Backend Architectures, Real-Time Systems & Microservices",
        "> React / Next.js  •  Node.js & Express  •  React Native  •  AWS Cloud",
        "> Modern UI/UX Engineering, High-Performance Web & Mobile Solutions"
    ]
    for i, line in enumerate(desc):
        md.text((name_x, 240 + i * 28), line, font=f_tag, fill=(210, 248, 255, 250))

    # --- Tech Badges (drawn as filled rectangles with bold text) ---
    badges = ["REACT", "NEXT.JS", "NODE.JS", "EXPRESS", "MONGODB", "REACT NATIVE", "AWS", "DOCKER", "TYPESCRIPT", "TAILWIND", "GRAPHQL"]
    bx, by = 85, 340
    cur_x, cur_y = bx, by
    md.text((bx, by - 24), "CORE_COMPETENCIES // TECH_STACK:", font=f_xs, fill=(0, 225, 245, 240))
    
    for badge in badges:
        bbox = f_badge.getbbox(badge)
        bw = bbox[2] - bbox[0] + 28
        bh = 32
        if cur_x + bw > 1480:
            cur_x = bx
            cur_y += 40
        md.rectangle([(cur_x, cur_y), (cur_x + bw, cur_y + bh)], outline=(0, 250, 255, 255), width=3, fill=(0, 210, 245, 200))
        md.text((cur_x + 14, cur_y + 6), badge, font=f_badge, fill=(255, 255, 255, 255))
        cur_x += bw + 14

    # --- Terminal Prompt ---
    term_y = 455
    md.rectangle([(85, term_y - 14), (1500, term_y - 12)], fill=(0, 200, 230, 180))
    md.text((85, term_y), "visitor@siyam-terminal:~$", font=f_tag, fill=(0, 255, 180, 255))
    md.text((370, term_y), "git commit -m 'Building the future with scalable code' _", font=f_tag, fill=(240, 252, 255, 250))

    # =========================================================================
    # CIRCLE FRAME (with orbital binary ring and ticks)
    # =========================================================================
    circle_r = 210
    circle_cx = banner_w - circle_r - 115
    circle_cy = banner_h // 2
    
    # Main circle ring (thick for strong binary definition)
    for offset in range(-2, 3):
        md.ellipse([(circle_cx-circle_r+offset, circle_cy-circle_r+offset),
                     (circle_cx+circle_r-offset, circle_cy+circle_r-offset)],
                    outline=(0, 255, 245, 255), width=2)
    
    # Outer orbit ring
    r_out = circle_r + 16
    md.ellipse([(circle_cx-r_out, circle_cy-r_out), (circle_cx+r_out, circle_cy+r_out)],
               outline=(0, 200, 235, 220), width=2)
    
    # Orbital ticks
    for i in range(60):
        angle = 2 * math.pi * i / 60
        tick_len = 14 if i % 5 == 0 else 8
        tx1 = circle_cx + (circle_r + 16) * math.cos(angle)
        ty1 = circle_cy + (circle_r + 16) * math.sin(angle)
        tx2 = circle_cx + (circle_r + 16 + tick_len) * math.cos(angle)
        ty2 = circle_cy + (circle_r + 16 + tick_len) * math.sin(angle)
        w = 3 if i % 5 == 0 else 2
        md.line([(tx1, ty1), (tx2, ty2)], fill=(0, 255, 210, 255), width=w)

    # Circle top/bottom cyber labels
    md.rectangle([(circle_cx-100, circle_cy-circle_r-20), (circle_cx+100, circle_cy-circle_r+4)], fill=(0, 240, 255, 255))
    md.text((circle_cx-86, circle_cy-circle_r-17), "[ 01001101 01000100 ]", font=f_xs, fill=(0, 8, 16, 255))
    
    md.rectangle([(circle_cx-82, circle_cy+circle_r-4), (circle_cx+82, circle_cy+circle_r+20)], fill=(0, 255, 190, 255))
    md.text((circle_cx-70, circle_cy+circle_r-1), "IDENTITY: VERIFIED", font=f_xs, fill=(0, 8, 16, 255))

    # =========================================================================
    # AVATAR PORTRAIT PROCESSING
    # =========================================================================
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
    ftly = circle_cy - fbs // 2 + 15

    master_np = np.array(master_map, dtype=np.float32)

    # =========================================================================
    # RENDER: 100% PURE BINARY GRID — EVERY PIXEL IS A 0 OR 1
    # =========================================================================
    canvas = Image.new("RGBA", (banner_w, banner_h), (2, 4, 8, 255))
    tl = Image.new("RGBA", (banner_w, banner_h), (0,0,0,0))
    td = ImageDraw.Draw(tl)
    gl = Image.new("RGBA", (banner_w, banner_h), (0,0,0,0))
    gd = ImageDraw.Draw(gl)

    random.seed(31337)
    
    # Reduce visual noise: disable rain and scanlines
    col_active = [False for _ in range(cols)]  # No rain columns
    row_band = [0.0 for _ in range(rows)]

    for ri in range(rows):
        y = ri * step_y
        rb = row_band[ri]
        
        for ci in range(cols):
            x = ci * step_x
            char = random.choice(['0', '1'])
            
            sx = min(banner_w - 1, x + step_x // 2)
            sy = min(banner_h - 1, y + step_y // 2)
            
            dx = sx - circle_cx
            dy = sy - circle_cy
            dist = math.sqrt(dx*dx + dy*dy)
            inside_circle = dist <= circle_r
            
            if inside_circle:
                # AVATAR PORTRAIT in binary
                ix = sx - ftlx
                iy = sy - ftly
                in_face = (0 <= ix < fbs) and (0 <= iy < fbs)
                mv = s_mask[iy, ix] if in_face else 0.0
                ev = max(0.0, min(1.0, (circle_r - dist) / 8.0))
                
                if in_face and mv > 0.18:
                    is_skin = s_skin[iy, ix] > 0.25
                    is_dark = s_dark[iy, ix] > 0.25
                    gv = s_gray[iy, ix]
                    edv = s_edge[iy, ix]
                    
                    if is_skin:
                        lum = (gv * 0.72 + edv * 0.4) * ev
                        if lum > 0.50:
                            td.text((x,y), char, font=font_mono_bold, fill=(255,255,255,255))
                            gd.text((x,y), char, font=font_mono_bold, fill=(0,255,240,255))
                        elif lum > 0.30:
                            td.text((x,y), char, font=font_mono, fill=(15,248,228,245))
                            gd.text((x,y), char, font=font_mono, fill=(0,218,218,175))
                        elif lum > 0.16:
                            td.text((x,y), char, font=font_mono, fill=(0,198,188,205))
                            gd.text((x,y), char, font=font_mono, fill=(0,145,162,85))
                        else:
                            td.text((x,y), char, font=font_mono, fill=(0,148,158,185))
                    elif is_dark:
                        if edv > 0.15:
                            td.text((x,y), char, font=font_mono, fill=(0,192,188,215))
                            gd.text((x,y), char, font=font_mono, fill=(0,142,162,95))
                        elif mv > 0.45:
                            td.text((x,y), char, font=font_mono, fill=(0,122,138,165))
                        else:
                            td.text((x,y), char, font=font_mono, fill=(0,78,95,115))
                    else:
                        # Simplified avatar rendering based on grayscale only
                        gray_val = s_gray[iy, ix]
                        if gray_val > 0.5:
                            td.text((x,y), char, font=font_mono_bold, fill=(255,255,255,255))
                        else:
                            td.text((x,y), char, font=font_mono, fill=(0,200,200,255))
                else:
                    # Circle interior simple background
                    td.text((x,y), char, font=font_mono, fill=(0,120,150,255))
            else:
                # OUTSIDE CIRCLE — Simplified rendering from master map only
                px = master_np[sy, sx]
                pr, pg2, pb, pa = px[0], px[1], px[2], px[3]
                if pa > 30:
                    lum = (0.299*pr + 0.587*pg2 + 0.114*pb) / 255.0
                    if lum > 0.5:
                        td.text((x,y), char, font=font_mono_bold, fill=(255,255,255,255))
                    else:
                        td.text((x,y), char, font=font_mono, fill=(0,140,180,255))

    # Multi-stage Neon Gaussian Bloom
    g1 = gl.filter(ImageFilter.GaussianBlur(radius=1.5))
    g2 = gl.filter(ImageFilter.GaussianBlur(radius=4.0))
    g3 = gl.filter(ImageFilter.GaussianBlur(radius=10.0))
    g4 = gl.filter(ImageFilter.GaussianBlur(radius=18.0))  # Extra wide bloom

    # Composite
    final = Image.alpha_composite(canvas, g4)
    final = Image.alpha_composite(final, g3)
    final = Image.alpha_composite(final, g2)
    final = Image.alpha_composite(final, g1)
    final = Image.alpha_composite(final, tl)

    final.save("binary-face-banner.png", "PNG", quality=95)
    print("Ultimate Enhanced Binary Matrix Banner saved!")

if __name__ == "__main__":
    generate_ultimate_binary_banner()
