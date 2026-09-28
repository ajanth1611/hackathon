import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = "devops-incidents-bank"

initial_incidents = [
    "Incident #101: Redis cache memory leak caused 504 Gateway Timeouts on auth service. Resolution: Cleared keyspace lock on port 6379 and restarted Redis cluster.",
    "Incident #102: Postgres DB high CPU usage due to missing index on users table query. Resolution: Created composite index idx_users_email_created_at.",
    "Incident #103: Microservice build failure in GitHub Actions on Docker layer caching. Resolution: Updated docker/build-push-action to v5 and cleared GitHub cache."
]

def seed():
    print("🚀 Seeding initial memories into Hindsight...")
    for log in initial_incidents:
        client.retain(bank_id=BANK_ID, content=log)
    print("✅ Memory seeding complete!")

if __name__ == "__main__":
    seed()