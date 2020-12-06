import numpy as np
import os.path
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd
import json
from flask import Flask, jsonify

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#db_path = BASE_DIR +  "\Resources\hawaii.sqlite"
#engine = create_engine(f"sqlite:///{db_path}")
engine = create_engine(f"sqlite:///Resources/hawaii.sqlite")
print(engine)

app = Flask(__name__)

@app.route("/")
def home(): 
    return (
        f"Available Routes:<br/>" 
    )  
@app.route('/api/v1.0/precipitation')
def precipitation(): 
    results = pd.read_sql('SELECT date, prcp FROM Measurement', engine) 
    results_json = results.to_dict(orient='records')
    return  jsonify(results_json)

@app.route('/api/v1.0/stations')
def stations(): 
    results = pd.read_sql('SELECT station, name FROM Station', engine) 
    results_json = results.to_dict(orient='records')
    return  jsonify(results_json)

@app.route('/api/v1.0/tobs')
def tobs(): 
    sql = """
        SELECT date, tobs FROM Measurement 
        WHERE date > 
        (
            SELECT  DATE(MAX(date), '-1 year') FROM Measurement 
        )   
        ORDER BY DATE DESC """
    results = pd.read_sql(sql, engine) 
    results_json = results.to_dict(orient='records')
    return  jsonify(results_json)

@app.route('/api/v1.0/test')
def td(): 
    sql = """
        SELECT date, tobs FROM Measurement 
        WHERE strftime('%m',date) = '06' """

    results = pd.read_sql(sql, engine) 
    results_json = results.to_dict(orient='records')
    return  jsonify(results_json)


@app.route('/api/v1.0/<start>/<end>')
def tdates(start, end):  
    sql = f"""
        SELECT MIN(tobs) TMIN, AVG(tobs) TAVG, MAX(tobs) TMAX   FROM Measurement 
        WHERE date >= '{start}' AND date <= '{end}'  """ 
    print(sql)
    results = pd.read_sql(sql, engine) 
    results_json = results.to_dict(orient='records')
    return  jsonify(results_json)

if __name__ == '__main__':
    app.run(debug=True)
