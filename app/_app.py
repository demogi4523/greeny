import io
import base64
from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import (
    FastAPI, File,
)
from fastapi.responses import RedirectResponse


from PIL import Image
import requests as r

from app.custom_errors import BadRequestCodeError, PhotosFormatError, PhotosLimitError
from app.models import (
    RequestCode, Data, main_px, 
    User, auth_px,
)
from app.auth import add_auth_to_app





def create_app(db, minio_client, config):
    main_px.initialize(db)
    auth_px.initialize(db)

    client_id = config.oauth2_github_client_id
    client_secret = config.oauth2_github_client_secret

    app = FastAPI()

    add_auth_to_app(app)

    @app.get("/q")
    def intermediate_oauth2_page(code: str):
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
        }

        resp = r.post(
            'https://github.com/login/oauth/access_token', 
            headers={'Accept': 'application/json'},
            data=data,
        )
        
        access_token = resp.json()['access_token']
        auth_headers = {'Authorization': f'token {access_token}'}
        resp = r.get('https://api.github.com/user', headers=auth_headers)
        payload = resp.json()

        result = {
            'login': payload['login'],
            'email': payload['email'],
        }

        return result

    @app.get("/")
    def oauth2_github_login():
        url = f'https://github.com/login/oauth/authorize?client_id={client_id}'
        return RedirectResponse(url)


    @app.post("/frames")
    def create_upload_file(files: List[bytes] = File()):
        """Download photos to min.io custom server"""
        amount_of_pictures = len(files)
        if amount_of_pictures > 15 or amount_of_pictures < 1:
            return {
                'status': PhotosLimitError,
            }
        
        bucket_name = str(datetime.today().strftime('%Y-%m-%d'))
        ex = minio_client.bucket_exists(bucket_name)
        if not ex:
            minio_client.make_bucket(bucket_name)

        req_code = RequestCode.create().req_code
        
        for img in files:
            format = Image.open(io.BytesIO(img)).format
            if format != 'JPEG':
                return {
                    'status': PhotosFormatError,
                }
            obj_name = f"{uuid4()}.jpg"
            b = io.BytesIO(img)
            l = len(img)
            minio_client.put_object(bucket_name, obj_name, b, l)

            Data.create(
                req_code = req_code,
                filename = obj_name,
            )

        return {"request_code": req_code}


    @app.get("/frames/{req_code}")
    def get_data_by_req_code(req_code: int):
        data = Data.select().where(Data.req_code == req_code)
        repr(data)
        if len(data) == 0:
            return {
                "status": BadRequestCodeError
            }
        bucket_name = str(data[0].creation_datetime.date())

        res = []
        for img in data:
            obj = minio_client.get_object(bucket_name, img.filename)
            q = obj.read()
            res.append({
                'content': base64.b64encode(q),
                'filename': img.filename,
                'creation_datetime': img.creation_datetime,
            })

        return {
            'obj': res,
        }

    @app.delete("/frames/{req_code}")
    def delete_data_by_req_code(req_code: int):
        data = Data.select().where(Data.req_code == req_code)
        if len(data) == 0:
            return {
                "status": BadRequestCodeError
            }
        
        bucket_name = str(data[0].creation_datetime.date())

        for el in data:
            minio_client.remove_object(bucket_name, el.filename)
            el.delete_instance()

        rc = RequestCode.get(RequestCode.req_code == req_code)
        rc.delete_instance()

        return {
            "status": "deleted",
        }

    @app.on_event("startup")
    def db_statup():
        db.connect()
        db.create_tables([
            RequestCode,
            Data,
            User,
        ], safe=True)
        db.close()
        db.connect()

        User.get_or_create(
            username = 'test',
            hashed_password = '$2b$12$S7d3IY6iYaZw00VnWQ0N8eZekQkRnWn4QOC.VNWLxaqiYAZ3rvvQu',
            email = 'test@example.com', # add email validation
            full_name = '',
            disabled = False,
        )
        User.get_or_none()

    @app.on_event("shutdown")        
    def db_shutdown():
        if not db.is_closed():
            db.close()

    return app
