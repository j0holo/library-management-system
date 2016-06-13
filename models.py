from peewee import *

db = MySQLDatabase(host='localhost',
                   user='unittest',
                   password='test_db',
                   database='test_db',
                   charset='utf8')


class BaseModel(Model):
    class Meta:
        database = db


class Publisher(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    summary = TextField()
    age = SmallIntegerField()


class Book(BaseModel):
    id = PrimaryKeyField()
    isbn = CharField(unique=True)
    title = CharField(max_length=32)
    author = CharField(max_length=256)
    published_id = ForeignKeyField(Publisher,
                                   related_name='published_by')
    amount_of_pages = SmallIntegerField()
    book_print = SmallIntegerField()
    edition = SmallIntegerField()
    summary = TextField()
    published_at = DateField(formats="%Y-%m-%d")
    language = CharField(max_length=64)


class Amount(BaseModel):
    id = PrimaryKeyField()
    book_id = ForeignKeyField(Book)
    paperback = SmallIntegerField()
    hardcover = SmallIntegerField()
    pdf = SmallIntegerField()
    ebook = SmallIntegerField()


class Genre(BaseModel):
    id = PrimaryKeyField()
    genre = CharField(unique=True)


class BookGenre(BaseModel):
    id = PrimaryKeyField()
    book_id = ForeignKeyField(Book)
    genre_id = ForeignKeyField(Genre)


class Customer(BaseModel):
    id = PrimaryKeyField()
    # max length of e-mail address is 256 chars
    email = CharField(max_length=256)
    password = CharField(max_length=128)
    first_name = CharField(max_length=128)
    surname = CharField(max_length=128)


class Review(BaseModel):
    id = PrimaryKeyField()
    customer_id = ForeignKeyField(Customer, related_name='reviewed_by')
    book_id = ForeignKeyField(Book)
    text = TextField()
    published_at = DateField(formats="%Y-%m-%d")
    rating = SmallIntegerField()


class Administrator(BaseModel):
    id = PrimaryKeyField()
    email = CharField(max_length=256)
    password = CharField(max_length=128)


if __name__ == "__main__":
    db.connect()
    db.create_tables([Publisher, Book, Amount, Genre,
                     BookGenre, Customer, Review, Administrator],
                     safe=True)
    print("done")
