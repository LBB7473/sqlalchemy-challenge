import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

base = automap_base()
base.prepare(engine, reflect=True)

measurement = base.classes.measurement
station = base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).\
    all()
    session.close
    precip = []
    for dates, rains in results:
        date_dict = {}
        date_dict[dates] = rains
        precip.append(date_dict)

    return jsonify(precip)

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)
    results = session.query(station.name).all()
    session.close
    station_name = list(np.ravel(results))
    return jsonify(station_name)

@app.route("/api/v1.0/tobs")
def active():
    session = Session(engine)
    date = dt.datetime(2016, 8, 23)

    results = session.query(measurement.tobs).\
    filter(station.station == measurement.station).\
    filter(station.station == "USC00519281").\
    filter(measurement.date > date).\
    all()
    session.close
    tobs = list(np.ravel(results))
    return jsonify(tobs)

@app.route("/api/v1.0/<start>")
def input(start):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date > start).\
    all()
    session.close
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def inputboth(start, end):
    session = Session(engine)
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.date > start).\
    filter(measurement.date < end).\
    all()
    session.close
    summary = []
    for tmin, tmax, tavg in results:
        tobs_dict = {}
        tobs_dict["Minimum Temperature"] = tmin
        tobs_dict["Maximum Temperature"] = tmax
        tobs_dict["Average Temperature"] = tavg
        summary.append(tobs_dict)

    return jsonify(summary)





if __name__ == '__main__':
    app.run(debug=True)
