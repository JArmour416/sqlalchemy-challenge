import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
        f"Dates and temperature from the last year. <br/>"
        f"/api/v1.0/stations<br/>"
        f"List of stations. <br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of Temperature Observations for the previous year. <br/>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Average, Max, and Min temperatures for a given start date. <br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Average, Max, and Min temperatures for a given date range. <br/>"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Dates and temperature from the last year"""
    # Query Dates and temperature from the last year
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()

    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all stations
    results = session.query(Station.name, Station.station, Station.elevation).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stations_list = []
    for name, station, elevation in results:
        station_dict = {}
        station_dict["name"] = name
        station_dict["station"] = station
        station_dict["elevation"] = elevation
        stations_list.append(station_dict)

         # creates JSONified list of dictionaries

    return jsonify(station_list)
        
@app.route("/api/v1.0/tobs")
def temp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Temperature Observations for the previous year"""
    # Query Temperature Observations
    results = session.query(Station.name, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()

    session.close()

    # creates JSONified list of dictionaries
    tobs_list = []
    for name, date, tobs in results:
        measure_dict = {}
        measure_dict["Date"] = date
        measure_dict["Station"] = station
        measure_dict["Temperature"] = tobs
        tobs_list.append(row)

    return jsonify(tobs_list)

@app.route('/api/v1.0/<date>/')
def given_date(date):

    """Return the average temp, max temp, and min temp for the date"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    session.close()
    
    # creates JSONified list of dictionaries
    date_list = []
    for result in results:
        date_dict = {}
        date_dict['Start Date'] = date
        date_dict['End Date'] = '2017-08-23'
        date_dict['Average Temperature'] = float(result[0])
        date_dict['Highest Temperature'] = float(result[1])
        date_dict['Lowest Temperature'] = float(result[2])
        date_list.append(date_dict)

    return jsonify(date_list)

@app.route('/api/v1.0/<start_date>/<end_date>/')

def period(start_date, end_date):

    """Return the avg, max, min, temp over a specific time period"""
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
        session.close()
  
    # creates JSONified list of dictionaries
    date_list = []
    for result in results:
        dates_dict = {}
        dates_dict["Start Date"] = start_date
        dates_dict["End Date"] = end_date
        dates_dict["Average Temperature"] = float(result[0])
        dates_dict["Highest Temperature"] = float(result[1])
        dates_dict["Lowest Temperature"] = float(result[2])
        date_list.append(dates_dict)

    return jsonify(date_list)


if __name__ == '__main__':
    app.run(debug=True)
