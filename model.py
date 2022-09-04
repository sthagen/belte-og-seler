import datetime as dti
from passlib.context import CryptContext
from sqlmodel import VARCHAR, Column, Field, Relationship, SQLModel

pwd_context = CryptContext(schemes=['bcrypt'])


class UserOutput(SQLModel):
    id: int
    username: str


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column('username', VARCHAR, unique=True, index=True))
    password_hash: str = ''

    def set_password(self, password):
        """Setting the passwords actually sets password_hash."""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash."""
        return pwd_context.verify(password, self.password_hash)


class BuildInput(SQLModel):
    description: str | None = ''
    source: str | None = ''
    version: str | None = ''
    timestamp: str = Field(default=dti.datetime.now(dti.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f +00:00'))
    target: str | None = Field(default='')
    sha512: str | None = Field(default='cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e')
    class Config:
        schema_extra = {
            'example': {
                'description': 'the precious build',
                'source': 'https://example.com/vcs/branch/xyz/',
                'version': '2022.9.4',
                'timestamp': '2022-09-04 19:20:21.123456 +00:00.',
                'target': 'https://example.com/brm/family/product/version/',
                'sha512': 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
            }
        }


class BuildOutput(BuildInput):
    id: int


class Build(BuildInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    product: "Product" = Relationship(back_populates="builds")


class ProductInput(SQLModel):
    family: str
    product: str
    description: str

    class Config:
        schema_extra = {
            'example': {
                'family': 'things',
                'product': 'thing',
                'description': 'The simple thing.'
            }
        }


class Product(ProductInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    builds: list[Build] = Relationship(back_populates="product")


class ProductOutput(ProductInput):
    id: int
    builds: list[BuildOutput] = []
