# coding=utf-8
__author__ = 'BaiYa'

from sqlalchemy import *

db = create_engine("sqlite:///example.db")
metadata = MetaData(db)
user_table = Table('users', metadata,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('name', String(40)),
                   Column('email', String(120)))
user_table.create()

i = user_table.insert()
i.execute(name='engle', email='engle@qq.com')
i.execute({'name':'ghost'}, {'name':'test'})

