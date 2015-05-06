from unittest import TestCase
import opengeodb

__author__ = 'mwelt'


class TestOpengeoDb(TestCase):
    connection = opengeodb.OpengeoDbConnection(
        host='localhost', user='opengeodb',
        passwd='opengeodb', db='opengeodb')

    def test_find_locations_by_zip(self):
        odb = opengeodb.OpengeoDb(TestOpengeoDb.connection)
        locs = odb.find_locations_by_zip("04205")
        self.assertEqual(len(locs), 1)

    def test_find_locations_by_name(self):
        odb = opengeodb.OpengeoDb(TestOpengeoDb.connection)
        locs = odb.find_locations_by_name("Leipzig")
        self.assertEqual(len(locs), 37)

    def test_find_locations_nearby_zip(self):
        odb = opengeodb.OpengeoDb(TestOpengeoDb.connection)
        locs = odb.find_locations_nearby_zip("73614", 10)
        self.assertEqual(len(locs), 16)
