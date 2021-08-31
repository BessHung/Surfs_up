# import dependencies

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.sql.expression import select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database
Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# Set Up Flask
app = Flask(__name__)

# Create Flask Routes
@app.route('/') #'/' means the root of our routes.
def Welcome():
    return(
    
    f"Welcome to the Climate Analysis API!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/temp/start/end")

@app.route('/api/v1.0/precipitation')
def precipitation():

    session = Session(engine)

    prev_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date:prcp for date, prcp in precipitation}
    
    session.close()

    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():

    session = Session(engine)

    results = session.query(Station.station).all()
    stations = list(np.ravel(results))

    session.close()

    return jsonify(stations=stations)

@app.route('/api/v1.0/tobs')
def temp_monthly():

    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.station =='USC00519281').all()
    temps = list(np.ravel(results))

    session.close()

    return jsonify(temps = temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    session = Session(engine)

    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))        
        return jsonify(temps = temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    
    session.close()
    
    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)