# Tiktok Delete Video Script
This script allows users to automate the process of deleting videos from TikTok by providing the video ID and a couple other values. (since TikTok doesn't have an API for deleting videos weirdly enough)

## Configuration
Before running the script, you need to set up the configuration file config.ini which contains the necessary cookies and headers required for the script to function. The configuration file has the following sections:

cookie: This section contains the sessionid, csrf_session_id, and username cookies.
header: This section contains the x-secsdk-csrf-token header.
tiktok: This section contains the videoid which is the ID of the video you want to delete.

```
[cookie]
sessionid = 
csrf_session_id = 
username = 

[header]
x-secsdk-csrf-token = 

[tiktok]
videoid = 
```

## Requirements
The script has a few dependencies which are listed in the requirements.txt file. You can install these dependencies using pip:
```
pip install -r requirements.txt
```

## Usage
To use the script, simply run the tiktok_delete_by_vidId.py file. The script uses Selenium to automate the browser actions and requires the necessary cookies and headers to be set in the config.ini file.