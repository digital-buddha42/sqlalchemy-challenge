# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# Homework-Github/sqlalchemy-challenge/Resources/hawaii.sqlite

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/<start>/<end><br/>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the query results from your precipitation analysis
    #  (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Convert to datetime object
    most_recent_date = pd.to_datetime(most_recent_date[0])

    # See the date 12 months ago
    twelve_months = most_recent_date - dt.timedelta(days=365)

    # Convert to correct format
    twelve_months = twelve_months.strftime("%Y-%m-%d")

    # Perform a query to retrieve the date and precipitation scores
    twelve_months_precipitation = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= twelve_months).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    precipitation_df = pd.DataFrame(twelve_months_precipitation, columns=['Date', 'Precipitation'])

    # Sort the dataframe by date
    precipitation_df = precipitation_df.sort_values(by='Date')
    
    session.close()
    
    prcp_list = []

    for index, row in precipitation_df.iterrows():
        precipitation_dict = {}
        precipitation_dict["Date"] = row["Date"]
        precipitation_dict["Precipitation"] = row["Precipitation"]
        prcp_list.append(precipitation_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).all()
    
    session.close()
    
    all_stations = [list(r)[0] for r in results]

    # Convert list of tuples into normal list - flattens results
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station 
    # for the previous year of data

    most_recent_date_active = session.query(Measurement.date).filter(Measurement.station == 'USC00519281').order_by(Measurement.date.desc()).first()

    # Convert to datetime object
    most_recent_date_active = pd.to_datetime(most_recent_date_active[0])

    # See the date 12 months ago
    twelve_months_date_active_station = most_recent_date_active - dt.timedelta(days=365)

    # Perform a query to retrieve the date and precipitation scores
    twelve_months_temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= twelve_months_date_active_station.strftime("%Y-%m-%d")).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    temperature_df = pd.DataFrame(twelve_months_temp, columns=['Date', 'tobs'])
    
    session.close()
    
    temp_list = []

    for index, row in temperature_df.iterrows():
        temperature_dict = {}
        temperature_dict["Date"] = row["Date"]
        temperature_dict["tobs"] = row["tobs"]
        temp_list.append(temperature_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(temp_list)


if __name__ == '__main__':
    app.run(debug=True)