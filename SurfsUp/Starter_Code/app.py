# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Welcome to the homepage!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0//temp/start <br/>"
        f"/api/v1.0//temp/start/end <br/>"
        f"start_date (string): A date string in the format %Y-%m-%d <br/> end_date (string): A date string in the format %Y-%m-%d"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    latest_year = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    session.close()

    all_precipitation = []
    for date, prcp in latest_year:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station,Station.name)
    session.close()
    
    all_stations = []
    for station, name in stations:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name    
        all_stations.append(station_dict)
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    latest_year_tobs  = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= '2016-08-23').all()
    session.close()

    all_tobs = []
    for date, tobs in latest_year_tobs:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/temp/<start>")
def start(start):
    session = Session(engine)

    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    t_stats = list(np.ravel(temp_stats))
    return jsonify(t_stats)

@app.route("/api/v1.0/temp/<start>/<end>")
def get_start_end(start, end):
    session = Session(engine)
    temp_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), \
            func.max(Measurement.tobs)).filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    session.close()
    t_stats = list(np.ravel(temp_stats))
    return jsonify(t_stats)

   

if __name__ == '__main__':
    app.run(debug=True)
