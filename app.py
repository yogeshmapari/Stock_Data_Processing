from flask import Flask, render_template, jsonify, request
import mysql.connector
import plotly.graph_objs as go
import configparser

app = Flask(__name__)

# Configuration file path
CONFIG_PATH = 'config.ini'


def get_database_connection():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Get the MySQL database configuration
    db_config = {
        'host': config['mysql']['host'],
        'user': config['mysql']['user'],
        'password': config['mysql']['password'],
        'database': config['mysql']['database']
    }

    # Establish a connection to the MySQL database
    connection = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database='int_layer'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/1')
def index1():
    return render_template('index1.html')
@app.route('/2')
def index2():
    return render_template('index2.html')
@app.route('/3')
def index3():
    return render_template('index3.html')
@app.route('/4')
def index4():
    return render_template('index4.html')
@app.route('/stocks')
def get_stocks():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "show tables"
    cursor.execute(query)
    tables = cursor.fetchall()
    cursor.close()
    connection.close()
    stock_list = [table[0] for table in tables]
    return jsonify(stock_list)

@app.route('/data/<stock>')
def get_stock_data(stock):
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT Date, Open, High, Low, Close, Volume , Daily_Return,   MA_5_Day, MA_10_Day, Volatility, RSI, MACD, Signal_9, Upper_Band, Lower_Band, Gain, Loss, AvgGain, AvgLoss, EMA_12, EMA_26, MA_20, SD_20 FROM {stock}"
    print(query)
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
