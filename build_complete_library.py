import subprocess
import json
import re
import os

OUTPUT_DIR = r"c:\Users\Admin\Desktop\python projects\aakash_academy_prompts"
DATA_DIR = os.path.join(OUTPUT_DIR, "data")

# 1. Load the 389 existing prompts from git HEAD
raw_head = subprocess.check_output(['git', 'show', 'HEAD:data/prompts.json'], cwd=OUTPUT_DIR, encoding='utf-8')
existing_prompts = json.loads(raw_head)
print(f"Loaded {len(existing_prompts)} prompts from git HEAD.")

# 2. Load the 39 new prompts from new_prompts_meta.json
with open(os.path.join(OUTPUT_DIR, 'new_prompts_meta.json'), 'r', encoding='utf-8') as f:
    new_meta = json.load(f)
print(f"Loaded {len(new_meta)} prompts from new_prompts_meta.json.")

def clean_text(s):
    if not s:
        return ""
    # Clean broken Unicode replacement character and entities
    s = s.replace('\ufffd', '—').replace('&amp;', '&').replace('&quot;', '"').replace('&#039;', "'")
    s = s.replace('—', '—')
    s = s.replace('\u2192', '->').replace('\u2190', '<-')
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def extract_core_subject(title):
    t = clean_text(title)
    # Remove prefixes like MASTER PROMPT, ULTRA, 30-SECOND, ENGINE, etc.
    sub = re.sub(r'^\d+\s*sec(ond)?\s*', '', t, flags=re.IGNORECASE)
    sub = re.sub(r'^MASTER\s+PROMPT\s*[-—:]*\s*', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'^ULTRA\s+MASTER\s+PROMPT\s*[-—:]*\s*', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'^VIRAL\s+', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'\s*ENGINE\s*$', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'\s*CONTENT\s*SYSTEM\s*$', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'\s*VIDEO\s*ENGINE\s*$', '', sub, flags=re.IGNORECASE)
    sub = re.sub(r'\s*v\d+(\.\d+)?\s*$', '', sub, flags=re.IGNORECASE)
    sub = sub.strip(' -—:')
    if not sub or len(sub) < 3:
        sub = t
    return sub

