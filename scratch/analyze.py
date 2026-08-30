import numpy as np
from PIL import Image, ImageFilter

def analyze_avatar():
    img = Image.open("avatar.png").convert("RGB")
    arr = np.array(img, dtype=np.float32) # (400, 400, 3)
    H, W, _ = arr.shape
    
    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]
    
    # Check color characteristics
    # Skin detector: (r > 95) & (g > 40) & (b > 20) & (max(r,g,b) - min(r,g,b) > 15) & (abs(r-g) > 15) & (r > g) & (r > b)
    skin_mask = (r > 100) & (g > 50) & (b > 30) & (r > g) & (g > b) & ((r - b) > 25)
    
    # Hair detector (dark top region)
    hair_mask = (r < 75) & (g < 75) & (b < 75)
    
    # Let's save debug masks to see
    Image.fromarray((skin_mask * 255).astype(np.uint8)).save("scratch/debug_skin.png")
    Image.fromarray((hair_mask * 255).astype(np.uint8)).save("scratch/debug_hair.png")
    print("Debug masks saved.")

analyze_avatar()
