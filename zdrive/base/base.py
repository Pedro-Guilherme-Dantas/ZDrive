#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

class DriveAPI:
    global SCOPES

    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):

        # Variable self.creds will
        # store the user access token.
        # If no valid token found
        # we will create one.
        self.creds = None

        # The file token.pickle stores the
        # user's access and refresh tokens. It is
        # created automatically when the authorization
        # flow completes for the first time.

        # Check if file token.pickle exists
        if os.path.exists('token.pickle'):
            # Read the token from the file and
            # store it in the variable self.creds
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available,
        # request the user to log in.
        self.creds = Credentials.from_service_account_file(filename="gitlab-1280-6f1fad5cb8ab.json")

        # Connect to the API service
        self.service = build('drive', 'v3', credentials=self.creds)

    def listFolders(self):
        try:
            page_token = None
            folders = []
            while True:
                response = self.service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                     spaces='drive',
                                                     fields='nextPageToken, files(id, name)',
                                                     pageToken=page_token).execute()

                for file in response.get('files', []):
                    # Process change
                    folder_data = (file.get('name'), file.get('id'))
                    folders.append(folder_data)

                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            return folders
        except Exception as e:
            print(str(e))
            return None
