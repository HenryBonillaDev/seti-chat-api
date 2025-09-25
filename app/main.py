from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlmodel import SQLModel, create_engine
from app.api.v1.routers.messages import router
from app.core.config import settings
from app.core.exceptions import CustomAPIException, custom_exception_handler, validation_exception_handler

engine = create_engine(settings.database_url, echo=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Hanldle application startup and shutdown events.
    Args:
        app (FastAPI): _description_
    """    
    try:
        SQLModel.metadata.create_all(engine)
        yield
    except Exception as e:
        print(f"Error during startup: {e}")
    finally:
        print("Shutting down...")

app = FastAPI(title="Messages API", version="1.0.0", lifespan=lifespan)
app.include_router(router, prefix="/api")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(CustomAPIException, custom_exception_handler)