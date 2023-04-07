import logging
import datetime
import json
from .models import User, Profile, Timestamp, Title, Comment
from . import db

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)


def get_timestamp(search_term: str):
    """
    check when search term was last stored in db
    parameters:
        search_term:    search term
    returns:
        time of last query, id associated with query
    """

    res = Timestamp.query.filter_by(search_term=search_term)
    try:
        if res:
            return [res.first().time, res.first().id]
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


def get_titles(fk: int):
    """
    retrieves titles and predictions from db
    parameters:
        fk:  primary key stored in Timestamp table
    returns:
        list of dictionaries consisting of title, prediction, permalink, and id
    """
    res = Title.query.filter_by(timestamp_id=fk)
    try:
        if res:
            corpus = []
            predictions = []
            permalinks = []
            id = []
            for row in res:
                corpus.append(row.title)
                predictions.append(row.prediction)
                permalinks.append(row.permalink)
                id.append(row.id)
            res = zip(corpus, predictions, permalinks, id)
            res = [{'title': t, 'prediction': p, 'permalink': l, 'id': i}
                   for t, p, l, i in res]
            return res
    except Exception as e:
        logger.error(f"Predictions for {fk} not found: {e}")


def store_titles(fk: int, data: list):
    """
    stores corpus and predictions into db
    parameters:
        fk: timestamp.id
        data: tuple consisting of title, prediction, and permalink
    """
    try:
        for item in data:
            stmt = Title(
                timestamp_id=fk,
                title=item['title'],
                prediction=item['prediction'],
                permalink=item['permalink'])
            db.session.add(stmt)
        db.session.commit()
        db.session.close()
    except Exception as e:
        logger.error(f"Error storing prediction for {fk} in database: {e}")
        raise ValueError({e})
    return


def delete_titles(fk: int):
    """
    delete query and timestamp from db
    parameters:
        fk: timestamp.id
    """
    try:
        res = Title.query.filter_by(timestamp_id=fk)
        if res:
            for row in res:
                db.session.delete(row)
            db.session.commit()
            db.session.close()
    except Exception as e:
        logger.error(f"There are no predictions for {fk} to delete: {e}")
    return


def get_comments(fk: int):
    pass


def store_comments(fk: str, predictions: zip):
    pass


def delete_comments(fk: str):
    pass


def get_profile(user_id: int):
    """
    Retrieves user profile from db
    Parameters:
        user_id:    current_user.id
    Returns:
        dictionary containing user profile
    """
    res = Profile.query.filter_by(user_id=user_id).first()
    email = User.query.filter_by(id=user_id).first().email
    try:
        if res:
            res = {'username': res.username,
                   'firstname': res.firstname,
                   'lastname': res.lastname,
                   'biography': res.biography,
                   'email': email,
                   'phone': res.phone}
        return res

    except Exception as e:
        logger.error(f"Profile for {user_id} not found: {e}")
        return None


def update_password(user_id: int, newpassword: str):
    target_user = User.query.filter_by(id=user_id).first()
    setattr(target_user, 'password', newpassword)
    db.session.commit()
    return


def update_profile(user_id: int, fields: dict):
    target_profile = Profile.query.filter_by(user_id=user_id).first()
    target_email = User.query.filter_by(id=user_id).first()
    for key in fields.keys():
        if key != 'email':
            setattr(target_profile, key, fields[key])
        else:
            setattr(target_email, key, fields[key])
    db.session.commit()
    return


logger.removeHandler(file_handler)
