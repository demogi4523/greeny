from peewee import (
    Model, CharField, BooleanField, Proxy,
)

px = Proxy()

class User(Model):
    class Meta:
        database = px
    
    username = CharField()
    hashed_password = CharField(max_length=512)
    email = CharField() # add email validation
    full_name = CharField()
    disabled = BooleanField()
