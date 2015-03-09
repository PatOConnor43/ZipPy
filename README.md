# ZipPy
A small Python script that can zip together a backup of your files, upload them to Google Drive, then email you if it completed.

# How It Works
Because we're dealing with a Google accounts we will need some credentials to login to your Drive account, then later an app pasword to send a notification email. ZipPy first looks for credentials for the Drive, if they aren't there you will be prompted to create credentials on a Google site. The new credentials will then be saved so this process can be automated. Next, you will need to tell it which directories to zip up. I have it hardcoded because this was something I whipped up in about a day, you are welcome to change that and give it parameters instead though. Then, it adds that zipfile to your drive and deletes the local copy. Once that is finished it will attempt to log into the email address that is given, (again hardcoded for me), and send a conformation email.

# Requirements
You will need the Google API for python which can be installed by using this command in terminal: <br>
<code>easy_install --upgrade google-api-python-client</code> <br>
or <br>
<code>pip install --upgrade google-api-python-client</code>

Everything else should be part of the standard library.

# Intended Use
Once you run this initially and get all your credentials in order, you can automate this pretty easily. Currently, I am using a Cron job to make a backup every other week.

# Important Note
This script does involve uploading files, which depending on your upload speed can take a long time. If you notice that the script is taking a long time, that is probably why. Just give it some time.

# Resources - Can also be found in code
<b>Create Google Project:</b> https://console.developers.google.com/project <br>
<b>Available Permission Scopes:</b> https://developers.google.com/drive/scopes <br>
<b>Creating App Password:</b> https://support.google.com/accounts/answer/185833

# Possible Future Developement
* Input parameters for flexibility
* Better error handling (email if failed backup, etc.)
* Implement progress bar
