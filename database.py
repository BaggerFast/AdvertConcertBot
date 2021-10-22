from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


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

        def __repr__(self):
            print(self.name)

    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        self.session = sessionmaker(bind=self.engine)()

    def __create(self):
        self.Base.metadata.create_all(self.engine)

    def get_authors(self):
        return self.session.query(self.Author).all()

    def get_authors_by_id(self, key):
        return self.session.query(self.Author).filter(self.Author.id == key).one()


if __name__ == "__main__":
    a = Database()
    a.get_authors(3)
