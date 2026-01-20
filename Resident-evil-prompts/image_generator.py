import os
import requests
import datetime
from pathlib import Path

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

MODEL_NAME = "google/nano-banana-pro"

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
        "model": MODEL_NAME,
        "input": {
            "prompt": prompt,
            "resolution": "2K",
            "aspect_ratio": "4:3",
            "output_format": "png",
            "safety_filter_level": "block_only_high"
        }
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
    get_url = prediction["urls"]["get"]

    # Polling simples
    while True:
        result = requests.get(get_url, headers=HEADERS).json()
        status = result.get("status")

        if status == "succeeded":
            return result["output"]  # ✅ string (URL direta)

        if status == "failed":
            raise RuntimeError("Geração da imagem falhou."

        )

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

    print(f"✅ Imagem gerada com Nano Banana Pro: {saved_path}")
