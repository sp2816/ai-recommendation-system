import requests
import time

URL = "http://127.0.0.1:8000/recommend/1"

success = 0
failed = 0

start = time.time()

for i in range(50):

    try:

        response = requests.get(
            URL,
            timeout=5
        )

        if response.status_code == 200:
            success += 1
        else:
            failed += 1

    except:
        failed += 1

end = time.time()

print(f"Successful Requests: {success}")
print(f"Failed Requests: {failed}")

print(
    f"Average Time: "
    f"{(end-start)/50:.4f} sec/request"
)