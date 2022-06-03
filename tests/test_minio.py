import json
import os

from fastapi.testclient import TestClient
from minio import Minio
from peewee import SqliteDatabase

from app._app import create_app
from app.custom_errors import BadRequestCodeError, PhotosLimitError, PhotosFormatError
import app.config as config
from app.config import minio_settings
from app.models import Data, RequestCode

db = SqliteDatabase("tests.db")
db.bind([Data, RequestCode], bind_refs=False, bind_backrefs=False)
db.connect()
db.create_tables([Data, RequestCode])
db.close() #  Wait for create_tables() to complete
db.connect() 

minio_client = Minio(
    **minio_settings,
)

app = create_app(db, minio_client, config)
test_client = TestClient(app)

def test_add_only_without_photo():
    response = test_client.post('/frames', files=[])
    assert response.status_code == 422


def test_add_max_15_photos():
    photo_name = 'tests/test1.jpeg'
    photos = [('files', (photo_name, open(photo_name, 'rb'), 'image/jpeg')) for i in range(16)]
    response = test_client.post('/frames', files=photos)
    
    assert response.status_code == 200
    assert json.loads(response.content)['status'] == PhotosLimitError

def test_add_get_delete_photos():
    photo_name1 = 'tests/test1.jpeg'
    photo_name2 = 'tests/test2.jpeg'
    photos = [
        ('files', (photo_name1, open(photo_name1, 'rb'), 'image/jpeg')),
        ('files', (photo_name2, open(photo_name2, 'rb'), 'image/jpeg')),
    ]
    
    response = test_client.post('/frames', files=photos)
    assert response.status_code == 200
    print(json.loads(response.content))
    req_code = json.loads(response.content).get("request_code")
    assert isinstance(req_code, int) 

    response = test_client.get(f'/frames/{req_code}')
    assert response.status_code == 200
    photos = json.loads(response.content).get('obj')
    assert len(photos) == 2

    assert 'content' in photos[0] 
    assert 'content' in photos[1]
    assert 'filename' in photos[0]
    assert 'filename' in photos[1]
    assert 'creation_datetime' in photos[0]
    assert 'creation_datetime' in photos[1]

    response = test_client.delete(f'/frames/{req_code}')
    assert response.status_code == 200
    assert json.loads(response.content).get("status") == "deleted"

    response = test_client.get(f'/frames/{req_code}')
    assert response.status_code == 200
    status = json.loads(response.content).get("status")
    print(status)
    assert status == BadRequestCodeError


def test_add_not_jpeg_photo_deny():
    photo_name = 'tests/test3.png'
    photos = (photo_name, open(photo_name, 'rb'), 'image/jpeg')
    response = test_client.post('/frames', files={ 'files': photos })
    
    assert response.status_code == 200
    assert json.loads(response.content)['status'] == PhotosFormatError


def test_get_photos_with_invalid_req_code():
    req_code = -1
    response = test_client.get(f'/frames/{req_code}')

    assert response.status_code == 200
    assert json.loads(response.content)['status'] == BadRequestCodeError