def format_complete_master_prompt(pid, raw_title, category):
    title = clean_text(raw_title)
    subject = extract_core_subject(title)
    
    return f"""MASTER PROMPT: {title}

[AI VIDEO ENGINE SPECIFICATIONS]
• Target AI Tools: Kling AI 1.5/2.0, Seedance 2.0/2.5, Google Veo 2, Luma Dream Machine, Runway Gen-3 Alpha, Midjourney v6
• Video Duration: 30 Seconds High-Retention Viral Reel / Short / TikTok
• Aspect Ratio: 9:16 (Vertical Fullscreen 1080x1920 / 4K) & 16:9 (Horizontal 3840x2160)
• Resolution & Quality: 8K Ultra-HD, 60fps, Photorealistic CGI & Real Cinema Fusion
• Category: {category}

================================================================================
[1] PRIMARY MASTER PROMPT (COPY DIRECTLY INTO AI VIDEO GENERATOR)
================================================================================
A hyper-realistic 8K resolution cinematic 30-second short video of {subject}. Shot on 35mm Arri Alexa LF with Master Anamorphic prime lenses, f/1.8 aperture, natural shallow depth of field, creamy background bokeh highlights. Volumetric atmospheric haze with dynamic golden hour sunbeam shafts piercing through the environment. Unreal Engine 5.4 and Octane Render ray-traced lighting, physically accurate micro-textures, authentic reflections, subsurface scattering on organic surfaces, hyper-detailed particle dynamics. Smooth mechanical Steadicam tracking movement, natural fluid motion blur, zero AI warping, perfectly consistent physics, 60fps high frame rate clarity. Filmic Kodak Vision3 500T color grading with deep rich contrast and vivid cinematic tones.

================================================================================
[2] 30-SECOND STEP-BY-STEP SCENE TIMELINE BREAKDOWN
================================================================================
• SHOT 1 — [00:00 to 00:06] (THE 3-SECOND INSTANT HOOK):
  - Camera Shot: Macro Close-Up / Low-Angle Dramatic Push-In
  - Visual Action: Immediate high-impact introduction of {subject}. Volumetric light rays highlight intricate surface textures. Dust motes and atmospheric particles float in the rim lighting.
  - Pacing & Dynamics: Smooth subtle acceleration with initial rack focus from background to foreground. Engineered for 100% viewer retention in the first 3 seconds.
  - Audio / SFX Cue: Low-frequency cinematic sub-bass drop with crisp tactile ASMR audio detail.

• SHOT 2 — [00:06 to 00:14] (ESCALATION & ENVIRONMENT REVEAL):
  - Camera Shot: 360-Degree Orbital Steadicam Tracking Arc Shot
  - Visual Action: The camera smoothly glides around {subject}, expanding the visual scale to reveal the broader setting. Dynamic lighting shifts across the frame, highlighting realistic reflections and environmental interaction.
  - Lighting Dynamics: High-contrast volumetric key light with soft atmospheric fill and natural specular highlights.
  - Pacing: Continuous fluid motion with realistic physics and depth.

• SHOT 3 — [00:14 to 00:22] (THE HIGH-RETENTION CLIMAX & PAYOFF):
  - Camera Shot: High-Speed Phantom Flex 4K Slow-Motion (120fps sensation)
  - Visual Action: The core visual payoff and peak dramatic moment of {subject}. Hyper-crisp micro-details, particle dispersion, intense visual energy, ultra-clean edges, and deep dimensional perspective.
  - Depth of Field: Ultra-shallow f/1.4 aperture blur melting background elements into silky bokeh.
  - Audio / SFX Cue: Rising cinematic riser peaking with a satisfying sonic impact.

• SHOT 4 — [00:22 to 00:30] (RESOLUTION & SEAMLESS OUTRO LOOP):
  - Camera Shot: Smooth Crane Pull-Back / Cinematic Wide Angle Reveal
  - Visual Action: Majestic wide panoramic composition completing the sequence of {subject}. Warm ambient light settles softly across the horizon, creating a visually satisfying, perfectly seamless loopable ending frame for endless replayability.
  - Outro Retention: Compelling closing composition encouraging viewer replay and social sharing.

================================================================================
[3] CAMERA RIG, LIGHTING & RENDER SPECIFICATIONS
================================================================================
• Cinema Rig: Arri Alexa 65 / Red V-Raptor 8K VV
• Lens Package: Cooke Anamorphic /i Full Frame Plus (35mm / 85mm Prime combo)
• Lighting Scheme: Three-Point Volumetric Cinematic Lighting + Natural Sun Shaft Key + Ambient Bounce
• Shutter Speed: 1/48 sec (180-degree shutter rule for natural cinematic motion blur)
• Color Space: ACEScg / Kodak Vision3 500T 5219 Film Emulation (Teal & Warm Amber balance)
• Render Engines: Unreal Engine 5.4.4 + Octane Render 2026 Enterprise + Redshift 8K

================================================================================
[4] TOOL-SPECIFIC OPTIMIZED PRESETS
================================================================================
• KLING AI 1.5 / 2.0 (PROFESSIONAL MODE):
  Prompt: "Cinematic 8K masterpiece video of {subject}, 35mm anamorphic lens flare, volumetric sunbeams, photorealistic physics, natural motion blur, award-winning cinematography, 60fps."
  Settings: Mode: Professional | Motion Scale: 6.5 | Camera Control: Smooth Pan & Zoom | Aspect Ratio: 9:16

• SEEDANCE 2.0 / 2.5:
  Prompt: "Hyper-realistic viral video of {subject}, Unreal Engine 5 render, cinematic lighting, 35mm film grain, 8k resolution, smooth continuous motion, masterpiece."
  Settings: Quality: Ultra | FPS: 30 | Aspect Ratio: 9:16

• GOOGLE VEO 2:
  Prompt: "National Geographic 8K UHD cinematic video showcasing {subject}, dramatic lighting, hyper-detailed textures, smooth slow-motion camera pan."
  Settings: Style: Cinematic Film | Motion Intensity: High

• LUMA DREAM MACHINE:
  Prompt: "3D cinematic camera tracking shot around {subject}, photorealistic lighting, octane render, vivid natural colors, incredible depth of field."
  Settings: Camera Motion: Pan Right + Slow Zoom Out

• MIDJOURNEY v6 (STILL STORYBOARD KEYFRAME):
  Prompt: "{subject}, cinematic lighting, photorealistic 8k, shot on 35mm anamorphic lens, f/1.8, award winning photography, octane render --ar 9:16 --style raw --v 6.0"

================================================================================
[5] VIRAL SOCIAL MEDIA HOOKS & ENGAGEMENT PACKAGE
================================================================================
• Viral Title Hooks:
  1. "You won't believe what happens when {subject}..."
  2. "The most satisfying {subject} video on the internet today."
  3. "Wait until the end of this {subject}..."
• Engagement Caption:
  "Rate this cinematic {subject} from 1 to 10 in the comments! 🔥 Follow for daily viral master prompts. #AI #CGI #Cinematic"
• Recommended Hashtags:
  #AIArt #AIAnimation #KlingAI #Seedance #GoogleVeo #Midjourney #ViralShorts #ReelsViral #TikTokAI #CinematicAI

================================================================================
[6] COMPREHENSIVE MASTER NEGATIVE PROMPT
================================================================================
(Paste into Negative Prompt Box in your AI generator)
blurry, low quality, distorted anatomy, pixelated, watermark, text logo, low resolution, noise, overexposed, artifacting, static background, jerky motion, oversaturated, deformed features, bad framing, duplicate limbs, uncanny valley, CGI video game render look, low fidelity, plastic skin, jittery frame rate, flickers, morphing objects, extra fingers, cartoonish look, bad geometry."""

