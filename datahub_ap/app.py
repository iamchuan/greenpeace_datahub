from flask import Flask, render_template
from utils import DataWrangler

app = Flask(__name__)

data_path = './data/pm2p5_2013.csv'
dw = DataWrangler(data_path)
month = 2


@app.route("/")
def hello():
    map_data = dw.get_month_data(month=month).to_dict(cols=['city', 'lat', 'lng', 'pm25'])
    return render_template('index.html', map_data=map_data)


if __name__ == "__main__":

    app.run(host='0.0.0.0', debug=False)

