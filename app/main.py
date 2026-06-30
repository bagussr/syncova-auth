from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import text

from app import settings
from app.integrations.redis import redis_client
from app.models import engine
from app.routes.auth import router as auth_router
from app.utils.exceptions import CustomExceptiom


async def lifespan(app: FastAPI):
    load_dotenv()
    if settings.ENV == "development":
        print(
            "⚠️ Running in development mode. Make sure to set ENV=production in production environments."
        )
    else:
        try:
            redis_client.ping()
            print("✅ Redis connected")
        except Exception as e:
            print("Redis startup failed: %s" % repr(e))
            raise ConnectionError("Failed to connect to Redis")

        # Database
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connected")
        except Exception as e:
            print("Database startup failed: %s" % repr(e))
            raise ConnectionError("Failed to connect to Database")

    yield


app = FastAPI(
    lifespan=lifespan,
)

exception_handler = CustomExceptiom(app)

app.include_router(auth_router)

exception_handler.init()
