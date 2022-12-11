from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app
from dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '13337704198',
            'identify_number': '320102200108300814',
            'password': '123'
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['name'] == 'foo'
    assert 'id' in data
    user_id = data['id']

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "foo"
    assert data["id"] == user_id


def test_create_user_existing_name():
    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '13337704199',
            'identify_number': '320102200108300815',
            'password': '123'
        }
    )
    assert response.status_code == 201


def test_create_user_existing_phone_number():
    response = client.post(
        '/users/',
        json={
            'name': 'bar',
            'phone_number': '13337704198',
            'identify_number': '320102200108300816',
            'password': '123'
        }
    )
    assert response.status_code == 409
