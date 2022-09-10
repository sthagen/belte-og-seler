from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from model import Build, BuildInput, Product, ProductInput, ProductOutput, User
from router.auth import get_current_user

router = APIRouter(prefix='/api/products')


@router.get('/')
def get_products(name: str | None = None, session: Session = Depends(get_session)) -> list:
    query = select(Product)
    if name:
        query = query.where(Product.name == name)
    return session.exec(query).all()


@router.get('/{id}', response_model=ProductOutput)
def product_by_id(id: int, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.get('/{product_id}/builds', response_model=List)
def get_product_builds(product_id: int, session: Session = Depends(get_session)) -> List:
    product = session.get(Product, product_id)
    if product:
        return product.builds
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.get('/{product_id}/builds/{id}', response_model=Build)
def get_product_build_by_id(product_id: int, id: int, session: Session = Depends(get_session)) -> Build:
    product = session.get(Product, product_id)
    if product:
        for build in product.builds:
            if build.id == id:
                return build
        raise HTTPException(status_code=404, detail=f'No product/build with ids={product_id}/{id}.')
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={product_id}.')


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
def remove_product(id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)) -> None:
    product = session.get(Product, id)
    if product:
        session.delete(product)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.put('/{id}', response_model=Product)
def change_product(
    id: int, new_data: ProductInput, session: Session = Depends(get_session), user: User = Depends(get_current_user)
) -> Product:
    product = session.get(Product, id)
    if product:
        product.family = new_data.family
        product.name = new_data.name
        product.description = new_data.description
        session.commit()
        return product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


@router.patch('/{id}', response_model=Product)
def patch_product(
    id: int,
    family: str | None = None,
    name: str | None = None,
    description: str | None = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Product:
    product = session.get(Product, id)
    if product:
        if family:
            product.family = family
        if name:
            product.name = name
        if description:
            product.description = description
        session.commit()
        return product
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={id}.')


class BadBuildException(Exception):
    pass


@router.post('/{product_id}/builds', response_model=Build)
def add_build(
    product_id: int,
    build_input: BuildInput,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Build:
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


@router.patch('/{product_id}/builds/{id}', response_model=Build)
def patch_product_build(
    product_id: int,
    id: int,
    description: str | None = None,
    version: str | None = None,
    target: str | None = None,
    taxonomy: str | None = None,
    sha512: str | None = None,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Build:
    product = session.get(Product, product_id)
    if product:
        for slot, build in enumerate(product.builds):
            if build.id == id:
                if description:
                    build.description = description
                if version:
                    build.version = version
                if target:
                    build.target = target
                if taxonomy:
                    build.taxonomy = taxonomy
                if sha512:
                    build.sha512 = sha512
                product.builds[slot] = build
                session.commit()
                return build
        raise HTTPException(status_code=404, detail=f'No product/build with ids={product_id}/{id}.')
    else:
        raise HTTPException(status_code=404, detail=f'No product with id={product_id}.')
