import redis
import json
import random
import numpy as np
import pickle

from sklearn.metrics.pairwise import cosine_similarity


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
# LOAD ITEM EMBEDDINGS
# ==========================

with open(
    "ml/models/item_embeddings.pkl",
    "rb"
) as file:

    item_embeddings_df = pickle.load(
        file
    )

print(
    "Item embeddings loaded!"
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
# CREATE USER VECTOR
# ==========================

favorite_product = user_profile[
    "favorite_product_type"
]

candidate_items = item_embeddings_df.sample(
    1000,
    random_state=42
)

user_vector = np.mean(

    np.vstack(
        candidate_items[
            "embedding"
        ].values
    ),

    axis=0
)


# ==========================
# COMPUTE SIMILARITIES
# ==========================

item_matrix = np.vstack(

    candidate_items[
        "embedding"
    ].values
)

similarity_scores = cosine_similarity(

    [user_vector],

    item_matrix

)[0]


candidate_items[
    "score"
] = similarity_scores


# ==========================
# TOP RECOMMENDATIONS
# ==========================

top_items = candidate_items.sort_values(

    by="score",

    ascending=False

).head(10)


print(
    "\nRecommended Products:"
)

for article_id in top_items[
    "article_id"
]:

    print(
        article_id
    )


# ==========================
# DAY 21 COMPLETE
# ==========================

print(
    "\nDay 21 Completed Successfully!"
)