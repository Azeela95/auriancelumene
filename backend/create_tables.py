from app.core.database import engine, Base
# import models to ensure they are registered
import app.models.user
Base.metadata.create_all(bind=engine)
print("Tables created (if DB reachable)")
