import datetime
from peewee import *

db = SqliteDatabase('catcodes.sqlite')

class Address(Model):
    url  = TextField()

    class Meta:
        database = db

class Code(Model):
    url = ForeignKeyField(Address, related_name='codes')
    status = TextField()
    requested_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db