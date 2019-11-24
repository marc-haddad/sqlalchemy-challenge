import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    all_date_prcp = []
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        all_date_prcp.append(date_prcp_dict)
    return jsonify(all_date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    yr_date_prcp = []
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").all()
    session.close()
    for date, prcp in results:
        date_prcp_dict = {}
        date_prcp_dict["date"] = date
        date_prcp_dict["prcp"] = prcp
        yr_date_prcp.append(date_prcp_dict)
    return jsonify(yr_date_prcp)

@app.route("/api/v1.0/<start>")
def vacay_st(start):
    session = Session(engine)
    start_date_prcp = []

    try:
        dt.datetime.strptime(start, "%Y-%m-%d").date()
        results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= start).all()
        session.close()
        for date, prcp in results:
            date_prcp_dict = {}
            date_prcp_dict["date"] = date
            date_prcp_dict["prcp"] = prcp
            start_date_prcp.append(date_prcp_dict)
        return jsonify(start_date_prcp)
    except:
        session.close()
        return jsonify({"error": "Date format must be: 'yyyy-mm-dd'"})

@app.route("/api/v1.0/<start>/<end>")
def vacay_st_end(start, end):
    session = Session(engine)
    start_end_date_prcp = []

    try:
        dt.datetime.strptime(start, "%Y-%m-%d").date()
        dt.datetime.strptime(end, "%Y-%m-%d").date()
        if(dt.datetime.strptime(start, "%Y-%m-%d").date() > dt.datetime.strptime(end, "%Y-%m-%d").date()):
            raise ValueError()
        results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        session.close()
        for date, prcp in results:
            date_prcp_dict = {}
            date_prcp_dict["date"] = date
            date_prcp_dict["prcp"] = prcp
            start_end_date_prcp.append(date_prcp_dict)
        return jsonify(start_end_date_prcp)
    except:
        session.close()    
        return jsonify({"Error": "Start/End format must be: 'yyyy-mm-dd/yyyy-mm-dd'"})

if __name__ == "__main__":
    app.run(debug=True)