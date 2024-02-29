# TODO add gui
# TODO allow global access
# TODO fix environmental variables

import os.path
import csv
import tkinter as tk
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_creds():
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  
  # get creds if there are none
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      # using envrionmental variables here for now 
      client_config = {
        "installed": {
          "client_id": os.environ.get("CLIENT_ID"),
          "client_secret": os.environ.get("CLIENT_SECRET"),
          "redirect_uris": [os.environ.get("REDIRECT_URI")],
          "auth_uri": "https://accounts.google.com/o/oauth2/auth",
          "token_uri": "https://oauth2.googleapis.com/token",
        }
      }
      flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  return creds

def processSheet(creds):
  # Call the Sheets API
  try :
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    
    # gather input file data
    print('Enter the file path to the txt file: ')
    txt_file_path = input()
    if(not os.path.exists(txt_file_path)):
      print('ERROR: file not found')
      return

    print('enter the delimiting character: ')
    delimiter = input()

    with open(txt_file_path, 'r') as file:
      reader = csv.reader(file, delimiter = delimiter)
      data = [row for row in reader]
    
    body = {
      'values': data
    }

    #gather spreadsheet data
    print('enter spreadsheet id: ')
    SPREADSHEET_ID = input()

    #gather range data
    print('enter the range (default Sheet1): ')
    RANGE_NAME = input()

    # Append data to the spreadsheet
    print('Appending data to the spreadsheet...')
    try : 
      result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        body=body
      ).execute()
      print(f'{result["updates"]["updatedCells"]} cells appended.')

    except :
      print("FAILURE: could not append data to the spreadsheet")

  except HttpError as err:
    print(err)

def tkDriver():
  window = tk.Tk()
  window.title("txt2sheet")
  window.geometry("700x700")
  window.mainloop()


def main():
  creds = get_creds()
  tkDriver()
  processSheet(creds)

if __name__ == "__main__":
  main()