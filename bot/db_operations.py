from db_init import get_session
from entity import *
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def get_or_create_user(telegram_id):
    telegram_id = str(telegram_id)
    rows = get_session().query(User).filter(User.telegram_id == telegram_id).all()

    if len(rows) == 0:
        user = User(telegram_id=telegram_id)
        session = get_session()
        session.add(user)
        session.commit()
        return user
    else:
        user = rows[0]
        return user


def update_username(telegram_id, username, fullname):
    user = get_or_create_user(telegram_id)
    user.username = username
    user.fullname = fullname
    session = get_session()
    session.add(user)
    session.commit()
    return user


def save_test(test: Test):
    session = get_session()
    session.add(test)
    session.commit()


def get_test_by_id(id):
    return get_session().query(Test).filter(Test.id == int(id)).one()


def create_or_update_user(user):
    session = get_session()
    session.add(user)
    session.commit()


def get_option(id):
    return get_session().query(Option).filter(Option.id == int(id)).one()


def save_answer_to_db(answer):
    session = get_session()
    session.add(answer)
    session.commit()
