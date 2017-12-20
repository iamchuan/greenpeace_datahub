import pandas as pd

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

class DataWrangler(object):

    def __init__(self, path=None, data=None):
        if path is None:
            if data is None:
                raise ValueError('Cannot import data')
            else:
                self.data = data
        else:
            self.data = pd.read_csv(path)

    def get_month_data(self, month):
        return DataWrangler(data=self.data.loc[self.data['month'] == month])

    def to_list(self, cols=None, header=False):
        if cols is None:
            cols = list(self.data)
        if header:
            yield cols
        for _, row in self.data.iterrows():
            yield [row[col] for col in cols]

    def add_col(self, col_name, func):
        self.data[col_name] = self.data.apply(func=func, axis=1)
        return self

    def to_dict(self, cols=None):
        if cols is None:
            return self.data.to_dict(orient='records')
        else:
            return self.data[cols].to_dict(orient='records')

def value_to_category(row):
    for val, level in sorted(category_map.items()):
        if row['pm25'] <= val:
            return level

def category_to_color(row):
    return color_map[row['category']]

if __name__ == '__main__':
    data_path = './data/pm2p5_2013.csv'
    dw = DataWrangler(data_path)
    # for row in dw.to_list():
    #     print(row)
    print(dw.get_month_data(2)\
          .add_col('category', value_to_category)\
          .add_col('color', category_to_color)\
          .to_dict())