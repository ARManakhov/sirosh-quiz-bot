import os.path
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import pickle
import os
from db_operations import get_or_create_user
from entity import Answer


def get_google_creds(google_credentials, scopes):
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(google_credentials, scopes)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_google_drive_service(creds):
    return build('drive', 'v3', credentials=creds)


def get_google_sheet_service(creds):
    return build('sheets', 'v4', credentials=creds)


def create_spreadsheet(sheet_service):
    spreadsheet = {'properties': {'title': 'title'}}
    return sheet_service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()


def share_spreadsheet(drive_service, spreadsheet):
    domain_permission = {
        'type': 'anyone',
        'role': 'reader',
        'allowFileDiscovery': True,
    }

    drive_service.permissions().create(
        fileId=spreadsheet['spreadsheetId'],
        body=domain_permission,
        fields="id"
    ).execute()


def get_spreadsheet_id_from_url(url: str):  # todo add link validation
    return PurePosixPath(unquote(urlparse(url).path)).parts[3]


def get_values_from_spreadsheet(sheet_service, spreadsheet_id: str):
    return sheet_service.spreadsheets() \
        .get(spreadsheetId=spreadsheet_id, ranges=["A1:F100"], includeGridData=True) \
        .execute()


def update_spreadsheet_raw_values(sheet_service, value, spreadsheetId):
    body = {
        'values': value
    }
    result = sheet_service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range="A1:Z100",
                                                          valueInputOption="RAW", body=body).execute()


def update_report_spreadsheet_values(sheet_service, value, spreadsheetId):
    raw_values = []
    for i in value:
        raw_i = []
        for j in i:
            if isinstance(j, Answer):
                if j.option is None:
                    raw_i.append(j.text)
                else:
                    raw_i.append(j.option.text)
            else:
                raw_i.append(j)
        raw_values.append(raw_i)
    update_spreadsheet_raw_values(sheet_service, raw_values, spreadsheetId)


def update_test_report_spreadsheet(sheet_service, test):
    user_answers = dict()
    for q in test.questions:
        for a in q.answers:
            if a.user_id not in user_answers:
                user = get_or_create_user(a.user_id)
                user_answers[a.user_id] = [user.username, user.fullname]
            user_answers[a.user_id].append(a)

    values = []
    for k in user_answers.keys():
        values.append(user_answers[k])

    update_report_spreadsheet_values(sheet_service, values, test.spreadsheet_id)


creds = get_google_creds(json.loads(os.environ['GOOGLE_CREDENTIALS']),
                         ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

drive_service = get_google_drive_service(creds)
sheet_service = get_google_sheet_service(creds)
