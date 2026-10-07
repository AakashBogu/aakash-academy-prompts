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

def build_complete_untruncated_master_prompt(item):
    title = item.get("title", "")
    category = item.get("category", "General AI")
    pid = item.get("id", "0")
    
    clean_title = re.sub(r'^\d+\s*sec\s*', '', title, flags=re.IGNORECASE)
    clean_title = re.sub(r'MASTER PROMPT|ENGINE|v1\.0|v1|ULTRA|VIRAL', '', clean_title, flags=re.IGNORECASE).strip()
    if not clean_title:
        clean_title = title

    return f"""================================================================================
# AAKASH ACADEMY — OFFICIAL MASTER AI PROMPT SYSTEM #{pid}
================================================================================
PROMPT NAME : {title}
CATEGORY    : {category}
AUTHOR      : Aakash Academy AI Engineering Team
COMPATIBLE  : Kling AI 1.5, Seedance 2.0, Google Veo 2, Luma Dream Machine, Runway Gen-3 Alpha, Midjourney v6

--------------------------------------------------------------------------------
[SECTION 1: READY-TO-COPY PRIMARY MASTER PROMPT]
--------------------------------------------------------------------------------
(Copy & Paste the text block below directly into Kling AI, Seedance 2.0, Google Veo 2, or Luma Dream Machine)

Create an ultra-photorealistic 8K resolution cinematic 30-second short film focusing on {clean_title}. The scene opens with an expressive macro detail shot, capturing hyper-realistic textures, volumetric light shafts breaking through atmosphere, and 35mm Arri Alexa anamorphic lens characteristics. Dynamic camera movement with smooth Steadicam tracking panning around the subject. Unreal Engine 5.4 octane render aesthetics, ray-traced shadows, hyper-detailed skin/surface rendering, filmic color grading with deep contrast ratios, award-winning cinematography, dramatic volumetric fog, highly fluid natural motion blur, 60fps ultra-crisp motion performance.

--------------------------------------------------------------------------------
[SECTION 2: 30-SECOND SHOT-BY-SHOT CINEMATIC TIMELINE]
--------------------------------------------------------------------------------
• SHOT 1 — [00:00 to 00:06] (HOOK & INTRODUCTION):
  - Camera Angle : Extreme Macro Close-Up / Low Angle Tilt-Up
  - Action Focus : Establishing scene environment for {clean_title}. Dust motes drift in golden hour rim lighting. High visual impact hook designed for 100% viewer retention on Reels/Shorts.
  - Motion Speed : Slow 0.7x speed with initial rack focus from background to foreground.

• SHOT 2 — [00:06 to 00:14] (ESCATION & DYNAMIC MOVEMENT):
  - Camera Angle : 360-Degree Orbital Steadicam Tracking Shot
  - Action Focus : Dramatic escalation revealing the broader setting and core narrative of {clean_title}. Sunlight sweeps across the frame, highlighting fine textures and dynamic environmental interactions.
  - Lighting     : High-contrast volumetric key light with deep atmospheric fill.

• SHOT 3 — [00:14 to 00:22] (CLIMAX & HIGH-RETENTION PAYOFF):
  - Camera Angle : High-Speed Phantom Flex 4K Slow-Motion (120fps feel)
  - Action Focus : The peak dramatic payoff moment of {clean_title}. Particle impacts, dynamic lighting flares, hyper-detailed physics, vivid color saturation, and striking visual geometry.
  - Depth of Field: Ultra-shallow f/1.4 aperture blur rendering smooth bokeh background elements.

• SHOT 4 — [00:22 to 00:30] (OUTRO RESOLUTION & SHARE HOOK):
  - Camera Angle : Smooth Crane Pull-Back / Cinematic Aerial Reveal
  - Action Focus : Wide cinematic view completing the narrative sequence. Soft golden hour glow setting down, leaving a memorable, loopable closing frame.

--------------------------------------------------------------------------------
[SECTION 3: TECHNICAL CAMERA & RENDER SPECIFICATIONS]
--------------------------------------------------------------------------------
• Camera Rig      : Arri Alexa LF with Cooke Anamorphic /i Full Frame Plus Lenses
• Focal Length    : 35mm & 85mm Prime Combo
• Lighting Setup  : Volumetric Sunbeam Key + Soft Ambient Bounce Light + Soft Rim Highlight
• Color Grade     : Kodak Vision3 500T Film Stock Emulation / Teal & Amber Balance
• Render Engine   : Unreal Engine 5.4 + Octane Render 2026.1 Enterprise
• Resolution      : Native 8K UHD (7680x4320)
• Aspect Ratios   : 9:16 (Shorts / Reels / TikTok) | 16:9 (YouTube 4K HD)

--------------------------------------------------------------------------------
[SECTION 4: AI GENERATOR SPECIFIC OPTIMIZED PRESETS]
--------------------------------------------------------------------------------
• KLING AI v1.5 PRESET:
  Prompt Text : "Cinematic 8K masterpiece video, {clean_title}, volumetric lighting, photorealistic textures, anamorphic lens flare, f/1.8, 60fps."
  Settings    : Mode: Professional | Creativity: 0.7 | Motion: 6 | Aspect Ratio: 9:16

• SEEDANCE 2.0 PRESET:
  Prompt Text : "Hyper-realistic short video of {clean_title}, Unreal Engine 5 render, cinematic lighting, 35mm film grain, 8k resolution, smooth motion."
  Settings    : Quality: Ultra | FPS: 30 | Aspect Ratio: 9:16

• GOOGLE VEO 2 PRESET:
  Prompt Text : "National Geographic cinematic quality video showcasing {clean_title}, dramatic lighting, 8k ultra hd, slow motion panning."
  Settings    : Style: Cinematic | Motion Intensity: High

• LUMA DREAM MACHINE PRESET:
  Prompt Text : "3D cinematic camera pan around {clean_title}, realistic lighting, octane render, vivid colors, photorealistic depth."
  Settings    : Camera Motion: Pan Right + Slow Zoom Out

• MIDJOURNEY v6 (STILL KEYFRAME GENERATION):
  Prompt Text : "{clean_title}, cinematic lighting, photorealistic, shot on 35mm lens, 8k resolution, octane render, award winning photo --ar 9:16 --style raw --v 6.0"

--------------------------------------------------------------------------------
[SECTION 5: COMPREHENSIVE NEGATIVE PROMPT (PASTE IN NEGATIVE BOX)]
--------------------------------------------------------------------------------
blurry, low quality, distorted anatomy, pixelated, watermark, text logo, low resolution, noise, overexposed, artifacting, static background, jerky motion, oversaturated, deformed features, bad framing, duplicate limbs, uncanny valley, CGI render look, low fidelity, plastic skin."""

print(f"Updating all {len(prompts)} prompts with complete, expanded master prompt systems...")

for p in prompts:
    p["prompt_text"] = build_complete_untruncated_master_prompt(p)
    p["is_free"] = True

# Write out prompts_data.js and data/prompts.json
with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
    f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(prompts, indent=2, ensure_ascii=False) + ";")

with open(os.path.join(OUTPUT_DIR, "data", "prompts.json"), "w", encoding="utf-8") as f:
    json.dump(prompts, f, indent=2, ensure_ascii=False)

print("Successfully updated all 389 prompts with complete, detailed master prompt systems!")
