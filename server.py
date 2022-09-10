import uvicorn  # type: ignore
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from router import auth, products, web
from router.products import BadBuildException

HOST = '127.0.0.1'
PORT = 8003
BASE = ''

app = FastAPI(
    title='Belt and Braces',
    openapi_url=f'{BASE}/api/v1/openapi.json',
    docs_url=f'{BASE}/documentation',
    redoc_url=None,
    description='The blurb ...',
    version='2022.9.7',
)

app.include_router(web.router, prefix=BASE)
app.include_router(products.router, prefix=BASE)
app.include_router(auth.router, prefix=BASE)

origins = [
    'http://localhost:8004',
    'http://localhost:8003',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.on_event('startup')
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.exception_handler(BadBuildException)
async def unicorn_exception_handler(request: Request, exc: BadBuildException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={'message': 'Bad Build'},
    )


# @app.middleware('http')
# async def add_products_cookie(request: Request, call_next):
#     response = await call_next(request)
#     response.set_cookie(key='products_cookie', value='you_were_already_here')
#     return response


if __name__ == '__main__':
    print(f'Starting notary service at https://{HOST}:{PORT}{BASE}/')
    uvicorn.run('server:app', host=HOST, port=PORT, reload=True)
