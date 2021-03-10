from google_init import *
from db_operations import *
from sqlalchemy.orm.exc import NoResultFound
from entity import Question, Option, Test


def make_test_from_spreadsheet(url: str, user_id: str):
    values = get_values_from_spreadsheet(sheet_service, get_spreadsheet_id_from_url(url))
    questions = []
    for row in values:
        options = []
        for col in row[1:]:
            options.append(Option(text=col))
        questions.append(Question(text=row[0], options=options))

    save_test(test=Test(author=get_or_create_user(user_id), questions=questions))


def start_test_if_exist(test_id, user_id):
    test = get_test_by_id(test_id)
    user = get_or_create_user(user_id)
    user.session = Session(test=test, question_num=0)
    create_or_update_user(user)
    return test.questions[0]


def get_next_question_if_exists(user_id):
    user = get_or_create_user(user_id)
    test = get_test_by_id(user.session.test.id)
    user.session.question_num += 1
    create_or_update_user(user)
    try:
        return test.questions[user.session.question_num]
    except IndexError:
        return None


def save_answer(user_id, option_id):
    user = get_or_create_user(user_id)
    option = get_option(option_id)
    save_answer_to_db(Answer(user=user, option=option))