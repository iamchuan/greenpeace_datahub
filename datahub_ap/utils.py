import pandas as pd


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

    def to_dict(self, cols=None):
        if cols is None:
            return self.data.to_dict(orient='records')
        else:
            return self.data[cols].to_dict(orient='records')


if __name__ == '__main__':
    data_path = './data/pm2p5_2013.csv'
    dw = DataWrangler(data_path)
    # for row in dw.to_list():
    #     print(row)
    print(dw.get_month_data(2).to_dict())