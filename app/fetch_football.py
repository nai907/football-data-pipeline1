import os
import json
import requests
import boto3

# API
url = "https://api.football-data.org/v4/teams/66/matches"
headers = {"X-Auth-Token": os.getenv("FOOTBALL_API_TOKEN")}

# Fetch from API
r = requests.get(url, headers=headers, timeout=10)
r.raise_for_status()
data = r.json()

# Save to same directory
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "matches.json")

with open(file_path, "w") as f:
    json.dump(data, f)

# Upload to your S3 bucket
s3 = boto3.client("s3")
s3.upload_file(
    file_path,
    "nanthayod-football",            # your bucket name
    "football/raw/matches.json"      # S3 key (path inside bucket)
)

print("Saved locally and uploaded to nanthayod-football")

import psycopg2

# PostgreSQL connection
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    dbname=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=5432
)

cur = conn.cursor()

# Insert matches
for m in data["matches"]:
    cur.execute(
        """
        INSERT INTO matches (match_id, utc_date, home_team, away_team, status)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (match_id) DO NOTHING
        """,
        (
            m["id"],
            m["utcDate"],
            m["homeTeam"]["name"],
            m["awayTeam"]["name"],
            m["status"]
        )
    )

conn.commit()
cur.close()
conn.close()

print("Data inserted into PostgreSQL")