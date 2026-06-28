import requests
import time


# ==========================
# TEST USER IDS
# ==========================

test_users = [

    "40beb0b49193159063a6f6135e02b4f42d96de02234afea9a002b8e193195431",

    "4975d739e72a2af4b29a01193d8dd426cc2f4f5269a14df2801eb7b34b482631",

    "077f74fa4a9efe8ec2cd200f99f9ff829eeb89087e59cc5dbdd00b20795590ab"

]


# ==========================
# API URL
# ==========================

BASE_URL = (
    "http://import.meta.env.VITE_API_URL"
)


# ==========================
# STRESS TEST
# ==========================

success_count = 0
failure_count = 0

start_time = time.time()

for i in range(50):

    user_id = test_users[
        i % len(test_users)
    ]

    response = requests.get(

        f"{BASE_URL}/recommend/{user_id}"

    )

    if response.status_code == 200:

        success_count += 1

    else:

        failure_count += 1

        print(

            f"Failed request {i}"

        )


end_time = time.time()


# ==========================
# RESULTS
# ==========================

print("\nStress Test Results")

print(
    "Successful Requests:",
    success_count
)

print(
    "Failed Requests:",
    failure_count
)

print(

    "Total Time:",

    round(
        end_time - start_time,
        2
    ),

    "seconds"
)

print(

    "Average Response Time:",

    round(

        (
            end_time
            - start_time
        )
        / 50,

        3
    ),

    "seconds/request"
)