# Combine existing 389 prompts + new 39 prompts
all_combined = {}

# Process existing prompts
for p in existing_prompts:
    pid = str(p["id"])
    title = clean_text(p["title"])
    cat = clean_text(p.get("category", "General AI"))
    img = p.get("image") or f"images/prompt_{pid}.png"
    views = p.get("views", f"{(int(pid) * 37) % 4800 + 600}")
    likes = p.get("likes", f"{(int(pid) * 19) % 1800 + 240}")
    
    all_combined[pid] = {
        "id": pid,
        "title": title,
        "category": cat,
        "image": img,
        "original_img": p.get("original_img", f"https://soniprompts.com/uploads/prompt_{pid}.png"),
        "is_free": True,
        "views": str(views),
        "likes": str(likes),
        "prompt_text": format_complete_master_prompt(pid, title, cat)
    }

# Process new prompts
for pid, item in new_meta.items():
    pid = str(pid)
    title = clean_text(item["title"])
    cat = clean_text(item["category"])
    img = f"images/prompt_{pid}.png"
    views = f"{(int(pid) * 37) % 4800 + 600}"
    likes = f"{(int(pid) * 19) % 1800 + 240}"
    
    all_combined[pid] = {
        "id": pid,
        "title": title,
        "category": cat,
        "image": img,
        "original_img": item.get("img_src", ""),
        "is_free": True,
        "views": str(views),
        "likes": str(likes),
        "prompt_text": format_complete_master_prompt(pid, title, cat)
    }

# Convert to list and sort descending by numeric ID
final_list = list(all_combined.values())
final_list.sort(key=lambda x: int(x["id"]) if x["id"].isdigit() else 0, reverse=True)

print(f"Total merged and finalized prompts: {len(final_list)}")
print(f"Newest prompt (ID {final_list[0]['id']}): {final_list[0]['title']}")
print(f"Oldest prompt (ID {final_list[-1]['id']}): {final_list[-1]['title']}")

# Verify that all images exist locally
missing_images = [p['id'] for p in final_list if not os.path.exists(os.path.join(OUTPUT_DIR, p['image']))]
print(f"Missing local images count: {len(missing_images)}")

# Save to data/prompts.json
with open(os.path.join(DATA_DIR, "prompts.json"), "w", encoding="utf-8") as f:
    json.dump(final_list, f, indent=2, ensure_ascii=False)

# Save to prompts_data.js
with open(os.path.join(OUTPUT_DIR, "prompts_data.js"), "w", encoding="utf-8") as f:
    f.write("const AAKASH_PROMPTS_DATA = " + json.dumps(final_list, indent=2, ensure_ascii=False) + ";")

print("Both prompts_data.js and data/prompts.json updated successfully!")
