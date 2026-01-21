import os
from pathlib import Path
import tweepy

# ==================================================
# CREDENCIAIS (ENVIRONMENT SECRETS)
# ==================================================

CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("X_CONSUMER_KEY_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise RuntimeError("Credenciais do X incompletas.")

# ==================================================
# AUTENTICAÇÃO OAUTH 1.0a
# ==================================================

auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)

# ==================================================
# FUNÇÕES
# ==================================================

def get_latest_image() -> str:
    image_dir = Path("Resident-evil-prompts/images")
    images = sorted(
        image_dir.glob("image_*.png"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if not images:
        raise RuntimeError("Nenhuma imagem encontrada para postar.")

    return str(images[0])


def post_image_to_x(image_path: str):
    media = api.media_upload(image_path)
    api.update_status(status="", media_ids=[media.media_id])

# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    image = get_latest_image()
    post_image_to_x(image)
    print("✅ Imagem postada com sucesso no X.")
