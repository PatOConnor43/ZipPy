#!/usr/bin/python

import httplib2
import pprint

import sys, os

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage

from zipfile import ZipFile, ZIP_DEFLATED
import time

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file) , os.path.join(root, file), ZIP_DEFLATED)

# Create a project at https://console.developers.google.com/project to get these keys
# They are specific to your app
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_SECRET_ID'

# Check https://developers.google.com/drive/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
REDIRECT_URI = 'YOUR_REDIRECT_URI'

# Get time to name the Zipfile
CURRENT_TIME = time.strftime("%c", time.localtime())

# If credentials exist, load them
storage = Storage('credentials')
if storage.get() is not None:
    credentials = storage.get()
   
# On the initial run, you will need to visit the URL given in the terminal,
# This will also create credentials so this process can be automated. 
else:
    
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    
    storage.put(credentials)

# Create an httplib2.Http object and authorize it with our credentials
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

items =  drive_service.files().list(q="title='Python Backup' and trashed=false").execute()['items']parent_id = items[0]['id']

# Create zipfile
myzip = ZipFile(CURRENT_TIME+'.zip', 'a')

# Put the location of the driectory here
zipdir('/HOME/EXAMPLE_DRIECTORY/DIRECTORY_TO_BACKUP/', myzip)


myzip.close()

# Insert a file
media_body = MediaFileUpload(CURRENT_TIME+'.zip', mimetype='application/zip', resumable=True)
body = {
  'title': CURRENT_TIME,
  'description': 'Backup from ' + CURRENT_TIME,
  'mimeType': 'application/zip',
  'parents': [{'id':parent_id}],
  'kind': 'drive#file'
}

# Get download link and remove the local Zipfile
file = drive_service.files().insert(body=body, media_body=media_body).execute()
downloadURL = file['alternateLink']
os.remove(CURRENT_TIME + '.zip')

# Set up email service.
msg = MIMEText('Backup of ' + CURRENT_TIME + '.zip was successful. The archive can be found at ' + downloadURL)
msg['Subject'] = 'Successful Backup'
msg['From'] = ''
msg['To'] = ''

s = smtplib.SMTP('smtp.gmail.com', port=587)
s.ehlo()
s.starttls()
s.ehlo()
# Google may prompt you to make yet another key to use rather than your password.
# You can find more information at https://support.google.com/accounts/answer/185833
s.login('YOUR_EMAIL', 'YOUR_APP_PASSWORD')

s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()
