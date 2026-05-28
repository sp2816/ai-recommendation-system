import redis
import json
import random


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

print(
    "\nSelected User Key:"
)

print(
    sample_user_key
)


# ==========================
# FETCH USER PROFILE
# ==========================

user_profile = redis_client.get(
    sample_user_key
)

user_profile = json.loads(
    user_profile
)

print(
    "\nUser Profile:"
)

print(
    user_profile
)


# ==========================
# GET ITEM KEYS
# ==========================

item_keys = redis_client.keys(
    "item:*"
)

print(
    f"\nTotal Items Available: {len(item_keys)}"
)


# ==========================
# SIMULATE RECOMMENDATIONS
# ==========================

recommended_items = random.sample(
    item_keys,
    10
)

print(
    "\nRecommended Products:"
)

for item in recommended_items:

    print(
        item.replace(
            "item:",
            ""
        )
    )


# ==========================
# DAY 19 COMPLETE
# ==========================

print(
    "\nDay 19 Completed Successfully!"
)