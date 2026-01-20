
import os
import random
import datetime

# ==================================================
# IDENTIDADE FIXA (estilo visual constante)
# ==================================================

FIXED_STYLE = """
Ultra-realistic cinematic survival horror.
Photorealistic textures, realistic lighting, dark color palette.
Mature tone, grounded realism, mysterious and tense atmosphere.
Inspired by classic and modern Resident Evil environments.
"""

# ==================================================
# ELEMENTOS VARIÁVEIS (variam a cada geração)
# ==================================================

LOCATIONS = [
    "a decaying gothic mansion hallway with cracked marble floors and rotting wooden walls",
    "a fog-covered rural village street with abandoned houses and ritualistic symbols",
    "an underground laboratory corridor with shattered glass and biohazard warning signs",
    "a ruined police station interior with overturned desks and flickering lights",
    "an abandoned hospital ward with rusted beds, torn curtains, and blood-stained tiles",
    "a collapsing castle interior illuminated by cold moonlight through broken windows",
    "a narrow sewer passage filled with steam, pipes, and stagnant water",
    "a destroyed urban street after a biological outbreak, debris scattered everywhere"
]

ATMOSPHERES = [
    "an oppressive sense of dread and constant danger",
    "absolute silence, broken only by distant echoes",
    "a heavy feeling of isolation as if something is stalking nearby",
    "thick tension that suggests an invisible threat",
    "a cold, lifeless ambiance with lingering biological contamination"
]

LIGHTING = [
    "a single handheld flashlight casting sharp shadows",
    "flickering fluorescent lights barely illuminating the area",
    "cold moonlight creating long, dramatic shadows",
    "emergency red lighting reflecting on wet surfaces",
    "dim ambient light mixed with volumetric fog"
]

CAMERA_FRAMING = [
    "wide cinematic shot emphasizing environment scale",
    "over-the-shoulder survival horror perspective",
    "low-angle shot increasing tension and unease",
    "static composition focused on environmental storytelling",
    "tight cinematic framing surrounded by darkness"
]

# ==================================================
# ARMAS – HANDGUNS / PISTOLS (ESTILO RESIDENT EVIL)
# ==================================================

HANDGUNS = [
    "a worn semi-automatic handgun held firmly, showing scratches and heavy use",
    "a tactical pistol with a mounted flashlight, reflecting dim light",
    "a classic survival handgun with a matte metal finish and textured grip",
    "a compact combat pistol partially illuminated in the darkness",
    "a service pistol resting cautiously at the survivor’s side"
]

# ==================================================
# PERSONAGEM (SEM ROSTO)
# ==================================================

CHARACTERS = [
    "a lone survivor standing in the shadows, face completely hidden",
    "a mysterious figure seen only from behind, identity concealed",
    "a human silhouette partially obscured by darkness and fog",
    "a survivor wearing practical clothing, facial features invisible",
    "a tense figure gripping a weapon, face lost in shadow"
]

# ==================================================
# FUNÇÃO PRINCIPAL
# ==================================================

def generate_prompt() -> str:
    prompt = f"""
{FIXED_STYLE}

Scene description:
{random.choice(LOCATIONS)}.
The environment feels abandoned and dangerous.

Atmosphere:
{random.choice(ATMOSPHERES)}.

Lighting:
{random.choice(LIGHTING)}.

Character presence:
{random.choice(CHARACTERS)}.
The character is holding {random.choice(HANDGUNS)}.
No face visible under any circumstances.

Camera:
{random.choice(CAMERA_FRAMING)}.

Visual rules:
No text, no logos, no symbols, no watermark.
No visible faces.
No exaggerated fantasy elements.

Focus:
Environmental storytelling, tension, realism, mystery.
""".strip()

    return prompt

# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    final_prompt = generate_prompt()

    os.makedirs("Resident-evil-prompts/prompts", exist_ok=True)

    filename = (
        "Resident-evil-prompts/prompts/"
        f"prompt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_prompt)

    print("\n=== PROMPT GERADO ===\n")
    print(final_prompt)
