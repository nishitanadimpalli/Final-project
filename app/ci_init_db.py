from app.database import engine, Base

print("🔧 Creating all database tables for CI...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")
