import os
import requests
import datetime
from pathlib import Path
import time

# ==================================================
# CONFIGURAÇÃO
# ==================================================

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    raise RuntimeError("REPLICATE_API_TOKEN não encontrado.")

HEADERS = {
    "Authorization": f"Token {REPLICATE_API_TOKEN}",
    "Content-Type": "application/json",
}

REPLICATE_ENDPOINT = "https://api.replicate.com/v1/predictions"

# Modelo Stable Diffusion XL
MODEL_VERSION = "stability-ai/stable-diffusion-xl"

# ==================================================
# FUNÇÕES
# ==================================================

def get_latest_prompt() -> str:
    prompt_dir = Path("Resident-evil-prompts/prompts")
    prompt_files = sorted(prompt_dir.glob("prompt_*.txt"), reverse=True)

    if not prompt_files:
        raise RuntimeError("Nenhum prompt encontrado.")

    return prompt_files[0].read_text(encoding="utf-8")


def generate_image(prompt: str) -> str:
    payload = {
        "version": MODEL_VERSION,
        "input": {
            "prompt": prompt,
            "width": 1024,
            "height": 1024,
            "guidance_scale": 7.5,
            "num_inference_steps": 35,
            "negative_prompt": (
                "cartoon, anime, illustration, low quality, blurry, "
                "bad anatomy, visible face, watermark, text"
            ),
        },
    }

    response = requests.post(
        REPLICATE_ENDPOINT,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    if response.status_code != 201:
        raise RuntimeError(f"Erro Replicate: {response.text}")

    prediction = response.json()
    status_url = prediction["urls"]["get"]

    while True:
        result = requests.get(status_url, headers=HEADERS).json()
        status = result.get("status")

        if status == "succeeded":
            return result["output"][0]

        if status == "failed":
            raise RuntimeError("Geração da imagem falhou.")

        time.sleep(3)


def download_image(image_url: str) -> str:
    image_data = requests.get(image_url).content
    os.makedirs("Resident-evil-prompts/images", exist_ok=True)

    filename = (
        "Resident-evil-prompts/images/"
        f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    with open(filename, "wb") as f:
        f.write(image_data)

    return filename


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    prompt = get_latest_prompt()
    image_url = generate_image(prompt)
    saved_path = download_image(image_url)

    print(f"✅ Imagem salva em {saved_path}")
