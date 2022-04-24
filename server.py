import uvicorn
from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from router import products, web, auth
from router.products import BadBuildException

app = FastAPI(title="Belt and Braces")
app.include_router(web.router)
app.include_router(products.router)
app.include_router(auth.router)

origins = [
    "http://localhost:8081",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.exception_handler(BadBuildException)
async def unicorn_exception_handler(request: Request, exc: BadBuildException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"},
    )


# @app.middleware("http")
# async def add_cars_cookie(request: Request, call_next):
#     response = await call_next(request)
#     response.set_cookie(key="cars_cookie", value="you_visited_the_carsharing_app")
#     return response


if __name__ == "__main__":
    uvicorn.run("server:app", port=8081, reload=True)
