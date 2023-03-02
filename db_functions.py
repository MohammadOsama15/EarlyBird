from .models import User, Query, Predictions
import datetime
from flask import Blueprint
from . import db


def store_query(handle:str):
    """
    store query and timestamp into db
    parameters: query:      a reddit handle
    """
    new_entry = Query(handle=handle, time=datetime.datetime.utcnow())
    db.session.add(new_entry)
    db.session.commit()
    return


def delete_query(handle:str):
    query = Query.query.filter_by(query=query).first()
    if query: 
        db.session.delete(query)
        db.session.commit()
    return


def fetch_results(fk:str):
    query = Predictions.query.filter_by(fk=fk)
    if query:
        corpus = []
        predictions = []
        for row in query:
            corpus.append(row.comment)
            predictions.append(row.prediction)
        return zip(corpus, predictions)


def store_prediction(fk, predictions:zip):
    """
    stores results into table, each text corpus (comment or post) is paired with a prediction
    parameters: 
        fk:             foreign key (unique reddit handle) stored in a different database
        predictions:    a zipped object consisting of corpus and predictions
    """
    for comment, prediction in predictions:
        new_entry = Predictions(fk = fk, comment=comment, prediction = prediction)
        db.session.add(new_entry)
    db.session.commit()
    return


def check_presence(query:str):
    query = Query.query.filter_by(query=query).first()
    if query:
        return query.time()
    return