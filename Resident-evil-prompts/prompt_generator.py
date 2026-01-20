
import random
import requests
import os
import datetime
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---------- BASE CRIATIVA ----------

LOCATIONS = [
    "a mold-infested gothic mansion corridor",
    "a fog-choked rural village inspired by Eastern Europe",
    "a flooded underground laboratory with biohazard symbols",
    "a destroyed police station hallway lit by emergency lights",
    "an abandoned hospital ward filled with shadows",
    "a ruined castle throne room at night",
    "a narrow sewer passage filled with steam",
    "a collapsed underground research facility"
]

ATMOSPHERE = [
    "oppressive survival horror tension",
    "absolute silence mixed with dread",
    "a constant feeling of being watched",
    "cold, abandoned, and decaying ambience",
    "ominous invisible threat nearby"
]

LIGHTING = [
    "single flashlight beam piercing the darkness",
    "flickering fluorescent lights",
    "cold moonlight entering through broken windows",
    "red emergency lighting reflecting on wet floors",
    "soft volumetric fog illuminated by distant lamps"
]

CHARACTERS = [
    "a lone survivor partially hidden in shadow, face completely obscured",
    "a mysterious silhouette wearing tactical gear, identity concealed",
    "a human figure seen only from behind, holding a weapon",
    "a hooded figure barely visible through heavy fog",
    "a survivor standing in darkness, no facial features visible"
]

CAMERA = [
    "wide cinematic shot",
    "over-the-shoulder survival horror perspective",
    "low-angle dramatic framing",
    "static frame emphasizing environment scale",
    "slow zoom cinematic composition"
]

def create_base_prompt():
    return f"""
Ultra realistic cinematic survival horror environment inspired by Resident Evil.

Scene:
{random.choice(LOCATIONS)}.
{random.choice(ATMOSPHERE)}.

Lighting:
{random.choice(LIGHTING)}.

Character:
{random.choice(CHARACTERS)}.
No face visible. No identifiable features.

Camera:
{random.choice(CAMERA)}.

Style:
Photorealistic, dark color palette, high detail, realistic textures.

Rules:
No text, no logos, no watermark.
"""

def refine_prompt_with_gpt(base_prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a professional cinematic prompt engineer specialized in survival horror environments inspired by classic Resident Evil."
            },
            {
                "role": "user",
                "content": f"Polish and enhance this image prompt for maximum realism, atmosphere and cinematic quality:\n\n{base_prompt}"
            }
        ],
        "temperature": 1.0,
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=body
    )

    return response.json()["choices"][0]["message"]["content"]

def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": "1024x1024"
    }

    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=body
    )

    image_base64 = response.json()["data"][0]["b64_json"]
    image_bytes = base64.b64decode(image_base64)

    folder = "generated_images"
    os.makedirs(folder, exist_ok=True)

    filename = f"re_scene_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(folder, filename)

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path

# ---------- EXECUTION ----------

if __name__ == "__main__":
    import base64

    base_prompt = create_base_prompt()
    final_prompt = refine_prompt_with_gpt(base_prompt)

    print("FINAL PROMPT:\n", final_prompt)

    image_path = generate_image(final_prompt)
    print("Image saved to:", image_path)
