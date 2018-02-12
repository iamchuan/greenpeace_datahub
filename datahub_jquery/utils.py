import pymysql.cursors
import yaml
from pymysql.err import OperationalError, InterfaceError


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

    reader = None
    config = None
    data = []

    def __init__(self, **kwargs):
        self.config = kwargs
        try:
            self.reader = MySQLReader(**self.config)
        except pymysql.err.InternalError:
            pass

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

    def by_pollutant(self, p_names, p_levels=None, p_colors=None):
        month_data_by_pollutant = dict()
        for p in p_names:
            p_data = list()
            for row in self.data:
                if p in row:
                    item = {k:v for k, v in row.items() if k in ('lat', 'lng', 'area')}
                    item['val'] = row.get(p)
                    if p_levels is not None and p_colors is not None:
                        idx = len(list(filter(lambda x: x <= item['val'], p_levels[p_names[p]])))
                        item['col'] = p_colors[idx]
                    p_data.append(item)
            if p_data:
                month_data_by_pollutant[p_names[p]] = p_data
        return month_data_by_pollutant


def level_to_range(level):
    lower = [0] + [v+1 for v in level[:-1]]
    upper = level
    range = ['{}-{}'.format(l,u) for l, u in zip(lower, upper)]
    range.append('>{}'.format(upper[-1]))
    return range


if __name__ == '__main__':
    # with open('./category.yml', 'r') as f:
    #     CATEGORY = yaml.load(f)
    #
    with open('./config.yml', 'r') as f:
        CONFIG = yaml.load(f)

    reader = MySQLReader(**CONFIG['mysql'])
    print(reader.fetch_data('SELECT * FROM map_air_pollution_2013 WHERE month=1 and pm2_5_24h=20'))
    # dw = DataWrangler(**CONFIG['mysql'])
    # data = dw.get_month_data('2014', '2').by_pollutant(p_names=CATEGORY['pollutant_names'],
    #                                                    p_levels=CATEGORY['pollutant_levels'],
    #                                                    p_colors=CATEGORY['level_colors'])
    # print(data['AQI'])
