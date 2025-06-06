import os
import psycopg2

# Read DATABASE_URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')
print("DATABASE_URL =", DATABASE_URL)

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    now = cur.fetchone()[0]
    print("✅ Connection successful. Server time is:", now)
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed with error:")
    print(e)
