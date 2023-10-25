import time
import configparser
import sys
import shutil
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Reading from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# set the cookie values
sessionid = config['cookie']['sessionid']
username = config['cookie']['username'] 
csrf_session_id = config['cookie']['csrf_session_id']

# set the header values
x_secsdk_csrf_token = config['header']['x-secsdk-csrf-token']

# set the video id to be deleted
video_id = config['tiktok']['videoid']

# Set up Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--detached")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--user-data-dir=/temp_profile")  # Set the correct path for the user data directory
# chrome_options.add_argument(f"--proxy-server=http://localhost:8080")
# chrome_options.add_argument("--ignore-certificate-errors")

# Set up Selenium WebDriver (e.g., using Chrome)
driver = webdriver.Chrome(options=chrome_options)

# Navigate to TikTok login page
driver.get("https://www.tiktok.com")

# set the sessionid cookie
driver.add_cookie({'name': 'sessionid', 'value': sessionid})

# Refresh the page
driver.refresh()

# Add a flag to track whether the video deletion was successful
video_deleted_successfully = False

def delete_video(video_id):
    global video_deleted_successfully

    # Create a requests Session object
    s = requests.Session()
    
    # Set the User-Agent header to match the browser's User-Agent
    selenium_user_agent = driver.execute_script("return navigator.userAgent;")
    s.headers.update({"User-Agent": selenium_user_agent})
    
    # required cookies for delete request: csrf_session_id(www.tiktok.com),
    # set the cookies
    s.cookies.set("csrf_session_id", csrf_session_id, domain="www.tiktok.com", path="/", secure=True)
    
    # required header for delete request: x-secsdk-csrf-token
    headers = {
        "x-secsdk-csrf-token": x_secsdk_csrf_token,
    }

    # Set the request URL
    url = f"https://www.tiktok.com/api/aweme/delete/?aweme_id={video_id}&target={video_id}"

    # Issue the POST request
    try:
        response = s.post(url, headers=headers)
        if response.ok:
            if response.json()["status_msg"] == "Login expired":
                print(f"Failed to delete video: {response.status_code}, Response body: {response.text}")
                video_deleted_successfully = False
            else:
                print("Video deleted successfully!")
                video_deleted_successfully = True
        else:
            print(f"Failed to delete video: {response.status_code}, Response body: {response.text}")
            video_deleted_successfully = False
    except Exception as e:
        print(f"An error occurred: {e}")
        video_deleted_successfully = False

# Wait for login to complete, Check if login was successful by checking the URL, 
# if after 10 seconds the url is not https://www.tiktok.com/foryou, then exit the program
try:
    WebDriverWait(driver, 10).until(EC.url_to_be("https://www.tiktok.com/explore"))
    print("Login successful!")
    
    # go to the profile page
    profile_url = f"https://www.tiktok.com/@{username}"
    driver.get(profile_url)
    print(f"Navigated to profile page of user: {username}")
    
    try:
        # if delete video function fails, print error and exit
        delete_video(int(video_id))
        
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
        
except:
    print("Login failed!")
    driver.save_screenshot("screenshot.png")
    sys.exit(1)

# At the end of your script, delete the custom user data directory
if not video_deleted_successfully:  # Only quit the driver and delete the directory if the video wasn't deleted successfully
    driver.quit()  # Ensure the browser is closed before deleting the directory
    shutil.rmtree("/temp_profile")