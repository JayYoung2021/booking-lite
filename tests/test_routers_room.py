import os

import pytest

from utils import client


def test_create_room():
    response = client.post(
        '/rooms/',
        json={
            'room_number': '1234',
            'type_': 'single',
            'price': 42
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data['room_number'] == '1234'
    assert 'id' in data
    room_id = data['id']

    response = client.get(f'/rooms/{room_id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['room_number'] == '1234'
    assert data['id'] == room_id


def test_create_room_existing_room_number():
    response = client.post(
        '/rooms/',
        json={
            'room_number': '3444',
            'type_': 'twin',
            'price': 3.44
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/rooms/',
        json={
            'room_number': '3444',
            'type_': 'family',
            'price': 4.55
        }
    )
    assert response.status_code == 409


def test_read_room():
    response = client.post(
        '/rooms/',
        json={
            'room_number': '5666',
            'type_': 'twin',
            'price': 58
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/rooms/',
        json={
            'room_number': '6666',
            'type_': 'twin',
            'price': 68.8
        }
    )
    assert response.status_code == 201

    response = client.get(
        '/rooms/',
    )
    assert response.status_code == 200


def test_read_room_nonexistent():
    response = client.get(
        '/rooms/?room_number=8333',
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == 0


def test_read_room_by_price():
    response = client.post(
        '/rooms/',
        json={
            'room_number': '9666',
            'type_': 'family',
            'price': 998
        }
    )
    assert response.status_code == 201

    response = client.post(
        '/rooms/',
        json={
            'room_number': '1066',
            'type_': 'family',
            'price': 1000
        }
    )
    assert response.status_code == 201

    response = client.get(
        '/rooms/?type_=family&price_min=997.99&price_max=1000.01',
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    assert (data[0]['price'] == 998, data[1]['price'] == 1000) \
           or (data[0]['price'] == 1000, data[1]['price'] == 998)


@pytest.fixture(scope='session', autouse=True)
def db_conn():
    yield
    # Will be executed after the last test
    files = ('test.db', 'sql_app.db')
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
