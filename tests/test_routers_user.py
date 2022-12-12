import os
import logging

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import app
from dependencies import get_db

logger = logging.getLogger(__name__)

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
            'phone_number': '13337704100',
            'identify_number': '320102200108300800',
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
            'phone_number': '13337704101',
            'identify_number': '320102200108300801',
            'password': '123'
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '13337704102',
            'identify_number': '320102200108300802',
            'password': '123'
        }
    )
    assert response.status_code == 201


def test_create_user_existing_phone_number():
    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '13337704103',
            'identify_number': '320102200108300803',
            'password': '123'
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/users/',
        json={
            'name': 'bar',
            'phone_number': '13337704103',
            'identify_number': '320102200108300804',
            'password': '123'
        }
    )
    assert response.status_code == 409


def test_read_users():
    response = client.get(
        '/users/',
    )
    assert response.status_code == 200


def test_read_users_existing_name():
    response = client.post(
        '/users/',
        json={
            'name': 'david',
            'phone_number': '13337704107',
            'identify_number': '320102200108300807',
            'password': '123'
        }
    )
    assert response.status_code == 201

    response = client.get(
        '/users/?name=david',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'david'


def test_read_users_nonexistent_name():
    response = client.post(
        '/users/',
        json={
            'name': 'lucy',
            'phone_number': '13337704108',
            'identify_number': '320102200108300808',
            'password': '123'
        }
    )
    assert response.status_code == 201

    response = client.get(
        '/users/?name=lucifer',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 0


def test_read_users_existing_phone_number():
    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '133377041110',
            'identify_number': '320102200108300810',
            'password': '123'
        }
    )
    assert response.status_code == 201

    response = client.get(
        '/users/?phone_number=133377041110',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    logger.info(data)
    assert len(data) == 1
    assert data[0]['phone_number'] == '133377041110'


def test_read_users_nonexistent_phone_number():
    response = client.post(
        '/users/',
        json={
            'name': 'foo',
            'phone_number': '133377041111',
            'identify_number': '320102200108300811',
            'password': '123'
        }
    )
    assert response.status_code == 201, response.text

    response = client.get(
        '/users/?phone_number=133377041000',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 0


def test_delete_db():
    os.remove('test.db')
