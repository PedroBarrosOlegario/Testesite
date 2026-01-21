import os
import datetime
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

# ==================================================
# CONFIGURAÇÃO
# ==================================================

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY não encontrada.")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash-image"  # Nano Banana

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
    print("🍌 Gerando imagem com Nano Banana...")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt],
    )

    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()

            os.makedirs("Resident-evil-prompts/images", exist_ok=True)
            filename = (
                "Resident-evil-prompts/images/"
                f"image_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )

            image.save(filename)
            return filename

    raise RuntimeError("Nenhuma imagem retornada pelo modelo.")


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    prompt = get_latest_prompt()
    image_path = generate_image(prompt)
    print(f"✅ Imagem gerada com Nano Banana: {image_path}")
