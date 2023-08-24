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

    # Return the JSON representation of your dictionary.

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
    # for date, prcp in precipitation_df:
    #     precipitation_dict = {}
    #     precipitation_dict["Date"] = date
    #     precipitation_dict["Precipitation"] = prcp
    #     prcp_list.append(precipitation_dict)

    for index, row in precipitation_df.iterrows():
        precipitation_dict = {}
        precipitation_dict["Date"] = row["Date"]
        precipitation_dict["Precipitation"] = row["Precipitation"]
        prcp_list.append(precipitation_dict)

    return jsonify(prcp_list)



if __name__ == '__main__':
    app.run(debug=True)