"""Define peewee models for the databases.

Run "python models.py" to update the db's with latest changes
made to the models.
"""
import os
from peewee import *

db = MySQLDatabase(None)


def refresh_unittest_db():
    """Rebuild unittest db to apply new model changes."""
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='unittest',
            password='test_db',
            database='test_db',
            charset='utf8')
    db.connect()
    print("Deleting unittest tables")
    db.drop_tables([Lend, Administrator, Review, Customer,
                    Genre, BookGenre, Book, Publisher, Author],
                   safe=True, cascade=True)
    print("Tables deleted")
    print("Creating new tables")
    db.create_tables([Publisher, Author, Book, Genre,
                     BookGenre, Customer, Lend, Review, Administrator],
                     safe=True)
    print("Tables created")
    print("done\n\n")


def refresh_development_db():
    """Rebuild development db to apply new model changes."""
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
    """Publisher model.

    id - primary key of publisher
    name - name of the publisher
    city - city where from the publisher operates
    """

    id = PrimaryKeyField()
    name = CharField(max_length=256)
    city = CharField(max_length=256)

    @staticmethod
    def add_publisher(name, city):
        """Add a new publisher.

        name - name of the publisher
        city - city where from the publisher operates
        return - a publisher object when succesfull or
            None when parameter lengths are more than
            256 chars long
        """
        if len(name) <= 265 and len(city) <= 256:
            return Publisher.create(name=name, city=city)
        return None

    @staticmethod
    def select_all():
        """Return all publishers.

        return - a SelectQuery obj or None if no publishers where found
        """
        publishers = Publisher.select()
        if publishers:
            return publishers
        return None

    @staticmethod
    def update_selected(publisher_id, name=None, city=None):
        """Update the publisher by id.

        id - id of the publisher you want to update
        name - name of the publisher
        city - city where from the publisher operates
        return - a publisher object when succesfull or
            None when the id does not exist
        """
        try:
            publisher = Publisher.get(Publisher.id == publisher_id)
            if name and len(name) <= 265:
                publisher.name = name
            if city and len(city) <= 265:
                publisher.city = city
            publisher.save()
            return publisher
        except Publisher.DoesNotExist:
            return None
        # false will never be returned, also not tested (redundant?)
        return False

    @staticmethod
    def delete_selected(publisher_id):
        """Delete publisher by id.

        id - unique id of the publiser
        """
        try:
            Publisher.get(Publisher.id == publisher_id).delete_instance()
            return True
        except DoesNotExist:
            return None


class Author(BaseModel):
    """Author model.

    id - primary key of author
    name - name of the author
    biograpy - a string of text about the author
    age - age of the author
    """

    id = PrimaryKeyField()
    name = CharField(max_length=256)
    biography = TextField()
    # Should be changed to birthdate or born_at
    age = SmallIntegerField()

    @staticmethod
    def add_author(name, biography, age):
        """Add a new author.

        name - name of author
        biography - string of text about the author
        age - age of the author
        """
        if len(name) <= 256:
            try:
                return Author.create(name=name, biography=biography, age=age)
            except ValueError:
                # return value error if age is not a integer
                return ValueError
        return None

    @staticmethod
    def select_all():
        """Return all authors.

        return - a SelectQuery obj or None if no authors where found
        """
        authors = Author.select()
        if authors:
            return authors
        return None

    @staticmethod
    def update_selected(author_id, name=None, biography=None, age=None):
        """Update author by id.

        id - id of the author you want to update
        name - name of the author
        biography - string of text about the author
        age - age of the author
        return - author obj or None if author does not exist
        """
        try:
            author = Author.get(Author.id == author_id)
            if name and len(name) <= 256:
                author.name = name
            if biography:
                author.biography = biography
            if isinstance(age, int):
                author.age = age
            author.save()
            return author
        except Author.DoesNotExist:
            return None
        # false will never be returned
        # TODO: remove false or make it usefull again
        return False

class Book(BaseModel):
    """Book model.

    id - unique id of the book
    isbn - unique ISBN of the book, each type of book has its own
        ISBN. So hardcover is different compared to paperback
    title - title of the book
    author_id - foreign key to the author
    publisher_id - foreign key to the publisher
    amount_of_pages - the amount of pages the book contains
    book_print - from which print the book is e.g. second print
    edition - from which edition the book is e.g. third edition
    summary - a summary about the book
    published_at - date of publishment
    language - in which language the book has been written
    book_type - book type: hardcover, paperback, pdf, e-book etc.
    amount - how many copies the library has
    """

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
    book_type = CharField(max_length=16)
    amount = SmallIntegerField(default=0)


class Genre(BaseModel):
    """Genre model.

    id - primary key
    genre - genre of the story
    """

    id = PrimaryKeyField()
    genre = CharField(unique=True)


class BookGenre(BaseModel):
    """BookGenre many-to-many model.

    A book can have multiple genres.

    id - primary key
    book_id - primary key of the book
    genre_id - primary key of the genre
    """

    id = PrimaryKeyField()
    book_id = ForeignKeyField(Book)
    genre_id = ForeignKeyField(Genre)


class Customer(BaseModel):
    """Model for customer of the library.

    id - primary key
    email - email of the customer, max length is 254 chars (RFC 3696)
    password - the password hashed with bcrypt
    first_name - name of the customer
    surname - surname of the customer
    """

    id = PrimaryKeyField()
    email = CharField(max_length=254)
    password = CharField(max_length=128)
    first_name = CharField(max_length=128)
    surname = CharField(max_length=128)


class Lend(BaseModel):
    """Lend model.

    id - primary key
    book_id - id of the lend book
    customer_id - id of the customer
    return_date - date when book should be returned
    returned_at - date when the book was returned
    """

    id = PrimaryKeyField()
    book_id = ForeignKeyField(Book)
    customer_id = ForeignKeyField(Customer, related_name='borrowed_by')
    return_date = DateField(formats="%Y-%m-%d")
    returned_at = DateField(formats="%Y-%m-%d")


class Review(BaseModel):
    """Review model.

    id - primary key
    customer_id - id of the customer that reviewed the book
    book_id - id of the book that got reviewed
    text - review of the book. Maybe change this to 'review', 'text'
        is to general
    published_at - date when review got published
    rating - rating of the book
    """

    id = PrimaryKeyField()
    customer_id = ForeignKeyField(Customer, related_name='reviewed_by')
    book_id = ForeignKeyField(Book)
    text = TextField()
    published_at = DateField(formats="%Y-%m-%d")
    rating = SmallIntegerField()


class Administrator(BaseModel):
    """Administrator model.

    id - primary key
    email - email of the admin, max length is 254 chars (RFC 3696)
    password - hashed password with bcrypt
    """

    id = PrimaryKeyField()
    email = CharField(max_length=254)
    password = CharField(max_length=128)


if __name__ == '__main__':
    refresh_unittest_db()
    refresh_development_db()
