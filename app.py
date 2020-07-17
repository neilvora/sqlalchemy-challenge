# Import Flask and sqlalchemy modules
from flask import Flask,jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import desc
import numpy as np
import pandas as pd



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect=True)

## Set DB variables
measurement = Base.classes.measurement
station = Base.classes.station


# Create flask app

app =Flask(__name__)


# Define what to do when a user reaches the index page

@app.route("/")
def home():
    print('Hello')
    return (
        f'Welcome to the Climate App!<br/>'
        f'</br>'
        f'Available Routes: <br/>'
        f'</br>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

# Precipitation API

@app.route('/api/v1.0/precipitation')
def precipitation():
    'Return the JSON of Date and prcp'
    session = Session(engine)

    results = session.query(measurement.date,measurement.prcp).all()

    session.close()

    results_df = pd.DataFrame(results,columns = ['Date','Prcp'])

    results_dict = results_df.set_index('Date').to_dict()


    return jsonify(results_dict)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)

    results = session.query(measurement.station.distinct()).all()

    session.close()

    results_list = list(np.ravel(results))

    return jsonify(results_list)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    results = session.query(measurement.date,measurement.tobs).filter(measurement.station=='USC00519281').\
    filter(measurement.date>='2016-08-23',measurement.date<'2017-08-23').all()



    results_list = list(np.ravel(results))

    return jsonify(results_list)

@app.route('/api/v1.0/<start>/')
def dates(start):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date>= start).all()

    session.close()

    results_list = list(np.ravel(results))

    min_max_avg_list = []
    results_dict = {}
    results_dict['min temp'] = results_list[0]
    results_dict['max temp'] = results_list[1]
    results_dict['avg temp'] = results_list[2]

    min_max_avg_list.append(results_dict)


    return jsonify(min_max_avg_list)

@app.route('/api/v1.0/<start>/<end>')
def date(start,end):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date>= start,measurement.date<=end).all()

    session.close()

    results_list = list(np.ravel(results))

    min_max_avg_list = []
    results_dict = {}
    results_dict['min temp'] = results_list[0]
    results_dict['max temp'] = results_list[1]
    results_dict['avg temp'] = results_list[2]

    min_max_avg_list.append(results_dict)

    return jsonify(min_max_avg_list)


if __name__ =="__main__":
    app.run(debug=True)