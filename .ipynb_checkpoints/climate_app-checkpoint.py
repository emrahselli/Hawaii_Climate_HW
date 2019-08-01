# Dependencies
from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

#Flask Routes
@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis:<br/>"
        f"/api/v1.0/precipitation returns last year precipitations from all stations<br/>"
        f"/api/v1.0/stations returns list of stations<br/>"
        f"/api/v1.0/tobs returns last year temperatures from all stations<br/>"
        f"/api/v1.0/start when date is given in the format of YYYY-MM-DD, returns MIN/AVG/MAX temperature for the days from start date to a set end date<br/>"
        f"/api/v1.0/start/end when dates are given in the format of YYYY-MM-DD, returns MIN/AVG/MAX temperature for the days in between<br/>")

# Precipitation API
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    precip = {date: prcp for date, prcp in prcp_query}

    return jsonify(precip)

# Stations API
@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(Station.station, Station.name).all()

    station = list(np.ravel(station_query))

    return jsonify(station)

# Temperature Observations API
@app.route("/api/v1.0/tobs")
def temp_obs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_ago).all()

    tobs = list(np.ravel(tobs_query))

    return jsonify(tobs)

# Start date API
@app.route("/api/v1.0/<start>")
def trip1(start): 
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    start = start_date - one_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

# Start/End date API
@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    one_year = dt.timedelta(days=365)
    start = start_date - one_year
    end = end_date - one_year
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


if __name__ == "__main__":
    app.run(debug=True)