import logging
from .models import Timestamp, Predictions
import datetime
from . import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('earlyBirds.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


def get_timestamp(search_term: str):
    """
    check when search term was last stored in db
    parameters:
        search_term:    search term
    returns:
        time of last query
    """

    res = Timestamp.query.filter_by(search_term=search_term).first()
    try:
        if res:
            return res.time
    except Exception as e:
        logger.error(
            f"Timestamp for {search_term} not found: {e}")
    return


def store_timestamp(search_term: str):
    """
    store search term and timestamp into db
    parameters:
        search_term:  search term
    """
    try:
        stmt = Timestamp(search_term=search_term,
                         time=datetime.datetime.utcnow())
        db.session.add(stmt)
        db.session.commit()
        db.session.close()
    except Exception as e:
        logger.error(
            f"Error storing timestamp for {search_term} in database: {e}")
        raise ValueError(
            f"Error storing timestamp for {search_term} in database: {e}")
    return


def delete_timestamp(search_term: str):
    """
    delete search term and timestamp from db
    parameters:
        search_term: search term
    """
    res = Timestamp.query.filter_by(search_term=search_term)
    try:
        if res:
            for row in res:
                db.session.delete(row)
            db.session.commit()
            db.session.close()
    except Exception as e:
        logger.error(
            f"There are no timestamps for {search_term} to delete: {e}")
    return


def get_predictions(fk: str):
    """
    retrieves corpus and predictions from db
    parameters:
        fk:  search term
    returns:
        zip object consisting of corpus and predictions
    """
    res = Predictions.query.filter_by(fk=fk)
    try:
        if res:
            corpus = []
            predictions = []
            for row in res:
                corpus.append(row.comment)
                predictions.append(row.prediction)
            return zip(corpus, predictions)
    except Exception as e:
        logger.error(f"Predictions for {fk} not found: {e}")


def store_prediction(fk: str, predictions: zip):
    """
    stores corpus and predictions into db
    parameters:
        fk: foreign key (search term)
        predictions:    a zipped object consisting of corpus and predictions
    """
    try:
        for comment, prediction in predictions:
            stmt = Predictions(
                fk=fk, comment=comment, prediction=prediction)
            db.session.add(stmt)
        db.session.commit()
        db.session.close()
    except Exception as e:
        logger.error(f"Error storing prediction for {fk} in database: {e}")
        raise ValueError({e})
    return


def delete_predictions(fk: str):
    """
    delete query and timestamp from db
    parameters:
        fk: foreign key (search term)
    """
    try:
        res = Predictions.query.filter_by(fk=fk)
        if res:
            for row in res:
                db.session.delete(row)
            db.session.commit()
            db.session.close()
    except Exception as e:
        logger.error(f"There are no predictions for {fk} to delete: {e}")
    return


logger.removeHandler(file_handler)
