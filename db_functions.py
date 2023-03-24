import logging
from .models import Query, Predictions
import datetime
from . import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('earlyBirds.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


def store_query(handle: str):
    """
    store query and timestamp into db
    parameters:
        handle:  a reddit handle
    """
    try:
        new_entry = Query(handle=handle, time=datetime.datetime.utcnow())
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error storing query {handle} in database: {e}")
        db.session.rollback()
        raise ValueError(f"Error storing query {handle} in database: {e}")
    return


def delete_query(handle: str):
    """
    delete query and timestamp from db
    parameters:
        handle:  a reddit handle
    """
    try:
        results = Query.query.filter_by(handle=handle)
        if results:
            for result in results:
                db.session.delete(result)
            db.session.commit()
    except Exception as e:
        logger.error(f"Error deleting query {handle} from database: {e}")
    return


def fetch_results(fk: str):
    """
    retrieves corpus and predictions from db
    parameters:
        fk:  foreign key (unique reddit handle)
    returns:
        zip object consisting of corpus and predictions
    """
    try:
        query = Predictions.query.filter_by(fk=fk)
        if query:
            corpus = []
            predictions = []
            for row in query:
                corpus.append(row.comment)
                predictions.append(row.prediction)
            return zip(corpus, predictions)
    except Exception as e:
        logger.error(f"Error fetching results for {fk} from database: {e}")


def store_prediction(fk: str, predictions: zip):
    """
    stores corpus and predictions into db
    parameters:
        fk:             foreign key (unique reddit handle)
        predictions:    a zipped object consisting of corpus and predictions
    """
    try:
        for comment, prediction in predictions:
            new_entry = Predictions(
                fk=fk, comment=comment, prediction=prediction)
            db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error storing prediction for {fk} in database: {e}")
    return


def delete_predictions(fk: str):
    """
    delete query and timestamp from db
    parameters:
        handle:  a reddit handle
    """
    try:
        records = Predictions.query.filter_by(fk=fk)
        if records:
            for record in records:
                db.session.delete(record)
            db.session.commit()
    except Exception as e:
        logger.error(f"Error deleting query {fk} from database: {e}")
    return


def check_timestamp(query: str):
    """
    check time of last query
    parameters:
        query:  a reddit handle
    returns:
        time of last query
    """
    try:
        query = Query.query.filter_by(handle=query).first()
        if query:
            return query.time
    except Exception as e:
        logger.error(
            f"Error checking presence of query {query} in database: {e}")
    return


logger.removeHandler(file_handler)
