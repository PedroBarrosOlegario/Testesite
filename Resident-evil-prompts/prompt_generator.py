
import os
import random
import requests
import json
import datetime

# ================= CONFIGURAÇÃO =================

API_KEY = os.getenv("GEMINI_API_KEY")
ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY não encontrada. Verifique os Environment Secrets do GitHub.")

# ================= BASE CRIATIVA =================

BASE_ELEMENTS = {
    "locations": [
        "a decaying gothic mansion corridor overtaken by mold",
        "a fog-covered rural village with abandoned wooden houses",
        "an underground laboratory filled with broken glass and biohazard signs",
        "a dark police station hallway with flickering emergency lights",
        "a ruined castle interior illuminated by moonlight",
        "an abandoned hospital ward with torn curtains and rusted beds",
        "a flooded city street at night with overturned vehicles",
        "a narrow underground passage surrounded by concrete and pipes"
    ],
    "atmospheres": [
        "a suffocating sense of dread and isolation",
        "absolute silence with an unseen threat nearby",
        "overwhelming tension as if danger lurks in the shadows",
        "cold, decaying survival horror ambience",
        "an oppressive, claustrophobic horror atmosphere"
    ],
    "lighting": [
        "a single flashlight beam cutting through darkness",
        "flickering fluorescent lights casting long shadows",
        "cold moonlight entering through broken windows",
        "red emergency lights reflecting on wet surfaces",
        "soft volumetric fog illuminated by distant lamps"
    ],
    "camera": [
        "wide cinematic framing",
        "over-the-shoulder survival horror perspective",
        "low-angle dramatic shot",
        "static composition emphasizing environment scale",
        "slow cinematic zoom"
    ]
}

# ================= FUNÇÕES =================

def build_base_prompt() -> str:
    return f"""
Create an ultra-realistic cinematic survival horror image inspired by the Resident Evil video game series.

Scene:
{random.choice(BASE_ELEMENTS["locations"])}.
{random.choice(BASE_ELEMENTS["atmospheres"])}.

Lighting:
{random.choice(BASE_ELEMENTS["lighting"])}.

Character presence:
A lone human silhouette may appear, but the face must be completely hidden or obscured.
No identifiable facial features.

Camera:
{random.choice(BASE_ELEMENTS["camera"])}.

Style rules:
Photorealistic, dark palette, realistic textures, cinematic lighting.
No text, no logos, no watermark.
""".strip()


def refine_with_gemini(prompt: str) -> str:
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are a professional cinematic prompt engineer specializing in "
                            "survival horror environments inspired by classic Resident Evil games.\n\n"
                            "Enhance and polish the following image prompt to maximize realism, mood, "
                            "uniqueness and cinematic quality. Ensure each result feels visually distinct.\n\n"
                            f"{prompt}"
                        )
                    }
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY
    }

    response = requests.post(
        ENDPOINT,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Gemini API error {response.status_code}: {response.text}"
        )

    result = response.json()

    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Resposta inesperada da Gemini API: {result}")

# ================= EXECUÇÃO =================

if __name__ == "__main__":
    base_prompt = build_base_prompt()
    final_prompt = refine_with_gemini(base_prompt)

    os.makedirs("Resident-evil-prompts/prompts", exist_ok=True)

    filename = (
        "Resident-evil-prompts/prompts/"
        f"prompt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_prompt)

    print("\n=== FINAL PROMPT GERADO ===\n")
    print(final_prompt)
