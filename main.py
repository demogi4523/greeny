import base64
from datetime import datetime
import io
import string
from uuid import uuid4
from fastapi import FastAPI, File
from minio import Minio
from peewee import Model, ForeignKeyField, AutoField, CharField, DateTimeField, PostgresqlDatabase

db = PostgresqlDatabase(
    'storage_db', 
    host='localhost', 
    port=5432, 
    user='postgres', 
    password='mysecretpassword'
)

class User(Model):
    pass

class Data(Model):
    class Meta:
        database = db
        db_table = 'inbox'
    
    # user = ForeignKeyField(User, backref='data')
    req_code = AutoField()
    filename = CharField(max_length=512) #fix max length for uuid4
    creation_datetime = DateTimeField(default=datetime.now)

endpoint = '127.0.0.1:9000'
access_key = 'user1'
secret_key = 'password1'

client = Minio(
    endpoint=endpoint,
    access_key=access_key,
    secret_key=secret_key,
    secure=False,
)
app = FastAPI()


@app.get("/")
async def main():
    return {
        "qq": "adsfa",
    }


@app.post("/frames")
def create_upload_file(f:bytes = File()):
    bucket_name = str(datetime.today().strftime('%Y-%m-%d'))
    # print(bucket_name)
    ex = client.bucket_exists(bucket_name)
    if not ex:
        client.make_bucket(bucket_name)
    
    obj_name = f"{uuid4()}.jpg"
    b = io.BytesIO(f)
    l = len(f)
    res = client.put_object(bucket_name, obj_name, b, l)

    print(res)

    data = Data.create(
        filename = obj_name,
    )
    req_code = data.req_code
    return {"request_code": req_code}


@app.get("/frames/{req_code}")
def get_data_by_req_code(req_code: int):
    data = Data.get(Data.req_code == req_code)
    bucket_name = str(data.creation_datetime.date())
    # print(type(data.creation_datetime))
    # print(data.creation_datetime.date())
    # print(bucket_name)
    # .today().strftime('%Y-%m-%d')
    obj = client.get_object(bucket_name, data.filename)
    # print(type(obj))
    # print(obj.read())
    q = obj.read()
    res = base64.b64encode(q)
    # res = [chr(int(str(i))) for i in set(res)]
    # print(res)
    # print(len(res))
    return {
        'obj': res,
        'req_code': data.req_code,
        'filename': data.filename,
        'creation_datetime': data.creation_datetime,
    }

@app.delete("/frames/{req_code}")
def delete_data_by_req_code(req_code: int):
    data = Data.get(Data.req_code == req_code)
    data.delete_instance()
    return {
        "status": "deleted",
    }


db.connect()
db.create_tables([
    # User, 
    Data,
])
