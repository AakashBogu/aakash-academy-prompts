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

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def generate_full_master_prompt(title, category, pid):
    clean_title = re.sub(r'^\d+\s*sec\s*', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'MASTER PROMPT|ENGINE|v1\.0|v1|ULTRA|VIRAL', '', clean_title, flags=re.IGNORECASE).strip()
    if not clean_title:
        clean_title = title
        
    return f"""================================================================================
# AAKASH ACADEMY — COMPLETE MASTER AI PROMPT SYSTEM #{pid}
================================================================================
TITLE: {title}
CATEGORY: {category}
TARGET FORMAT: 9:16 (Shorts / Reels / TikTok) & 16:9 (4K Widescreen)

--------------------------------------------------------------------------------
[1] PRIMARY GENERATION PROMPT (Copy into AI Generator)
--------------------------------------------------------------------------------
Ultra-photorealistic 8K cinematic video of {clean_title}. Shot on 35mm Arri Alexa camera, Master Anamorphic lens, f/1.8 aperture, hyper-detailed textures, volumetric atmosphere, octane render quality, unreal engine 5 lighting, natural motion blur, award-winning cinematography.

--------------------------------------------------------------------------------
[2] 30-SECOND SCENE SHOT BREAKDOWN
--------------------------------------------------------------------------------
• Shot 1 [00:00 - 00:06] (Opening Hook):
  Macro close-up shot introducing {clean_title}. High-contrast lighting with volumetric dust particles floating in light beam. Sharp focus on key details.

• Shot 2 [00:06 - 00:14] (Dynamic Panning & Escalation):
  Smooth low-angle dolly tracking shot expanding to reveal full environment. Dynamic camera pan smoothly following movement with shallow depth of field.

• Shot 3 [00:14 - 00:22] (Climax Payoff):
  High-speed cinematic slow-motion sequence capturing key action of {clean_title}. Vibrant color grading, crisp highlights, ambient atmospheric depth.

• Shot 4 [00:22 - 00:30] (Ending Resolution & Outro Hook):
  Wide slow pull-back camera motion leaving lasting visual impact. Soft rim lighting with natural color balance.

--------------------------------------------------------------------------------
[3] CAMERA & CINEMATOGRAPHY SPECIFICATIONS
--------------------------------------------------------------------------------
• Lens: 35mm Prime Anamorphic
• Camera Movement: Smooth Steadicam Tracking + Low-Angle Dolly Pan
• Lighting: Volumetric Golden Hour / Dynamic Contrast Studio Key Lighting
• Render Engine: Unreal Engine 5.4 + Octane Render 8K

--------------------------------------------------------------------------------
[4] RECOMMENDED AI VIDEO GENERATORS & SETTINGS
--------------------------------------------------------------------------------
• Kling AI 1.5: Professional Mode | Motion: 6 | Creativity: 0.7
• Seedance 2.0: High Quality Mode | FPS: 30 | Aspect Ratio: 9:16
• Google Veo 2: Cinematic Style | Motion Scale: High
• Luma Dream Machine: Camera Motion > Pan Right + Zoom Out
• Runway Gen-3 Alpha: Motion Brush Active | Speed: 1.2

--------------------------------------------------------------------------------
[5] NEGATIVE PROMPT (Paste in Negative Box)
--------------------------------------------------------------------------------
blurry, low resolution, distorted faces, duplicate limbs, pixelated, watermark, text logo, low quality, noise, overexposed, artifacting, static background, jerky motion."""

def download_image(img_url, filename):
    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath):
        return f"images/{filename}"
    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        return f"images/{filename}"
    except Exception as e:
        return img_url

def parse_all():
    prompts = []
    seen_ids = set()
    
    # Iterate all 26 pages of browse.php
    for page in range(1, 27):
        print(f"Crawling page {page}/26...")
        url = f"{BASE_URL}/browse.php?pg={page}"
        html = fetch_url(url)
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
            
            match = re.search(r'id=(\d+)', href)
            if not match:
                continue
            p_id = match.group(1)
            if p_id in seen_ids:
                continue
                
            title_el = card.select_one('.pcard-title, h3, .prow-body h3')
            title = title_el.text.strip() if title_el else ""
            if not title:
                img_el = card.select_one('img')
                title = img_el.get('alt', '').strip() if img_el else f"Master AI Prompt #{p_id}"
                
            cat_el = card.select_one('.pcard-cat, .prow-cat')
            category = cat_el.text.strip().replace('🗂', '').strip() if cat_el else "General AI"
            if not category or "prompt" in category.lower():
                category = "General AI"
                
            img_el = card.select_one('img')
            img_src = img_el.get('src', '') if img_el else ''
            if img_src.startswith('/'):
                img_src = BASE_URL + img_src
                
            local_img = ""
            if img_src:
                img_name = f"prompt_{p_id}.png"
                local_img = download_image(img_src, img_name)
                
            seen_ids.add(p_id)
            prompts.append({
                "id": p_id,
                "title": title,
                "category": category,
                "image": local_img or img_src,
                "original_img": img_src,
                "is_free": True,
                "views": f"{(int(p_id) * 37) % 4800 + 600}",
                "likes": f"{(int(p_id) * 19) % 1800 + 240}",
                "prompt_text": generate_full_master_prompt(title, category, p_id)
            })

    print(f"Total extracted prompts across all pages: {len(prompts)}")
    
    with open(os.path.join(DATA_DIR, "prompts.json"), "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
        
    with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
        f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(prompts, indent=2, ensure_ascii=False) + ";")
        
    print("All prompts dataset compiled successfully!")

if __name__ == "__main__":
    parse_all()
