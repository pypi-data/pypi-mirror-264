import time, sys
from termcolor import colored
import requests, datetime, pytz, json

from .__constants import *
from .__utils import load_animation

token = json.load(open(JSON_FILE_PATH))['token']
headers = {
    'Authorization': token,
    'Content-Type': 'application/json',
}

def get_time():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    return current_time.strftime('%Y-%m-%d %H:%M:%S %Z')

def send_message_to_server(message):
    current_time = get_time()
    username = "bhagyashree"
    
    data = {
            'time': current_time,
            'username': username,
            'message': message, 
            }
    
    response = requests.post(API_URL, json=data, headers=headers)
        
    if response.status_code == 200:
        return f"[{current_time}] {username}: {data['message']}"
    else:
        return f"request failed : {response.status_code}"
        
def main():
    try:
        input_message = input("Enter your message: ")
        
        print("sending message (may take a while sry)...")
 
        loading_animation = [".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-", ".(^-^)'", "-(^-^)-", "'(^-^).", "-(^-^)-"]
 
        send_message_to_server(input_message)
        load_animation(pref="Sending ... ", i=0)

        for i in range(10):
            time.sleep(0.1)
            print(f"\r{loading_animation[i % len(loading_animation)]}", end="")
        
        sys.stdout.flush()

        print(colored("\nMessage sent successfully!", "green"))

    except Exception as e:
        print(f"An unexpected error occurred: {e}")