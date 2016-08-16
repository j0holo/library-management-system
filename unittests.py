import unittest
import os
from models import *


class TestPublisherModel(unittest.TestCase):

    def setUp(self):
        db.connect()

    def tearDown(self):
        q = Publisher.delete()
        q.execute()
        db.close()

    # add_publisher()
    def test_add_publisher_returns_publisher(self):
        new_publisher = Publisher.add_publisher(
            name="Books from Holland", city="Amsterdam")

        self.assertTrue(isinstance(new_publisher, Publisher))

    def test_add_publisher_stored_in_db(self):
        publisher_name = "Written by U"
        city = "Amsterdam"
        Publisher.add_publisher(name=publisher_name, city=city)
        publisher_in_db = Publisher.get(
            Publisher.name == publisher_name)
        self.assertEqual(publisher_name, publisher_in_db.name)

    def test_add_publisher_name_length(self):
        publisher_name = "a" * 266
        city = "Amsterdam"
        publisher = Publisher.add_publisher(name=publisher_name,
                                            city=city)
        self.assertTrue(publisher is None)

    def test_add_publisher_city_length(self):
        publisher_name = "British Books"
        city = "a" * 266
        publisher = Publisher.add_publisher(name=publisher_name,
                                            city=city)
        self.assertTrue(publisher is None)

    # select_all()
    def test_select_all_publishers(self):
        name = "The German Writters"
        Publisher.create(name=name,
                         city="Berlin")
        publishers = Publisher.select_all()
        self.assertTrue(any(publisher.name == name
                        for publisher in publishers))

    def test_select_all_publishers_no_entries(self):
        publishers = Publisher.select_all()
        self.assertTrue(publishers is None)

    # update_selected()
    def test_update_publisher(self):
        publisher = Publisher.create(name="test", city="city")
        Publisher.update_selected(publisher, "new_test", "new_city")
        new_publisher = Publisher.get(Publisher.name == "new_test")
        self.assertEqual(new_publisher.city, "new_city")
        self.assertEqual(new_publisher.name, "new_test")

    def test_update_only_name(self):
        publisher = Publisher.create(name="name", city="city")
        Publisher.update_selected(publisher, "new_name")
        new_publisher = Publisher.get(Publisher.name == "new_name")
        self.assertEqual(new_publisher.name, "new_name")
        self.assertEqual(new_publisher.city, "city")

    def test_update_only_city(self):
        publisher = Publisher.create(name="name", city="city")
        Publisher.update_selected(publisher, city="new_city")
        new_publisher = Publisher.get(Publisher.name == "name")
        self.assertEqual(new_publisher.name, "name")
        self.assertEqual(new_publisher.city, "new_city")

    def test_update_string_length(self):
        publisher = Publisher.create(name="name", city="city")
        Publisher.update_selected(publisher, "a" * 266, "a" * 266)
        new_publisher = Publisher.get(Publisher.name == "name",
                                      Publisher.city == "city")
        self.assertEqual(new_publisher.name, "name")
        self.assertEqual(new_publisher.city, "city")

    def test_update_not_existing(self):
        publisher_updated = Publisher.update_selected(666, "new_name")
        self.assertTrue(publisher_updated is None)

    # delete_selected()
    def test_delete_existing_publisher(self):
        publisher = Publisher.create(name="name", city="city")
        self.assertTrue(Publisher.delete_selected(publisher.id))

    def test_delete_non_existing_publisher(self):
        self.assertFalse(Publisher.delete_selected(666))

