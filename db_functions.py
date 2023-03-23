import logging
from .models import Query, Predictions
import datetime
from . import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler that writes log messages to a file
file_handler = logging.FileHandler('earlyBirds.log')
file_handler.setLevel(logging.INFO)

# Add the file handler to the logger
logger.addHandler(file_handler)


def store_query(handle: str):
    """
    store query and timestamp into db
    parameters: query:      a reddit handle
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
    try:
        query = Query.query.filter_by(query=handle).first()
        if query:
            db.session.delete(query)
            db.session.commit()
    except Exception as e:
        logger.error(f"Error deleting query {handle} from database: {e}")
        db.session.rollback()
        raise ValueError(f"Error deleting query {handle} from database: {e}")
    return


def fetch_results(fk: str):
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
        db.session.rollback()
        raise ValueError(f"Error fetching results for {fk} from database: {e}")


def store_prediction(fk, predictions: zip):
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
        db.session.rollback()
        raise ValueError(f"Error storing prediction for {fk} in database: {e}")
    return


def check_presence(query: str):
    try:
        query = Query.query.filter_by(query=query).first()
        if query:
            return query.time()
    except Exception as e:
        logger.error(
            f"Error checking presence of query {query} in database: {e}")
        db.session.rollback()
        raise ValueError(
            f"Error checking presence of query {query} in database: {e}")
    return


# Remove the file handler from the logger
logger.removeHandler(file_handler)
