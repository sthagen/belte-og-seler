from fastapi import APIRouter, Request, Form, Depends, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from router.products import get_products

router = APIRouter()

templates = Jinja2Templates(directory='template')


@router.get("/", response_class=HTMLResponse)
def home(request: Request, products_cookie: str | None = Cookie(None)):
    print(products_cookie)
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/search", response_class=HTMLResponse)
def search(*, bar: str = Form(...), foos: int = Form(...), request: Request, session: Session = Depends(get_session)):
    products = get_products(bar=bar, foos=foos, session=session)
    return templates.TemplateResponse("search_results.html", {"request": request, "products": products})
