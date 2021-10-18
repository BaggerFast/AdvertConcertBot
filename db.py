from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey

# Метаданные-это информация о данных в БД; например, информация о таблицах и столбцах, в которых мы храним данные.
meta = MetaData()

# создаём таблицы
authors = Table('Authors', meta,
                Column('id', Integer, primary_key=True),
                Column('name', String(250), nullable=False),
                Column('photo', String(250), nullable=False)
                )

books = Table('Tracks', meta,
              Column('id', Integer, primary_key=True),
              Column('track', String(250), nullable=False),
              Column('author_id', Integer, ForeignKey("Authors.id"), nullable=False),
              )

# подключаемся к бд и заносим данные
# субд+драйвер://юзер:пароль@хост:порт/база
engine = create_engine('sqlite:///college.db', echo=True)
books.create(engine)

conn = engine.connect()

"""ins_author_query = authors.insert().values(name = 'Lutz')
conn.execute(ins_author_query)

ins_book_query = books.insert().values(title = 'Learn Python', author_id = 1, genre = 'Education', price = 1299)
conn.execute(ins_book_query)
ins_book_query2 = books.insert().values(title = 'Clear Python', author_id = 1, genre = 'Education', price =956)
conn.execute(ins_book_query2)"""

# books_gr_1000_query = books.select().where(books.c.price > 1000) # SELECT * FROM Books WHERE Books.price > 1000;
# result = conn.execute(books_gr_1000_query)
#
# for row in result:
#    print (row)
#
# print()
#
# s = select([books, authors]).where(books.c.author_id == authors.c.id_author)
# result = conn.execute(s)
#
# for row in result:
#    print (row)
