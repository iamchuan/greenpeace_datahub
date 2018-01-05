from flask import Flask, render_template, request, redirect
from utils import *
from collections import OrderedDict

app = Flask(__name__)

year_opt = ('2013', '2014')

month_opt = OrderedDict([('January', 1),
                         ('February', 2),
                         ('March', 3),
                         ('April', 4),
                         ('May', 5),
                         ('June', 6),
                         ('July', 7),
                         ('August',8),
                         ('September', 9),
                         ('October', 10),
                         ('November', 11),
                         ('December', 12)])

default_yr = 2013
default_mo = 1

with open('./config.yml', 'r') as f:
    CONFIG = yaml.load(f)

dw = DataWrangler(**CONFIG['mysql'])


@app.route("/", methods=['GET'])
def index():
    return redirect("/map")


@app.route("/map", methods=['GET'])
def china_map():
    # get year/month from WTForm
    yr = request.args.get('year')
    mo = request.args.get('month')
    # get year/month values
    if yr is None:
        year = default_yr
    else:
        year = int(yr)
    if mo is None:
        month = default_mo
    else:
        month = month_opt[mo]
    # retrieve map data
    map_data = dw.get_month_data(year=year, month=month)\
        .add_col('category', value_to_category)\
        .add_col('color', category_to_color)\
        .data
    # render map page
    return render_template('index.html',
                           map_data=map_data,
                           yr_selected=yr,
                           mo_selected=mo,
                           years=year_opt,
                           months=month_opt)


if __name__ == "__main__":
    app.run(debug=True)