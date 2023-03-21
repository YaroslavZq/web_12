import time

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from fastapi_limiter import FastAPILimiter
import redis.asyncio as redis
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import contacts, birthdays, auth, users
from src.conf.config import settings

app = FastAPI()

origins = [
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called &quot;My-Process-Time&quot;
    that contains the time it took for this function to run. This is useful for debugging purposes.

    :param request: Request: Access the request object
    :param call_next: Call the next middleware in the chain
    :return: A response object
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response


@app.get("/", name='Корінь проекту')
def read_root():
    """
    The read_root function returns a dictionary with the key &quot;message&quot; and value &quot;REST APP v0.2&quot;.
    This is the root of our API, so it's just a simple message.

    :return: A dictionary with a message
    :doc-author: Trelent
    """
    return {"message": "REST APP v1.2"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    """
    The healthchecker function is a simple function that checks if the database is configured correctly.
    It does this by making a request to the database and checking if it returns any results.
    If there are no results, then we know something went wrong with our configuration.

    :param db: Session: Get the database session
    :return: A dictionary with a message
    :doc-author: Trelent
    """
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are used by the app, such as databases or caches.

    :return: A list of objects to be passed to the application
    :doc-author: Trelent
    """
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)

app.include_router(contacts.router, prefix='/api')
app.include_router(birthdays.router, prefix='/api')
app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
