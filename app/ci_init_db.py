import time
from sqlalchemy.exc import OperationalError
from app.database import engine, Base

print("🔄 Waiting for Postgres to be ready...")

# Retry until Postgres is ready
for i in range(20):
    try:
        with engine.connect() as conn:
            print("✅ Postgres is ready!")
            break
    except OperationalError:
        print(f"⏳ Postgres not ready yet... retrying ({i+1}/20)")
        time.sleep(1)

# Create all tables
print("🔨 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully!")
