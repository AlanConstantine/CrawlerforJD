# -*- coding: utf-8 -*-
# @Date  : 2017-10-05 12:15:26
# @Author: Alan Lau (rlalan@outlook.com)

from peewee import *
from datetime import datetime


sql_db = SqliteDatabase('JDwires.sqlite')
sql_db.connect()


class BaseModel(Model):

    class Meta:
        database = sql_db


class Wires(BaseModel):
    id = IntegerField(null=False, primary_key=True)
    url = CharField(null=False, max_length=1000)
    title = CharField(null=False, max_length=1000)
    price = FloatField()
    commentnum = CharField(null=False, max_length=1000)


class JDWires(BaseModel):
    id = IntegerField(null=False, primary_key=True)
    url = CharField(null=False)
    title = CharField(null=False)
    price = FloatField()
    comm_num = CharField(null=False)
    introduction = CharField(null=False)
    specification = CharField(null=False)
    aftersale = CharField(null=False)
    comments = CharField(null=False)


if __name__ == '__main__':
    # Wires.create_table()
    JDWires.create_table()
