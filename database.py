from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from misc import Settings


class Database:
    Base = declarative_base()

    class Tracks(Base):
        __tablename__ = 'Tracks'
        id = Column(Integer, primary_key=True)
        track = Column(String(250), nullable=False)
        author_id = Column(Integer, ForeignKey("Authors.id"))

    class Author(Base):
        __tablename__ = 'Authors'
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        photo = Column(String(250), nullable=False)
        music = relationship("Tracks")

    class Users(Base):
        __tablename__ = 'Users'
        id = Column(Integer, primary_key=True)
        vk_id = Column(Integer, nullable=False)
        state_id = Column(Integer, default=0, nullable=False)

    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True if Settings.debug else False)
        self.session = sessionmaker(bind=self.engine)()

    def create(self):
        self.Base.metadata.create_all(self.engine)

    def get_users_by_id(self, user_id):
        try:
            return self.session.query(self.Users).filter(self.Users.vk_id == user_id).one()
        except exc.NoResultFound:
            return False

    def get_authors(self):
        return self.session.query(self.Author).all()

    def get_authors_by_id(self, key):
        try:
            return self.session.query(self.Author).filter(self.Author.id == key).one()
        except exc.NoResultFound:
            return False


if __name__ == "__main__":
    a = Database()
    a.create()
