import os
import re
import json
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = "https://soniprompts.com"
OUTPUT_DIR = r"c:\Users\Admin\Desktop\python projects\aakash_academy_prompts"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
DATA_DIR = os.path.join(OUTPUT_DIR, "data")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
}

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as res:
            return res.read().decode('utf-8', errors='ignore')
    except:
        return None

def build_master_prompt(title, category, pid):
    clean = re.sub(r'^\d+\s*sec\s*', '', title, flags=re.IGNORECASE)
    clean = re.sub(r'MASTER PROMPT|ENGINE|v1\.0|v1|ULTRA|VIRAL', '', clean, flags=re.IGNORECASE).strip()
    if not clean:
        clean = title
        
    return f"""================================================================================
# AAKASH ACADEMY — COMPLETE MASTER AI PROMPT SYSTEM #{pid}
================================================================================
PROMPT TITLE: {title}
CATEGORY: {category}
TARGET RATIO: 9:16 (Shorts / Reels / TikTok) & 16:9 (4K Widescreen)

--------------------------------------------------------------------------------
[1] PRIMARY GENERATION PROMPT (Paste into AI Video Tool)
--------------------------------------------------------------------------------
Ultra-photorealistic 8K cinematic video of {clean}. Shot on 35mm Arri Alexa camera, Master Anamorphic lens, f/1.8 aperture, hyper-detailed textures, volumetric atmosphere, Octane render quality, Unreal Engine 5 lighting, natural motion blur, award-winning cinematography.

--------------------------------------------------------------------------------
[2] 30-SECOND SHOT-BY-SHOT BREAKDOWN
--------------------------------------------------------------------------------
• Shot 1 [00:00 - 00:06] (Opening Hook):
  Macro close-up shot introducing {clean}. High-contrast lighting with volumetric dust particles floating in light beam. Sharp focus on key details.

• Shot 2 [00:06 - 00:14] (Dynamic Panning & Escalation):
  Smooth low-angle dolly tracking shot expanding to reveal full environment. Dynamic camera pan smoothly following movement with shallow depth of field.

• Shot 3 [00:14 - 00:22] (Climax Payoff):
  High-speed cinematic slow-motion sequence capturing key action of {clean}. Vibrant color grading, crisp highlights, ambient atmospheric depth.

• Shot 4 [00:22 - 00:30] (Resolution & Outro Hook):
  Wide slow pull-back camera motion leaving lasting visual impact. Soft rim lighting with natural color balance.

--------------------------------------------------------------------------------
[3] LENS & CINEMATOGRAPHY SPECIFICATIONS
--------------------------------------------------------------------------------
• Lens: 35mm Prime Anamorphic
• Camera Motion: Smooth Steadicam Tracking + Low-Angle Dolly Pan
• Lighting: Volumetric Golden Hour / Studio Key Contrast
• Render Quality: Unreal Engine 5.4 + Octane Render 8K

--------------------------------------------------------------------------------
[4] RECOMMENDED AI VIDEO GENERATORS & SETTINGS
--------------------------------------------------------------------------------
• Kling AI 1.5: Professional Mode | Motion: 6 | Creativity: 0.7
• Seedance 2.0: High Quality Mode | FPS: 30 | Aspect Ratio: 9:16
• Google Veo 2: Cinematic Style | Motion Scale: High
• Luma Dream Machine: Camera Motion > Pan Right + Zoom Out
• Runway Gen-3 Alpha: Motion Brush Active | Speed: 1.2

--------------------------------------------------------------------------------
[5] NEGATIVE PROMPT (Paste in Negative Prompt Box)
--------------------------------------------------------------------------------
blurry, low resolution, distorted faces, duplicate limbs, pixelated, watermark, text logo, low quality, noise, overexposed, artifacting, static background, jerky motion."""

def run_build():
    prompts = []
    seen = set()
    
    print("Building full dataset for all available pages...")
    for pg in range(1, 27):
        url = f"{BASE_URL}/browse.php?pg={pg}"
        html = fetch(url)
        if not html:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.pcard, .prow, .mq-card')
        
        for card in cards:
            href = card.get('href', '')
            if not href:
                a_tag = card.select_one('a[href*="prompt.php"]')
                if a_tag:
                    href = a_tag.get('href', '')
            m = re.search(r'id=(\d+)', href)
            if not m:
                continue
            pid = m.group(1)
            if pid in seen:
                continue
                
            title_el = card.select_one('.pcard-title, h3, .prow-body h3')
            title = title_el.text.strip() if title_el else f"Master AI Prompt #{pid}"
            cat_el = card.select_one('.pcard-cat, .prow-cat')
            cat = cat_el.text.strip().replace('🗂', '').strip() if cat_el else "General AI"
            if not cat or "prompt" in cat.lower():
                cat = "General AI"
                
            img_el = card.select_one('img')
            img_src = img_el.get('src', '') if img_el else ''
            if img_src.startswith('/'):
                img_src = BASE_URL + img_src
                
            img_local = f"images/prompt_{pid}.png"
            full_img_path = os.path.join(OUTPUT_DIR, img_local)
            if not os.path.exists(full_img_path):
                img_local = img_src
                
            seen.add(pid)
            prompts.append({
                "id": pid,
                "title": title,
                "category": cat,
                "image": img_local,
                "is_free": True,
                "views": f"{(int(pid) * 37) % 4800 + 600}",
                "likes": f"{(int(pid) * 19) % 1800 + 240}",
                "prompt_text": build_master_prompt(title, cat, pid)
            })

    print(f"Total compiled prompts: {len(prompts)}")
    with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
        f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(prompts, indent=2, ensure_ascii=False) + ";")
    with open(os.path.join(DATA_DIR, "prompts.json"), "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    print("Dataset compiled successfully!")

if __name__ == "__main__":
    run_build()
