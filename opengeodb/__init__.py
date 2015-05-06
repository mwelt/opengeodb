from collections import namedtuple
import pymysql as db

__author__ = 'mwelt'

OpengeoDbLoc = namedtuple("OpengeoDbLoc", "plz, name, dist")

OpengeoDbConnection = namedtuple("OpengeoDbConnection",
                                 "host, user passwd, db")


class OpengeoDb:
    def __init__(self, connection):
        self._connection = connection

    def get_con(self):
        """
         :return:
        """
        return db.connect(host=self._connection.host,
                          user=self._connection.user,
                          passwd=self._connection.passwd,
                          db=self._connection.db)

    def find_locations_by_zip(self, zipcode):
        """
        :param zipcode: string
        :return: list [OpengeoDbLoc]
        """
        with self.get_con() as cur:
            cur.execute("""
            select zc_zip, zc_location_name
            from zip_coordinates where zc_zip = %s""", (zipcode, ))

        return [OpengeoDbLoc(plz=r[0], name=r[1], dist=0)
                for r in cur.fetchall()]

    def find_locations_by_name(self, name):
        """
        :param name: string
        :return: list [OpengeoDbLoc]
        """
        with self.get_con() as cur:
            cur.execute("""
            select zc_zip, zc_location_name
            from zip_coordinates where zc_location_name like %s""",
                        ('%' + name + '%', ))

            return [OpengeoDbLoc(plz=r[0], name=r[1], dist=0)
                    for r in cur.fetchall()]

    def find_locations_nearby_zip(self, zipcode, distance):
        """
        :param zipcode: string
        :param distance: string
        :return: list [OpengeoDbLoc]
        """
        with self.get_con() as cur:
            cur.execute("""
                select zc_id, zc_location_name from zip_coordinates
                where zc_zip = %s""", (zipcode, ))

            if cur.rowcount == 0:
                return

            zc_id = cur.fetchone()[0]
            cur.execute("""SELECT
                    dest.zc_zip,
                    dest.zc_location_name,
                    ACOS(
                         SIN(RADIANS(src.zc_lat)) * SIN(RADIANS(dest.zc_lat))
                         + COS(RADIANS(src.zc_lat)) * COS(RADIANS(dest.zc_lat))
                         * COS(RADIANS(src.zc_lon) - RADIANS(dest.zc_lon))
                    ) * 6380 AS distance
                    FROM zip_coordinates dest
                    CROSS JOIN zip_coordinates src
                    WHERE src.zc_id = %s
                    AND dest.zc_id <> src.zc_id
                    HAVING distance < %s
                    ORDER BY distance;""", (zc_id, distance))

            return [OpengeoDbLoc(plz=r[0], name=r[1], dist=r[2])
                    for r in cur.fetchall()]
