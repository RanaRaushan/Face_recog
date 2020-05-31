from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle



def main_out(df):

    # change this by your sheet ID
    online_attend_sheet = '18t2bhgjUkDOLirMYfY0Cw0QsD0V6OwOxPNU7gHrFu6s'

    # change the range if needed
    SAMPLE_RANGE_NAME = 'A1:AA1000'


    def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
        global service
        SCOPES = [scope for scope in scopes[0]]
        # print(SCOPES)

        cred = None

        if os.path.exists('token_write.pickle'):
            with open('token_write.pickle', 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
                cred = flow.run_local_server()

            with open('token_write.pickle', 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(api_service_name, api_version, credentials=cred)
            print(api_service_name, 'service created successfully')
            # return service
        except Exception as e:
            print(e)
            # return None


    # change 'my_json_file.json' by your downloaded JSON file.
    Create_Service('credentials.json', 'sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets'])


    def Export_Data_To_Sheets():

        response_date = service.spreadsheets().values().append(
            spreadsheetId=online_attend_sheet,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict(
                majorDimension='ROWS',
                values=df.T.reset_index(drop=True).T.values.tolist())
        )
        response_date.execute()
        # print('Sheet successfully Updated')


    Export_Data_To_Sheets()




