from datetime import datetime

from peewee import (
    Model, ForeignKeyField, AutoField, 
    CharField, DateTimeField, Proxy
)

px = Proxy()

class RequestCode(Model):
    class Meta:
        database = px
    
    req_code = AutoField()

# TODO: add support for minio user management
# class User(Model):
#     pass

class Data(Model):
    class Meta:
        database = px
        table_name = 'inbox'
    
    # user = ForeignKeyField(User, backref='data')
    req_code = ForeignKeyField(RequestCode, backref='data')
    filename = CharField(max_length=512) # TODO: fix max length for uuid4
    creation_datetime = DateTimeField(default=datetime.now)
