import os
import gdown

MODELS_DIR = "ml/models"

os.makedirs(MODELS_DIR, exist_ok=True)

files = {
    "candidate_tower.weights.h5": "1ECXwr1xfeLTluiko4ZllJevB-n7nTPvq",
    "feature_vocab.pkl": "1-m6KBGDfJTjvUeXo9fVeQPAGGEtZMixE",
    "item_embeddings.pkl": "13SNDHcywz3DMSgT_GkXTLFdA57KPvBEq",
    "item_store.pkl": "1vYTPHPk3LioZj2U1rviPCyhHz7Ihjdsz",
    "query_tower.weights.h5": "1LmC-XOGm_0Dr02-2VWKF9MSV6zPCigZZ",
    "redis_items.pkl": "1wwcj72SPrOo79JxVGyJnTYuV9VPMqDGC",
    "redis_users.pkl": "1XEqMPzmuiS1YWvv5db6DYBE0xqv9lmuP",
    "two_tower_weights.weights.h5": "1oFAc8bXd_KsoXRgIT9PLmmYcZ5GVgxUw",
    "user_store.pkl": "1rNPwZlC0luF9n-ll6ufkVdYX3dIgotfc",
}

for filename, file_id in files.items():

    output = os.path.join(MODELS_DIR, filename)

    if os.path.exists(output):
        print(f"{filename} already exists.")
        continue

    url = f"https://drive.google.com/uc?id={file_id}"

    print(f"Downloading {filename}...")

    gdown.download(url, output, quiet=False)

print("All models downloaded successfully.")