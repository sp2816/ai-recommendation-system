import redis
import json
import random
import numpy as np


# ==========================
# CONNECT TO REDIS
# ==========================

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

print(
    "Redis Connected:",
    redis_client.ping()
)


# ==========================
# GET RANDOM USER
# ==========================

user_keys = redis_client.keys(
    "user:*"
)

sample_user_key = random.choice(
    user_keys
)

user_profile = redis_client.get(
    sample_user_key
)

user_profile = json.loads(
    user_profile
)

print(
    "\nSelected User:"
)

print(
    user_profile
)


# ==========================
# FETCH RANDOM ITEMS
# ==========================

item_keys = redis_client.keys(
    "item:*"
)

sample_items = random.sample(
    item_keys,
    10
)

print(
    "\nFetching Item Embeddings..."
)


item_embeddings = []

for item_key in sample_items:

    embedding = redis_client.get(
        item_key
    )

    embedding = json.loads(
        embedding
    )

    embedding = np.array(
        embedding
    )

    item_embeddings.append({

        "article_id":
            item_key.replace(
                "item:",
                ""
            ),

        "embedding":
            embedding
    })


print(
    "\nFetched Items:"
)

for item in item_embeddings:

    print(
        item[
            "article_id"
        ]
    )


# ==========================
# CHECK EMBEDDING SHAPE
# ==========================

print(
    "\nEmbedding Shape:"
)

print(

    item_embeddings[0][
        "embedding"
    ].shape
)


# ==========================
# DAY 20 COMPLETE
# ==========================

print(
    "\nDay 20 Completed Successfully!"
)