from flask import Flask, render_template, request
from utils import *

app = Flask(__name__)

data_path = './data/pm2p5_2013.csv'
dw = DataWrangler(data_path)
month_opt = {'January':1, 'February':2, 'March':3, 'April':4,
             'May':5, 'June':6, 'July':7, 'August':8, 'September':9,
             'October':10, 'November':11, 'December':12}

default_mo = 1


@app.route("/", methods=['GET'])
def china_map():
    map_data = dw.get_month_data(month=default_mo)\
        .add_col('category', value_to_category)\
        .add_col('color', category_to_color)\
        .to_dict(cols=['city', 'lat', 'lng', 'pm25', 'category', 'color'])
    print(map_data)
    return render_template('index.html', map_data=map_data, months=month_opt)


@app.route("/<string:month>", methods=['GET'])
def china_map_mon(month):
    map_data = dw.get_month_data(month=month_opt[month])\
        .add_col('category', value_to_category)\
        .add_col('color', category_to_color)\
        .to_dict(cols=['city', 'lat', 'lng', 'pm25', 'category', 'color'])
    return render_template('index.html', map_data=map_data, months=month_opt, selected=month)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)

