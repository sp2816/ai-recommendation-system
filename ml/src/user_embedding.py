import os
from pathlib import Path
import pickle

# Do not force legacy tf.keras adapter; prefer the bundled Keras in TensorFlow.
# For some TF builds, forcing legacy Keras requires the external `tf_keras` package
# which may not be installed in the environment and is unnecessary for inference.
os.environ["TF_USE_LEGACY_KERAS"] = "0"

import tensorflow as tf


BASE_DIR = Path(__file__).resolve().parents[2]


# Load feature vocab
with open(
    BASE_DIR / "ml/models/feature_vocab.pkl",
    "rb"
) as file:

    feature_vocab = pickle.load(file)


user_vocab = feature_vocab["user_vocab"]
favorite_product_vocab = feature_vocab["favorite_product_vocab"]
season_vocab = feature_vocab["season_vocab"]


class QueryTower(
    tf.keras.Model
):

    def __init__(self):

        super().__init__()

        self.customer_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=user_vocab,
                mask_token=None
            ),
            tf.keras.layers.Embedding(
                len(user_vocab) + 1,
                32
            )
        ])

        self.favorite_product_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=favorite_product_vocab,
                mask_token=None
            ),
            tf.keras.layers.Embedding(
                len(favorite_product_vocab) + 1,
                16
            )
        ])

        self.season_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=season_vocab,
                mask_token=None
            ),
            tf.keras.layers.Embedding(
                len(season_vocab) + 1,
                8
            )
        ])

        self.dense_layers = tf.keras.Sequential([
            tf.keras.layers.Dense(
                128,
                activation="relu"
            ),
            tf.keras.layers.Dense(64)
        ])

    def call(self, features):

        customer_vector = self.customer_embedding(
            features["customer_id"]
        )

        favorite_product_vector = self.favorite_product_embedding(
            features["favorite_product_type"]
        )

        season_vector = self.season_embedding(
            features["season"]
        )

        numeric_features = tf.stack([
            tf.cast(features["age"], tf.float32),
            tf.cast(features["purchase_frequency"], tf.float32),
            tf.cast(features["avg_spend"], tf.float32),
            tf.cast(features["repeat_purchase_ratio"], tf.float32)
        ], axis=1)

        return self.dense_layers(
            tf.concat([
                customer_vector,
                favorite_product_vector,
                season_vector,
                numeric_features
            ], axis=1)
        )


query_model = QueryTower()

query_model(
    {
        "customer_id": tf.constant([user_vocab[0]]),
        "favorite_product_type": tf.constant([favorite_product_vocab[0]]),
        "season": tf.constant([season_vocab[0]]),
        "age": tf.constant([0.0], dtype=tf.float32),
        "purchase_frequency": tf.constant([0.0], dtype=tf.float32),
        "avg_spend": tf.constant([0.0], dtype=tf.float32),
        "repeat_purchase_ratio": tf.constant([0.0], dtype=tf.float32)
    }
)


# Load trained weights
try:
    query_model.load_weights(
        BASE_DIR / "ml/models/query_tower.weights.h5"
    )
except Exception as error:
    print(
        f"Warning: query tower weights could not be loaded: {error}"
    )


def get_user_embedding(
    user_profile
):

    embedding = query_model(
        {
            "customer_id": tf.convert_to_tensor([user_profile["customer_id"]]),
            "favorite_product_type": tf.convert_to_tensor([user_profile["favorite_product_type"]]),
            "season": tf.convert_to_tensor([user_profile["season"]]),
            "age": tf.convert_to_tensor([user_profile["age"]], dtype=tf.float32),
            "purchase_frequency": tf.convert_to_tensor([user_profile["purchase_frequency"]], dtype=tf.float32),
            "avg_spend": tf.convert_to_tensor([user_profile["avg_spend"]], dtype=tf.float32),
            "repeat_purchase_ratio": tf.convert_to_tensor([user_profile["repeat_purchase_ratio"]], dtype=tf.float32)
        }
    )

    return embedding.numpy()