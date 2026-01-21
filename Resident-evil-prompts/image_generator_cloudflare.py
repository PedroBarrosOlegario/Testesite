import os
import datetime
from pathlib import Path
import requests

# ==================================================
# CONFIGURAÇÃO (envs EXATOS)
# ==================================================

CLOUD_FLARE_API = os.getenv("CLOUD_FLARE_API")
CLOUDFLARE_ACCOUNT = os.getenv("CLOUDFLARE_ACCOUNT")

if not CLOUD_FLARE_API or not CLOUDFLARE_ACCOUNT:
    raise RuntimeError(
        "CLOUD_FLARE_API ou CLOUDFLARE_ACCOUNT não encontrados nos Environment Secrets."
    )

API_URL = (
    f"https://api.cloudflare.com/client/v4/accounts/"
    f"{CLOUDFLARE_ACCOUNT}/ai/run/"
    "@cf/bytedance/stable-diffusion-xl-lightning"
)

HEADERS = {
    "Authorization": f"Bearer {CLOUD_FLARE_API}",
    "Content-Type": "application/json"
}

# ==================================================
# FUNÇÕES
# ==================================================

def get_latest_prompt() -> str:
    prompt_dir = Path("Resident-evil-prompts/prompts")
    prompt_files = sorted(prompt_dir.glob("prompt_*.txt"), reverse=True)

    if not prompt_files:
        raise RuntimeError("Nenhum prompt encontrado para gerar imagem.")

    return prompt_files[0].read_text(encoding="utf-8")


def generate_image(prompt: str) -> str:
    print("⚡ Gerando imagem com Cloudflare SDXL Lightning...")

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
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Erro Cloudflare {response.status_code}: {response.text}"
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
    print(f"✅ Imagem gerada com Cloudflare SDXL: {image_path}")
