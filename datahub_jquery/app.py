from flask import Flask, jsonify, render_template, request, redirect
from utils import DataWrangler, level_to_range
import yaml


app = Flask(__name__)

with open('./category.yml', 'r') as f:
    CATEGORY = yaml.load(f)

with open('./config.yml', 'r') as f:
    CONFIG = yaml.load(f)

dw = DataWrangler(**CONFIG['mysql'])


@app.route('/', methods=['GET'])
def index():
    return redirect('/map')


@app.route('/map')
def map():
    names = list(CATEGORY['pollutant_names'].values())
    ranges = {p:level_to_range(CATEGORY['pollutant_levels'][p]) for p in names}
    rows = [{'col':CATEGORY['level_colors'][i],'val':[ranges[p][i] for p in names]} for i in range(6)]
    p_level = {
        'p_name': names,
        'rows': rows
    }
    return render_template('map.html', p_level=p_level)


@app.route('/explore')
def explore():
    return render_template('temp.html')


@app.route('/analysis')
def analysis():
    return render_template('temp.html')


@app.route('/about')
def about():
    return render_template('temp.html')


@app.route('/pollutants')
def get_pollutants():
    year = request.args.get('year', 2014, type=str)
    month = request.args.get('month', 1, type=str)
    data = dw.get_month_data(year=year, month=month)\
        .by_pollutant(p_names=CATEGORY['pollutant_names'],
                      p_levels=CATEGORY['pollutant_levels'],
                      p_colors=CATEGORY['level_colors'])
    return jsonify(**data)


if __name__ == '__main__':
    app.run(debug=True)