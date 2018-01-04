import pymysql.cursors
import yaml
from pymysql.err import OperationalError, InterfaceError


category_map = {50:'Excellent',
                100:'Good',
                150:'Lightly Polluted',
                200:'Moderately Polluted',
                250:'Heavily Polluted',
                float('inf'):'Severely Polluted'}

color_map = {'Excellent':'#0b40e7',
             'Good':'#11c300',
             'Lightly Polluted':'#ffe132',
             'Moderately Polluted':'#ff9936',
             'Heavily Polluted':'#ff1313',
             'Severely Polluted':'darkred'}


class MySQLReader(object):

    __CONFIG = None

    def __init__(self, **kwargs):
        self.__CONFIG = kwargs
        self.__connect()

    def __connect(self):
        self.conn = pymysql.connect(charset="utf8mb4",
                                    cursorclass=pymysql.cursors.DictCursor,
                                    **self.__CONFIG)

    def fetch_data(self, query):
        while True:
            try:
                with self.conn.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
            except (OperationalError, InterfaceError):
                self.__connect()

    def close(self):
        self.conn.close()


class DataWrangler(object):

    data = []

    def __init__(self, **kwargs):
        self.reader = MySQLReader(**kwargs)

    def get_month_data(self, year, month):
        table = self.reader.fetch_data("""
        SELECT ap.*, round(ll.latitude, 5) lat, round(ll.longitude, 5) lng FROM (
            SELECT *
            FROM map_air_pollution_{}
            WHERE month = {}
        ) ap INNER JOIN area_latlng ll
        ON ap.area = ll.area
        """.format(year, month))
        self.data = table
        return self

    def add_col(self, col_name, func):
        for row in self.data:
            row[col_name] = func(row)
        return self

    def to_list(self, cols=None, header=False):
        if header:
            yield cols
        for _, row in self.data:
            yield [row[col] for col in cols]


def value_to_category(row):
    for val, level in sorted(category_map.items()):
        if row['pm2_5'] <= val:
            return level


def category_to_color(row):
    return color_map[row['category']]


if __name__ == '__main__':

    with open('./config.yml', 'r') as f:
        CONFIG = yaml.load(f)
    dw = DataWrangler(**CONFIG['mysql'])
    print(dw.get_month_data(2013, 1)
          .add_col('category', value_to_category)
          .add_col('color', category_to_color)
          .data)

