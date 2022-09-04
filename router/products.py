from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from model import Build, BuildInput, Product, ProductInput, ProductOutput, User
from router.auth import get_current_user

router = APIRouter(prefix='/api/products')


@router.get('/')
def get_products(product: str | None = None, session: Session = Depends(get_session)) -> list:
    query = select(Product)
    if product:
        query = query.where(Product.product == product)
    return session.exec(query).all()


@router.get('/{id}', response_model=ProductOutput)
def product_by_id(id: int, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.post('/', response_model=Product)
def add_product(
    product_input: ProductInput, session: Session = Depends(get_session), user: User = Depends(get_current_user)
) -> Product:
    new_product = Product.from_orm(product_input)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product


@router.delete('/{id}', status_code=204)
def remove_product(id: int, session: Session = Depends(get_session)) -> None:
    product = session.get(Product, id)
    if product:
        session.delete(product)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.put('/{id}', response_model=Product)
def change_product(id: int, new_data: ProductInput, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, id)
    if product:
        product.family = new_data.family
        product.product = new_data.product
        product.description = new_data.description
        session.commit()
        return product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


class BadBuildException(Exception):
    pass


@router.post('/{product_id}/builds', response_model=Build)
def add_build(product_id: int, build_input: BuildInput, session: Session = Depends(get_session)) -> Build:
    product = session.get(Product, product_id)
    if product:
        new_product = Build.from_orm(build_input, update={'product_id': product_id})
        # if new_product.end < new_product.start:
        #    raise BadBuildException("Build end before start")
        product.builds.append(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')
