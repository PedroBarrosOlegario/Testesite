import os
import json
import requests
from pathlib import Path
from requests_oauthlib import OAuth1

# ==================================================
# AUTH - OAuth 1.0a USER CONTEXT
# ==================================================

CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("X_CONSUMER_KEY_SECRET")
ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    raise RuntimeError("❌ Credenciais do X incompletas nos Environment Secrets.")

auth = OAuth1(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

# ==================================================
# ENDPOINTS OFICIAIS
# ==================================================

MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
CREATE_TWEET_URL = "https://api.x.com/2/tweets"

# ==================================================
# FUNÇÕES
# ==================================================

def get_latest_image() -> str:
    """
    Pega a imagem mais recente gerada pelo pipeline.
    """
    image_dir = Path("Resident-evil-prompts/images")

    images = sorted(
        image_dir.glob("image_*.png"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not images:
        raise RuntimeError("❌ Nenhuma imagem encontrada para postar.")

    return str(images[0])


def upload_media(image_path: str) -> str:
    """
    Faz upload da imagem para o Twitter/X (v1.1).
    Retorna o media_id_string.
    """
    with open(image_path, "rb") as image_file:
        files = {"media": image_file}
        response = requests.post(
            MEDIA_UPLOAD_URL,
            auth=auth,
            files=files
        )

    if response.status_code != 200:
        raise RuntimeError(
            f"❌ Erro no upload da mídia ({response.status_code}): {response.text}"
        )

    return response.json()["media_id_string"]


def create_post(media_id: str):
    """
    Cria o post no X v2 usando o media_id.
    """
    payload = {
        "media": {
            "media_ids": [media_id]
        }
        # Texto intencionalmente omitido (post só com imagem)
        # "text": ""
    }

    response = requests.post(
        CREATE_TWEET_URL,
        auth=auth,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload)
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"❌ Erro ao criar post ({response.status_code}): {response.text}"
        )

    return response.json()


# ==================================================
# EXECUÇÃO
# ==================================================

if __name__ == "__main__":
    print("📸 Localizando imagem...")
    image_path = get_latest_image()

    print("⬆️ Enviando imagem...")
    media_id = upload_media(image_path)

    print("📝 Criando post...")
    result = create_post(media_id)

    print("✅ Post publicado com sucesso!")
    print(result)
