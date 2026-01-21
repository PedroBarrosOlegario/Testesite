import os
import random
import datetime
from pathlib import Path
import requests

# ==================================================
# CONFIGURAÇÃO (SECRETS EXATOS)
# ==================================================

CLOUD_FLARE_API = os.getenv("CLOUD_FLARE_API")
CLOUDFLARE_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT")

if not CLOUD_FLARE_API or not CLOUDFLARE_ACCOUNT:
    raise RuntimeError(
        "CLOUD_FLARE_API ou CLOUDFLARE_ACCOUNT não encontrados nos Environment Secrets."
    )

BASE_URL = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT}/ai/run"

HEADERS = {
    "Authorization": f"Bearer {CLOUD_FLARE_API}",
    "Content-Type": "application/json"
}

# ==================================================
# MODELOS DISPONÍVEIS (ESCOLHA ALEATÓRIA)
# ==================================================

MODELS = [
    {
        "name": "SDXL Lightning (Bytedance)",
        "path": "@cf/bytedance/stable-diffusion-xl-lightning"
    },
    {
        "name": "SDXL Base 1.0 (Stability AI)",
        "path": "@cf/stabilityai/stable-diffusion-xl-base-1.0"
    }
]

# ==================================================
# FUNÇÕES
# ==================================================

def get_latest_prompt() -> str:
    prompt_dir = Path("Resident-evil-prompts/prompts")
    files = sorted(prompt_dir.glob("prompt_*.txt"), reverse=True)

    if not files:
        raise RuntimeError("Nenhum prompt encontrado.")

    return files[0].read_text(encoding="utf-8")


def generate_image(prompt: str) -> str:
    model = random.choice(MODELS)
    model_url = f"{BASE_URL}/{model['path']}"

    print(f"🎲 Modelo escolhido: {model['name']}")

    payload = {
        "prompt": prompt,
        "negative_prompt": (
            "cartoon, anime, illustration, low quality, blurry, "
            "bad anatomy, visible face, watermark, text"
        ),
        "width": 1024,
        "height": 1024,
        "guidance": 7.5,
        "num_steps": 20
    }

    response = requests.post(
        model_url,
        headers=HEADERS,
        json=payload,
        timeout=90
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Erro Cloudflare [{model['name']}] "
            f"{response.status_code}: {response.text}"
        )

    os.makedirs("Resident-evil-prompts/images", exist_ok=True)

    filename = (
        "Resident-evil-prompts/images/"
        f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    with open(filename, "wb") as f:
        f.write(response.content)

    return filename


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    prompt = get_latest_prompt()
    image_path = generate_image(prompt)

    print(f"✅ Imagem gerada com sucesso: {image_path}")
