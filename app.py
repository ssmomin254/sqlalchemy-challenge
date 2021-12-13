import numpy as numpy
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")

def greeting():
    return(
        f'Avaliable options:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/&lt;start&gt;<br/>'
        f'/api/v1.0/&lt;start&gt;/&lt;end&gt;'
    )

@app.route('/api/v1.0/precipitation')

def precipitation():
    session = Session(engine)
    precip = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    dates = []

    for date, prcp in precip:
        precip_dict = {}
        precip_dict[date] = prcp
        dates.append(precip_dict)
    
    session.close()

    return jsonify(dates)

@app.route('/api/v1.0/stations<br/>')
def stations():
    session = Session(engine)
    stn = session.query(Station.station, Station.name).all()

    stn_dict = {}

    for station,name in stn:
        stn_dict[station] = name
    
    session.close

    return jsonify(stations)

@app.route('/api/v1.0/tobs<br/>')
def tobs():
    session=Session(engine)
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    last_date = last_date.date()
    year_ago = last_date - dt.timedelta(days=365)

    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).order_by(Measurement.date).all()

    temp_list = []

    for date, tobs in temps:
        temp_dict = {}
        temp_dict[date] = tobs
        temp_list.append(temp_dict)
    
    session.close

    return jsonify(temp_list)

@app.route('/api/v1.0/&lt;start&gt;<br/>')
def start_range(start):
    session = Session(engine)

    temp_list = []

    temps = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).order_by(Measurement.date).all()

    for date, min, max, avg in temps:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = avg
        temp_list.append(temp_dict)
    
    session.close()

    return jsonify(temp_list)

@app.route('/api/v1.0/&lt;start&gt;/&lt;end&gt;')
def start_end_range(start, end):
    session = Session(engine)

    temp_list = []

    temps = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start and Measurement.date <= end).order_by(Measurement.date).all()

    for date, min, max, avg in temps:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = avg
        temp_list.append(temp_dict)
    
    session.close()

    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)
