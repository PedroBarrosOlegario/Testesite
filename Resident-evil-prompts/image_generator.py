import os
import datetime
from pathlib import Path
import replicate

# ==================================================
# CONFIGURAÇÃO
# ==================================================

if not os.getenv("REPLICATE_API_TOKEN"):
    raise RuntimeError("REPLICATE_API_TOKEN não encontrado.")

# A lib replicate usa automaticamente o env REPLICATE_API_TOKEN

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
    output = replicate.run(
        "google/nano-banana-pro",
        input={
            "prompt": prompt,
            "resolution": "2K",
            "aspect_ratio": "4:3",
            "output_format": "png",
            "safety_filter_level": "block_only_high"
        }
    )

    # Nano Banana retorna um File-like object
    os.makedirs("Resident-evil-prompts/images", exist_ok=True)

    filename = (
        "Resident-evil-prompts/images/"
        f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    with open(filename, "wb") as f:
        f.write(output.read())

    return filename

# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    prompt = get_latest_prompt()
    image_path = generate_image(prompt)

    print(f"✅ Imagem gerada com Nano Banana Pro: {image_path}")
