import os
import datetime
from pathlib import Path
from PIL import Image
import google.generativeai as genai

# ==================================================
# CONFIGURAÇÃO DA API (NÃO HARD-CODA CHAVE)
# ==================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY não encontrada nos Environment Secrets.")

genai.configure(api_key=API_KEY)

# Modelo de imagem do Google
image_model = genai.ImageGenerationModel("imagen-3.0-generate-001")

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
    print("🎨 Gerando imagem com Imagen 3...")

    response = image_model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio="4:3",   # ótimo para cenas e storytelling
        safety_filter="block_only_high"
    )

    if not response.images:
        raise RuntimeError("Nenhuma imagem retornada pela API (bloqueada pelo safety filter).")

    image = response.images[0]

    os.makedirs("Resident-evil-prompts/images", exist_ok=True)

    filename = (
        "Resident-evil-prompts/images/"
        f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )

    image.save(filename)

    return filename


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    prompt = get_latest_prompt()
    image_path = generate_image(prompt)

    print(f"✅ Imagem gerada com sucesso: {image_path}")
