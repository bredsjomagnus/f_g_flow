from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]


def get_sheet_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('sheet_token.pickle'):
        with open('sheet_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sheet_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('sheet_token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


# def create_spreadsheet(service, spreadsheet_title):
#     """
#     Create new spreadsheet
#     """
#     SPREADSHEET_ID = ""
#     spreadsheet_body = {
#         "properties": {
#             "title": spreadsheet_title
#         }
#     }
#     try:
#         request = service.spreadsheets().create(body=spreadsheet_body)
#         spreadsheet = request.execute()
#         SPREADSHEET_ID = spreadsheet['spreadsheetId']
#     except Exception as e:
#         print("While trying to create new spreadsheet error: ", e)
#         sys.exit()

#     return SPREADSHEET_ID


# def add_content(service, SPREADSHEET_ID, sheet_ids, contents):
#     for sheet_name, sheet_id in sheet_ids.items():

#         klass_range = sheet_name+'!A1'
#         try:
#             range = klass_range
#             values = contents[sheet_name]
#             resource = {
#                 "values": values
#             }
#             # use append to add rows and update to overwrite
#             response = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
#                                                               range=range, body=resource, valueInputOption="USER_ENTERED").execute()
#             # print('.', end="")
#         except Exception as e:
#             print("While trying to append values error: ", e)
#             sys.exit()


# def update_spreadsheet(service, SPREADSHEET_ID, _object, message):
#     """
#     Updating the sheets with _object generated for column widht, colors and alignment
#     """

#     requests = []
#     for key in _object:
#         requests.append(_object[key])

#     # Trying to update spreadsheet with assigned requests
#     try:
#         body = {
#             "requests": requests
#         }
#         response = service.spreadsheets().batchUpdate(
#             spreadsheetId=SPREADSHEET_ID, body=body).execute()

#     except Exception as e:
#         print("While trying to batchUpdate error: ", e)
#         sys.exit()

#     return response
