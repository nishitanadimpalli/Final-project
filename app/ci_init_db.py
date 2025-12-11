from app.database import Base, engine
from app import models

print("Creating all tables for CI...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")
