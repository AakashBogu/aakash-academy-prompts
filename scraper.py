import os
import re
import json
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

BASE_URL = "https://soniprompts.com"
OUTPUT_DIR = r"c:\Users\Admin\Desktop\python projects\aakash_academy_prompts"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
DATA_DIR = os.path.join(OUTPUT_DIR, "data")

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_url(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def download_image(img_url, filename):
    filepath = os.path.join(IMAGES_DIR, filename)
    if os.path.exists(filepath):
        return f"images/{filename}"
    try:
        req = urllib.request.Request(img_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response, open(filepath, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Downloaded image: {filename}")
        return f"images/{filename}"
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}")
        return img_url

def parse_prompts():
    prompts = []
    seen_ids = set()
    
    # We will crawl pages 1 to 10 of browse.php
    for page in range(1, 11):
        print(f"Fetching browse page {page}...")
        url = f"{BASE_URL}/browse.php?pg={page}"
        html = fetch_url(url)
        if not html:
            continue
            
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('.pcard, .prow, .mq-card')
        
        # Also parse marquee cards on home page if page == 1
        if page == 1:
            home_html = fetch_url(BASE_URL)
            if home_html:
                home_soup = BeautifulSoup(home_html, 'html.parser')
                mq_cards = home_soup.select('.mq-card')
                for mq in mq_cards:
                    href = mq.get('href', '')
                    match = re.search(r'id=(\d+)', href)
                    if not match:
                        continue
                    p_id = match.group(1)
                    if p_id in seen_ids:
                        continue
                    img_tag = mq.select_one('img')
                    cap_tag = mq.select_one('.mq-cap')
                    title = cap_tag.text.strip() if cap_tag else (img_tag.get('alt', '').strip() if img_tag else f"Prompt #{p_id}")
                    img_src = img_tag.get('src', '') if img_tag else ''
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
                        "category": "Featured",
                        "image": local_img or img_src,
                        "original_img": img_src,
                        "is_free": True,
                        "views": f"{(int(p_id) * 41) % 4500 + 800}",
                        "likes": f"{(int(p_id) * 23) % 1500 + 230}",
                        "prompt_text": generate_master_prompt(title, "Featured")
                    })
        
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
                "is_free": True, # All free for Aakash Academy!
                "views": f"{(int(p_id) * 37) % 3500 + 400}",
                "likes": f"{(int(p_id) * 19) % 1200 + 120}",
                "prompt_text": generate_master_prompt(title, category)
            })

    print(f"Total extracted prompts: {len(prompts)}")
    with open(os.path.join(DATA_DIR, "prompts.json"), "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
        
    # Write JS file for frontend
    with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
        f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(prompts, indent=2, ensure_ascii=False) + ";")
        
    print("Prompts dataset written successfully!")

def generate_master_prompt(title, category):
    clean_title = re.sub(r'^\d+\s*sec\s*', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'MASTER PROMPT|ENGINE|v1\.0|v1|ULTRA', '', clean_title, flags=re.IGNORECASE).strip()
    
    return f"""[AAKASH ACADEMY MASTER AI PROMPT]
Subject: {clean_title}
Category: {category}
Style & Atmosphere: Ultra-photorealistic 8K resolution, cinematic lighting, hyper-detailed textures, Unreal Engine 5 render, volumetric atmosphere, Octane render quality.
Camera Settings: 35mm lens, shallow depth of field, dynamic panning motion, smooth motion blur, filmic color grading.
Action Breakdown:
- 00:00 - 00:10: High-impact opening hook featuring detailed focus on main subject ({clean_title}).
- 00:10 - 00:20: Escalating dynamic camera movement with cinematic reveal and volumetric lighting effects.
- 00:20 - 00:30: Satisfying climax payoff, vibrant colors, perfectly crisp focus and atmospheric depth.
Recommended AI Engines: Kling AI v1.5, Seedance 2.0, Google Veo 2, Luma Dream Machine, Runway Gen-3 Alpha, Midjourney v6.
Aspect Ratio: 9:16 (Vertical Shorts / Reels / TikTok) & 16:9 (Horizontal YouTube HD)
Negative Prompt: Blurry, low quality, distorted anatomy, pixelated, watermark, text logo, low resolution, noise, overexposed."""

if __name__ == "__main__":
    parse_prompts()
