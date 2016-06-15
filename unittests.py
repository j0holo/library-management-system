import unittest

from models import *


class TestPublisherModel(unittest.TestCase):

    def setUp(self):
        db.connect()

    def tearDown(self):
        q = Publisher.delete()
        q.execute()
        db.close()

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
        # publisher should be None
        self.assertFalse(publisher)

    def test_add_publisher_city_length(self):
        publisher_name = "British Books"
        city = "a" * 266
        publisher = Publisher.add_publisher(name=publisher_name,
                                            city=city)
        self.assertFalse(publisher)

    def test_select_all_publishers(self):
        Publisher.create(name="The German Writters",
                         city="Berlin")
        publishers = Publisher.select_all()
        self.assertTrue(any(publisher.name == "The German Writters"
                        for publisher in publishers))

    def test_select_all_publishers_no_entries(self):
        publishers = Publisher.select_all()
        self.assertTrue(publishers is None)

if __name__ == '__main__':
    unittest.main()
