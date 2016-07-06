import os
from peewee import *

db = MySQLDatabase(None)


def refresh_unittest_db():
    """Drop and create all tables in unittest db."""
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='unittest',
            password='test_db',
            database='test_db',
            charset='utf8')
    db.connect()
    print("Deleting unittest tables")
    db.drop_tables([Lend, Administrator, Review, Customer, Genre, BookGenre,
                   Book, Publisher, Author], safe=True, cascade=True)
    print("Tables deleted")
    print("Creating new tables")
    db.create_tables([Publisher, Author, Book, Genre,
                     BookGenre, Customer, Lend, Review, Administrator],
                     safe=True)
    print("Tables created")
    print("done\n\n")


def refresh_development_db():
    """Drop and create all tables in development db."""
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='development',
            password='devpassword',
            database='devdatabase',
            charset='utf8')
    db.connect()
    print("Deleting development tables")
    db.drop_tables([Lend, Administrator, Review, Customer, Genre, BookGenre,
                   Book, Publisher, Author], safe=True, cascade=True)
    print("Tables deleted")
    print("Creating new tables")
    db.create_tables([Publisher, Author, Book, Genre,
                     BookGenre, Customer, Lend, Review, Administrator],
                     safe=True)
    print("Tables created")
    print("done\n\n")


class BaseModel(Model):
    class Meta:
        database = db


class Publisher(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=256)
    city = CharField(max_length=256)

    @staticmethod
    def add_publisher(name, city):
        if len(name) <= 265 and len(city) <= 256:
            return Publisher.create(name=name, city=city)
        return None

    @staticmethod
    def select_all():
        publishers = Publisher.select()
        if publishers:
            return publishers
        return None

    @staticmethod
    def update_selected(publisher_id, name=None, city=None):
        try:
            publisher = Publisher.get(Publisher.id == publisher_id)
            if name and len(name) <= 265:
                publisher.name = name
            if city and len(city) <= 265:
                publisher.city = city
            publisher.save()
            return True
        except Publisher.DoesNotExist:
            return None
        return False

    @staticmethod
    def delete_selected(publisher_id):
        try:
            Publisher.get(Publisher.id == publisher_id).delete_instance()
            return True
        except DoesNotExist:
            return None


class Author(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=256)
    biography = TextField()
    age = SmallIntegerField()

    @staticmethod
    def add_author(name, biography, age):
        if len(name) <= 256:
            try:
                return Author.create(name=name, biography=biography, age=age)
            except ValueError:
                return False
        return None

class Book(BaseModel):
    id = PrimaryKeyField()
    isbn = CharField(unique=True)
    title = CharField(max_length=32)
    author_id = ForeignKeyField(Author, related_name='written_by')
    publisher_id = ForeignKeyField(Publisher,
                                   related_name='published_by')
    amount_of_pages = SmallIntegerField()
    book_print = SmallIntegerField()
    edition = SmallIntegerField()
    summary = TextField()
    published_at = DateField(formats="%Y-%m-%d")
    language = CharField(max_length=64)
    # types: hardcover, paperback, pdf, e-book etc.
    book_type = CharField(max_length=16)
    amount = SmallIntegerField(default=0)


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


class Lend(BaseModel):
    id = PrimaryKeyField()
    book_id = ForeignKeyField(Book)
    customer_id = ForeignKeyField(Customer, related_name='borrowed_by')
    return_date = DateField(formats="%Y-%m-%d")
    returned_at = DateField(formats="%Y-%m-%d")


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


if __name__ == '__main__':
    refresh_unittest_db()
    refresh_development_db()
