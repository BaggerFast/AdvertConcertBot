from typing import Union
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from misc.addition import Settings


class Database:
    __Base = declarative_base()

    # tables
    class Tracks(__Base):
        __tablename__ = 'Tracks'
        id = Column(Integer, primary_key=True)
        track = Column(String(250), nullable=False)
        author_id = Column(Integer, ForeignKey("Authors.id"))

    class Author(__Base):
        __tablename__ = 'Authors'
        id = Column(Integer, primary_key=True)
        name = Column(String(250), nullable=False)
        photo = Column(String(250), nullable=False)
        music = relationship("Tracks")

    class Users(__Base):
        __tablename__ = 'Users'
        id = Column(Integer, primary_key=True)
        vk_id = Column(Integer, nullable=False)
        state_id = Column(Integer, default=0, nullable=False)
        selected_author = relationship("SelectedAuthor", uselist=False, backref="Users")

    class SelectedAuthor(__Base):
        __tablename__ = 'SelectedAuthor'
        id = Column(Integer, primary_key=True)
        author_id = Column(Integer, default=0, nullable=False)
        user_id = Column(Integer, ForeignKey('Users.id'))

    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True if Settings.debug else False)
        self.session = sessionmaker(bind=self.engine)()
        self.create()

    def create(self):
        self.__Base.metadata.create_all(self.engine)

    # get
    @property
    def get_authors(self):
        return list(self.session.query(self.Author).order_by(self.Author.id))

    def get_authors_by_id(self, key: int):
        try:
            return self.session.query(self.Author).filter(self.Author.id == key).one()
        except exc.NoResultFound:
            return None

    def get_users_by_id(self, key: int):
        try:
            return self.session.query(self.Users).filter(self.Users.vk_id == key).one()
        except exc.NoResultFound:
            return False

    def get_user_selected_author(self, user: Union[int, Users]):
        if isinstance(user, int):
            user = self.get_users_by_id(user)
        return user.selected_author.author_id

    # create
    def create_user_if_not_exists(self, key) -> Users:
        user = self.get_users_by_id(key)
        if not user:
            user = self.Users(vk_id=key, state_id=0)
            self.session.add(user)
            self.session.commit()
        return user

    # set
    def set_user_state(self, user: Union[int, Users], state_id):
        if isinstance(user, int):
            user = self.get_users_by_id(user)
        user.state_id = state_id
        self.session.commit()

    def set_user_selected_author(self, user: Union[int, Users], selected: int):
        if isinstance(user, int):
            user = self.get_users_by_id(user)
        if user.selected_author:
            user.selected_author.author_id = selected
            self.session.add(user)
        else:
            selected = self.SelectedAuthor(user_id=user.id, author_id=selected)
            self.session.add(selected)
        self.session.commit()
