import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="recommendation_db",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

tables = [
    "users",
    "products",
    "wishlist",
    "search_history",
    "view_history",
    "user_interactions"
]

for table in tables:
    try:
        cursor.execute(
            f"SELECT COUNT(*) FROM {table}"
        )

        count = cursor.fetchone()[0]

        print(
            f"{table}: {count} rows"
        )

    except Exception as e:
        print(
            f"{table}: ERROR -> {e}"
        )

cursor.close()
conn.close()