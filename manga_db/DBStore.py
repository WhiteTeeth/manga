# coding=utf-8
__author__ = 'BaiYa'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

engine = create_engine('sqlite:///manga.db', echo=False, encoding='utf-8', convert_unicode=False)
Base = declarative_base()
init_db()
Session = sessionmaker(bind=engine)
session = Session()

class Manga(Base):

    __tablename__ = 'manga'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    name_pinyin = Column(String)
    author = Column(String)
    introduction = Column(String)
    added_at = Column(Date, default=func.now())
    update_at = Column(Date, default=func.now())
    poster = Column(String)
    source = Column(String, nullable=False)

    def __setattr__(self, key, value):
        if ((value) and (key == 'name' or key == 'name_pinyin' or key == 'author' or key == 'introduction')):
            super.__setattr__(self, key, value.decode('utf-8'))
        else:
            super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

    def __repr__(self):
        return "<Manga (name='%s', name_pinyin='%s', author='%s', added_at='%s', update_at='%s', introduction='%s', poster='%s', source='%s')>" \
               % (self.name, self.name_pinyin, self.author, self.added_at, self.update_at, self.introduction, self.poster, self.source)

class Plot(Base):

    __tablename__ = "plot"

    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer, ForeignKey(str('%s.id' % str(Manga.__tablename__))))
    index = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    added_at = Column(DateTime, default=func.now())

    manga = relationship(Manga.__name__, backref = backref(__tablename__, order_by=id))

    def __setattr__(self, key, value):
        if (value and key == 'plot_title'):
            super.__setattr__(self, key, value.decode('utf-8'))
        else:
            super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

    def __repr__(self):
        return "<Plot ('manga_name=', 'index=%d', 'title=%s', link='%s')>" % (self.index, self.title, self.link)

class Pic(Base):

    __tablename__ = 'pic'

    id = Column(Integer, primary_key=True)
    plot_id = Column(Integer, ForeignKey(str('%s.id' % str(Plot.__tablename__))))
    page = Column(Integer, nullable=False)
    link = Column(String, nullable=False)
    source = Column(String, nullable=False)
    added_at = Column(DateTime, default=func.now())

    plot = relationship(Plot.__name__, backref = backref(__tablename__, order_by=id))

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

    def __repr__(self):
        return "<Pic ('plot_id=%d', 'page=%d', 'link=%s')>" % (self.plot_id, self.page, self.link)

class Request(Base):
    '''
    缓存url请求时间
    '''

    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    etag = Column(String)
    last_modified = Column(String, nullable=False)

    def __repr__(self):
        return "<Request ('id=%d', 'url=%s', 'etag=%s', 'request_time=%s')>" % (self.id, self.url, self.etag, str(self.request_time))
