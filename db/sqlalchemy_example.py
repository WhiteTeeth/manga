# coding=utf-8
__author__ = 'BaiYa'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///manga.db', echo=True, encoding='utf-8', convert_unicode=True)
Base = declarative_base()

class DB_Base(object):

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=func.now())
    pass


class Manga(Base):
    '''
    Manga Table
    id  |  Integer
    name | String
    name_pinyin | String
    '''
    __tablename__ = 'manga'

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=func.now())
    name = Column(String, nullable=False)
    name_pinyin = Column(String, nullable=False)
    author = Column(String)
    introduction = Column(String)

    def __setattr__(self, key, value):
        if (key == 'name' or key == 'name_pinyin' or key == 'author'):
            super.__setattr__(self, key, unicode(value, 'utf-8'))
        else:
            super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

    def __repr__(self):
        return "<Manga (name='%s', name_pinyin='%s')>" % (self.name, self.name_pinyin)

class Plot(Base):

    __tablename__ = "plot"

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=func.now())
    plot_id = Column(Integer, nullable=False)
    plot_title = Column(String, nullable=False)
    manga_id = Column(Integer, ForeignKey(str('%s.id' % str(Manga.__tablename__))))

    manga = relationship(Manga.__name__, backref = backref(__tablename__, order_by=id))

    def __setattr__(self, key, value):
        if (key == 'plot_title'):
            super.__setattr__(self, key, unicode(value, 'utf-8'))
        else:
            super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

    def __repr__(self):
        return "<Plot ('manga_id=%d', 'plot_id=%d', 'plot_title=%s')>" % (self.manga_id, self.plot_id, self.plot_title)

class Pic(Base):

    __tablename__ = 'pic'

    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, default=func.now())
    url = Column(String, nullable=False)
    plot_id = Column(Integer, ForeignKey(str('%s.id' % str(Plot.__tablename__))))

    Plot = relationship(Plot.__name__, backref = backref(__tablename__, order_by=id))

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)
        pass

    def __getattr__(self, key):
        super.__getattribute__(self, key)
        pass

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

if __name__ == "__main__":
    init_db()
    manga = Manga(name="海贼王", name_pinyin="haizeiwang")
    plot = Plot(plot_title='第1集', plot_id=1)
    manga.plot = [plot]
    print manga
    drop_db()

# Session = sessionmaker(bind=engine)
# session = Session()
# session.add(manga)
# session.commit()
# our_manga = session.query(Manga).filter_by(name=unicode("海贼王",'utf-8'))
# print(our_manga[-1].plot)

