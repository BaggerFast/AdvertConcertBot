from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey


class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        meta = MetaData()
        self.conn = self.engine.connect()
        self.authors = Table('Authors', meta,
                             Column('id', Integer, primary_key=True),
                             Column('name', String(250), nullable=False),
                             Column('photo', String(250), nullable=False)
                             )

        self.music = Table('Tracks', meta,
                           Column('id', Integer, primary_key=True),
                           Column('track', String(250), nullable=False),
                           Column('author_id', Integer, ForeignKey("Authors.id")),
                           )

    def get_authors(self):
        return self.conn.execute(self.authors.select())

    def get_authors_by_id(self, id):
        try:
            return list(self.conn.execute(self.authors.select().where(self.authors.c.id == id)))[0]
        except IndexError:
            return False

    def get_music_by_author_id(self, author_id):
        return self.conn.execute(select(self.music.c.track).where(self.music.c.author_id == author_id))