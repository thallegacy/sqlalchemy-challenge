import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask Setup
#################################################
app = Flask(__name__)


# Flask Routes
#################################################

@app.route("/")
def home():
    #List all available api routes
    return (
        f"Climate App<br/><br/>"
        f"Here is a list of all available routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/><br/>"
        f"For the routes above with start or end dates please use the (yyyy-mm-dd) format"
        
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Last 12 months of precipitation data and plot the results

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query Data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").\
                                                                    filter(Measurement.date <= "2017-08-23").all()

    #Close session
    session.close()

    # Create empty list
    all_prcp = []
    
    #Create loop to read in values
    for date,prcp  in results:
        # Create empty dictionary
        prcp_dict = {}
        # Add dictionary values
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        # Add dictionaries to list       
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    #List of stations

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query Data
    results = session.query(Station.station, Station.name).all()

    #Close session
    session.close()

    # Create empty list
    all_stations = []
    
    #Create loop to read in values
    for station,name  in results:
        # Create empty dictionary
        station_dict = {}
        # Add dictionary values
        station_dict["station"] = station
        station_dict["name"] = name
        # Add dictionaries to list       
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Dates and temperature observations of the most active station for the last year of data.

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query Data
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').\
                                                                    filter(Measurement.date >= "2016-08-23").\
                                                                    filter(Measurement.date <= "2017-08-23").all()

    #Close session
    session.close()

    # Create empty list
    all_tobs = []
    
    #Create loop to read in values
    for date,tobs  in results:
        # Create empty dictionary
        tobs_dict = {}
        # Add dictionary values
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        # Add dictionaries to list       
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Query Data
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                                                                            filter(Measurement.date >= start).all()

    #Close session
    session.close()

    # Create empty list
    all_start_dates = []
    
    #Create loop to read in values
    for tmin, tavg, tmax  in results:
        # Create empty dictionary
        starttobs_dict = {}
        # Add dictionary values
        starttobs_dict["TMIN"] = tmin
        starttobs_dict["TAVG"] = tavg
        starttobs_dict["TMAX"] = tmax
        # Add dictionaries to list       
        all_start_dates.append(starttobs_dict)
        
    return jsonify(all_start_dates)

if __name__ == "__main__":
    app.run(debug=True)
