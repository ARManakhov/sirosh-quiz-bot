from google_init import *
from db_operations import *
from sqlalchemy.orm.exc import NoResultFound
from entity import Question, Option, Test


def make_test_from_spreadsheet(url: str, user_id: str):
    values = get_values_from_spreadsheet(sheet_service, get_spreadsheet_id_from_url(url))
    default_background = values['properties']['defaultFormat']['backgroundColor']
    real_data = values['sheets'][0]['data'][0]['rowData']
    questions = []
    for row_data in real_data:
        row = row_data['values']
        options = []
        for col in row[1:]:
            options.append(Option(text=list(col['userEnteredValue'].values())[0],
                                  correct=col['effectiveFormat']['backgroundColor'] != default_background))
        questions.append(Question(text=row[0]['userEnteredValue']['stringValue'], options=options))

    sheet = create_new_spreadsheet()
    test = Test(author=get_or_create_user(user_id), questions=questions, spreadsheet_id=sheet['spreadsheetId'])
    save_test(test=test)
    return test


def create_new_spreadsheet():
    sheet = create_spreadsheet(sheet_service)
    share_spreadsheet(drive_service, sheet)
    return sheet


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


def get_current_question(user_id):
    user = get_or_create_user(user_id)
    test = get_test_by_id(user.session.test.id)
    try:
        return test.questions[user.session.question_num]
    except IndexError:
        return None


def save_answer(user_id, option_id):
    user = get_or_create_user(user_id)
    option = get_option(option_id)
    save_answer_to_db(Answer(user=user, option=option, question=option.question))


def clean_session(user_id):
    user = get_or_create_user(user_id)
    user.session = None
    create_or_update_user(user)


def user_has_session(user_id):
    user = get_or_create_user(user_id)
    return user.session is not None


def try_save_text_answer(user_id, text):
    user = get_or_create_user(user_id)
    question = get_current_question(user_id)
    if question is None:
        clean_session(user_id=user_id)
    else:
        if len(question.options) == 0:
            save_answer_to_db(Answer(user=user, question=question, text=text))
            return True
    return False


def save_user_to_test(user_id):
    user = get_or_create_user(user_id)
    test = get_test_by_id(user.session.test.id)
    update_test_report(user.session.test.id)
    user.resolved_tests.append(test)
    user.session = None
    create_or_update_user(user)


def update_test_report(test_id):
    update_test_report_spreadsheet(sheet_service, get_test_by_id(test_id))
