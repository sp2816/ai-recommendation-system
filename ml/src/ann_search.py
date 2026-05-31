import pickle
import numpy as np
import tensorflow as tf
from sklearn.metrics.pairwise import cosine_similarity


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


# ==========================
# ANN SEARCH FUNCTION
# ==========================

def get_recommendations(


    user_profile,

    top_k=10

):

    candidate_items = item_embeddings_df.sample(
        min(1000, len(item_embeddings_df)),
        random_state=42
    )


    from ml.src.user_embedding import (
        query_model
    )


    user_input = {

        "customer_id":
            tf.constant([
                user_profile[
                    "customer_id"
                ]
            ]),

        "favorite_product_type":
            tf.constant([
                user_profile[
                    "favorite_product_type"
                ]
            ]),

        "season":
            tf.constant([
                user_profile[
                    "season"
                ]
            ]),

        "age":
            tf.constant([
                user_profile[
                    "age"
                ]
            ], dtype=tf.float32),

        "purchase_frequency":
            tf.constant([
                user_profile[
                    "purchase_frequency"
                ]
            ], dtype=tf.float32),

        "avg_spend":
            tf.constant([
                user_profile[
                    "avg_spend"
                ]
            ], dtype=tf.float32),

        "repeat_purchase_ratio":
            tf.constant([
                user_profile[
                    "repeat_purchase_ratio"
                ]
            ], dtype=tf.float32)
    }


    user_vector = query_model(
        user_input
    ).numpy()[0]


    item_matrix = np.vstack(

        candidate_items[
            "embedding"
        ].values
    )


    similarity_scores = cosine_similarity(

        [user_vector],

        item_matrix

    )[0]


    # base similarity score
    candidate_items["score"] = similarity_scores

    # ---- Lightweight reranking boost ----
    # boost items that match the user's favorite product type and season
    fav_type = user_profile.get("favorite_product_type")
    user_season = user_profile.get("season")

    fav_boost = 0.8
    season_boost = 0.6
    popularity_weight = 0.05

    # product type match
    if "product_type_name" in candidate_items.columns:
        type_match = (candidate_items["product_type_name"] == fav_type).astype(float)
    else:
        type_match = np.zeros(len(candidate_items), dtype=float)

    # season match
    if "season" in candidate_items.columns:
        season_match = (candidate_items["season"] == user_season).astype(float)
    else:
        season_match = np.zeros(len(candidate_items), dtype=float)

    # optional popularity signal (normalize if present)
    if "popularity" in candidate_items.columns:
        pop_raw = candidate_items["popularity"].astype(float)
        if pop_raw.max() > pop_raw.min():
            pop_norm = (pop_raw - pop_raw.min()) / (pop_raw.max() - pop_raw.min())
        else:
            pop_norm = np.zeros(len(candidate_items), dtype=float)
    else:
        pop_norm = np.zeros(len(candidate_items), dtype=float)

    # final score = similarity + weighted boosts
    final_score = (
        similarity_scores
        + fav_boost * type_match
        + season_boost * season_match
        + popularity_weight * pop_norm
    )

    candidate_items["score"] = final_score

    # sort and return top_k article ids
    top_items = candidate_items.sort_values(by="score", ascending=False).head(top_k)

    return list(top_items["article_id"])