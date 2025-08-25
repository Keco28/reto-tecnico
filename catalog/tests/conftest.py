import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.database.db import get_db, Base
from app.database.models import Product
from app.database import schemas
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    product = Product(
        sku="ABC123",
        name="test1",
        description="desc1",
        base_price=200,
        currency="COP",
        category="categ1"
    )
    db.add(product)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    yield session
    session.close()
    
@pytest.fixture
def new_product():
    return schemas.ProductCreate(
        sku="serv123",
        name="serv",
        description="service test",
        base_price=40,
        currency="USD",
        category="service"
    )

@pytest.fixture
def existing_product():
    return schemas.ProductCreate(
        sku="ABC123",
        name="test1",
        description="desc1",
        base_price=200,
        currency="COP",
        category="categ1"
    )

@pytest.fixture
def updated_product():
    return schemas.ProductUpdate(
        name="new name",
        base_price=500
    )
    
@pytest.fixture
def request_data():
    return {
        "sku": "DEF4563",
        "name": "test2",
        "description": "desc2",
        "base_price": 3200,
        "currency": "USD",
        "category": "categ2"
    }