class TestAuthorModel(unittest.TestCase):

    def setUp(self):
        db.connect()

    def tearDown(self):
        q = Author.delete()
        q.execute()
        db.close

    # add_author()
    def test_add_author_returns_author(self):
        new_author = Author.add_author("Mark Luther",
                                       "lorem ipsum",
                                       54)
        self.assertTrue(isinstance(new_author, Author))

    def test_add_author_stored_in_db(self):
        name = "Mark Luther"
        biography = "lorem ipsum"
        age = 54
        Author.add_author(name, biography, age)
        author_in_db = Author.get(Author.name == name,
                                  Author.biography == biography,
                                  Author.age == 54)
        self.assertTrue(author_in_db)

    def test_add_author_name_length(self):
        name = "a" * 266
        biography = "lorem ipsum"
        age = 54
        author_with_long_name = Author.add_author(name, biography, age)
        self.assertFalse(author_with_long_name)

    def test_add_author_age_must_be_int(self):
        name = "Mark Luther"
        biography = "lorem ipsum"
        age = "number"
        new_author = Author.add_author(name, biography, age)
        self.assertTrue(new_author is ValueError)

    # select_all()
    def test_select_all_authors(self):
        name = "Mark Luther"
        Author.create(name=name, biography="lorem ipsum", age=55)
        authors = Author.select_all()
        self.assertTrue(any(author.name == name
                        for author in authors))

    def test_select_all_authors_no_entries(self):
        authors = Author.select_all()
        self.assertTrue(authors is None)

    # update_selected()
    def test_update_author(self):
        name = "Friedrich Nietzsche"
        biography = "lorem ipsum"
        age = 55
        author = Author.create(name=name,
                               biography=biography,
                               age=age)

        Author.update_selected(author, name, biography, age)
        new_author = Author.get(Author.name == name)
        self.assertEqual(new_author.name, name)
        self.assertEqual(new_author.biography, biography)
        self.assertEqual(new_author.age, age)

    def test_update_only_name(self):
        name = "Plato"
        biography = "Greek philosopher"
        age = 67
        author = Author.create(name=name,
                               biography=biography,
                               age=age)

        name = "Friedrich Nietzsche"

        Author.update_selected(author, name=name)
        new_author = Author.get(Author.name == name)
        self.assertEqual(new_author.name, name)
        self.assertEqual(new_author.biography, biography)
        self.assertEqual(new_author.age, age)

    def test_update_only_biography(self):
        name = "Plato"
        biography = "Greek philosopher"
        age = 67
        author = Author.create(name=name,
                               biography=biography,
                               age=age)

        biography = "Updated biography"

        Author.update_selected(author, biography=biography)
        new_author = Author.get(Author.name == name)
        self.assertEqual(new_author.name, name)
        self.assertEqual(new_author.biography, biography)
        self.assertEqual(new_author.age, age)

    def test_update_only_age(self):
        name = "Plato"
        biography = "Greek philosopher"
        age = 67
        author = Author.create(name=name,
                               biography=biography,
                               age=age)

        age = 31

        Author.update_selected(author, age=age)
        new_author = Author.get(Author.name == name)
        self.assertEqual(new_author.name, name)
        self.assertEqual(new_author.biography, biography)
        self.assertEqual(new_author.age, age)

    def test_update_name_length(self):
        name = "Plato"
        biography = "Greek philosopher"
        age = 67
        author = Author.create(name=name,
                               biography=biography,
                               age=age)

        Author.update_selected(author, name="a" * 266)
        new_author = Author.get(Author.name == name)
        self.assertEqual(new_author.name, name)
        self.assertEqual(new_author.biography, biography)
        self.assertEqual(new_author.age, age)

    def test_update_not_existing(self):
        self.assertTrue(Author.update_selected(
                        1, name="does_not_exist")
                        is None)

    # delete_selected()
    def test_delete_existing_author(self):
        author = Author.create(name="Brian",
                               biography="lorem ipsum",
                               age=33)
        self.assertTrue(Author.delete_selected(author.id))

    def test_delete_non_existing_author(self):
        self.assertFalse(Author.delete_selected(1))

if __name__ == '__main__':
    db.init(host=os.getenv('DB_HOST', 'localhost'),
            user='unittest',
            password='test_db',
            database='test_db',
            charset='utf8')
    unittest.main()
