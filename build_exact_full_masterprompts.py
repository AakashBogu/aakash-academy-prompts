import os
import re
import json

OUTPUT_DIR = r"c:\Users\Admin\Desktop\python projects\aakash_academy_prompts"
DATA_FILE = os.path.join(OUTPUT_DIR, "data", "prompts.json")

if not os.path.exists(DATA_FILE):
    print("Error: data/prompts.json not found!")
    exit(1)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    prompts = json.load(f)

def generate_exact_full_prompt(item):
    title = item.get("title", "").strip()
    category = item.get("category", "General AI").strip()
    pid = item.get("id", "0")
    
    # Extract subject name cleanly
    clean_title = re.sub(r'^\d+\s*sec\s*', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'MASTER PROMPT|ENGINE|v1\.0|v1|ULTRA|VIRAL|3D|3DCARTOON', '', clean_title, flags=re.IGNORECASE).strip()
    if not clean_title or len(clean_title) < 3:
        clean_title = title

    return f"""MASTER PROMPT: {title}

PROMPT OVERVIEW:
A high-retention 30-second short video designed for YouTube Shorts, Instagram Reels, and TikTok featuring {clean_title}. Shot with cinematic quality, hyper-realistic detail, volumetric lighting, and fluid motion.

================================================================================
SECTION 1: MAIN PROMPT FOR AI VIDEO GENERATORS (KLING AI / SEEDANCE 2.0 / VEO 2 / LUMA)
================================================================================
A photorealistic 8K resolution cinematic 30-second video of {clean_title}. Extremely detailed visual textures, 35mm Arri Alexa camera movement, Master Anamorphic prime lens, f/1.8 depth of field. Volumetric atmosphere with golden hour sun shafts breaking through the background. Dynamic camera pan smoothly tracking the main subject. Unreal Engine 5.4 octane render aesthetics, ray-traced shadows, hyper-detailed surface details, filmic color grading, professional cinematography, 60fps fluid natural motion blur.

================================================================================
SECTION 2: STEP-BY-STEP 30-SECOND SCENE TIMELINE
================================================================================
00:00 - 00:06 (SCENE 1: THE OPENING HOOK):
- Camera Shot: Macro close-up focusing directly on {clean_title}.
- Visuals: Dust particles floating in high-contrast volumetric rim lighting. Sharp focus on key details.
- Audio / SFX: Deep cinematic bass drop with crisp ASMR audio detail.

00:06 - 00:14 (SCENE 2: ESCALATION & DYNAMIC MOTION):
- Camera Shot: 360-degree orbital Steadicam tracking shot moving smoothly around the scene.
- Visuals: The camera pans across the environment to reveal dramatic depth and action. Sunlight sweeps across the background highlighting realistic reflections.

00:14 - 00:22 (SCENE 3: THE CLIMAX & HIGH-RETENTION PAYOFF):
- Camera Shot: High-speed 120fps slow-motion sequence capturing the primary action peak of {clean_title}.
- Visuals: Particle effects, vivid color saturation, sharp optics, and ultra-shallow bokeh background blur.

00:22 - 00:30 (SCENE 4: RESOLUTION & SHARE HOOK):
- Camera Shot: Wide slow pull-back camera motion leaving a memorable visual impact.
- Visuals: Soft golden hour lighting settling down, creating a seamlessly loopable video finish.

================================================================================
SECTION 3: AI ENGINE CONFIGURATION & PRESETS
================================================================================
• KLING AI 1.5:
  - Prompt: "Cinematic 8K video of {clean_title}, volumetric sunbeams, photorealistic 35mm camera pan, 60fps."
  - Settings: Mode: Professional | Motion: 6 | Aspect Ratio: 9:16

• SEEDANCE 2.0:
  - Prompt: "Hyper-realistic short video of {clean_title}, Unreal Engine 5 render, cinematic lighting, 8k resolution, smooth motion."
  - Settings: Quality: Ultra | FPS: 30 | Aspect Ratio: 9:16

• GOOGLE VEO 2:
  - Prompt: "National Geographic cinematic quality video showcasing {clean_title}, dramatic lighting, 8k ultra hd, slow motion panning."
  - Settings: Style: Cinematic | Motion Scale: High

================================================================================
SECTION 4: COMPREHENSIVE NEGATIVE PROMPT
================================================================================
blurry, low quality, distorted anatomy, pixelated, watermark, text logo, low resolution, noise, overexposed, artifacting, static background, jerky motion, oversaturated, deformed features, bad framing, duplicate limbs, uncanny valley, CGI render look, low fidelity, plastic skin."""

print(f"Generating exact full master prompts for all {len(prompts)} items...")

for item in prompts:
    item["prompt_text"] = generate_exact_full_prompt(item)
    item["is_free"] = True

# Save output to prompts_data.js and data/prompts.json
with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
    f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(prompts, indent=2, ensure_ascii=False) + ";")

with open(os.path.join(OUTPUT_DIR, "data", "prompts.json"), "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

print("All master prompts updated with exact full content successfully!")
