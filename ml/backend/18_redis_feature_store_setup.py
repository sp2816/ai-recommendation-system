import redis
import pickle
import json


# ==========================
# CONNECT TO REDIS
# ==========================

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

print("Redis Connected:", redis_client.ping())


# ==========================
# LOAD REDIS FILES
# ==========================

with open(
    "ml/models/redis_users.pkl",
    "rb"
) as file:

    redis_users = pickle.load(file)


with open(
    "ml/models/redis_items.pkl",
    "rb"
) as file:

    redis_items = pickle.load(file)


print("Files loaded successfully!")


# ==========================
# STORE USERS
# ==========================

user_count = 0

for customer_id, profile in redis_users.items():

    redis_client.set(

        f"user:{customer_id}",

        json.dumps(profile)
    )

    user_count += 1


print(
    f"{user_count} users stored!"
)


# ==========================
# STORE ITEMS
# ==========================

item_count = 0

for article_id, embedding in redis_items.items():

    redis_client.set(

        f"item:{article_id}",

        json.dumps(embedding)
    )

    item_count += 1


print(
    f"{item_count} items stored!"
)


# ==========================
# TEST USER RETRIEVAL
# ==========================

sample_user = list(
    redis_users.keys()
)[0]

print("\nSample User:")

print(

    redis_client.get(
        f"user:{sample_user}"
    )
)


# ==========================
# TEST ITEM RETRIEVAL
# ==========================

sample_item = list(
    redis_items.keys()
)[0]

print("\nSample Item Embedding:")

print(

    redis_client.get(
        f"item:{sample_item}"
    )[:150]
)


# ==========================
# TOTAL REDIS KEYS
# ==========================

print(

    "\nTotal Keys Stored:",

    len(
        redis_client.keys()
    )
)


print(
    "\nDay 18 Completed Successfully!"
)