from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import argparse
import sys, time
from .utils import *
from termcolor import colored

import os
import json
from .ascii_art import banana_car

from .message import main as message_main

yes_no_count = 0

json_path = pkg_resources.resource_filename('bhagyashree', 'assets/data.json')

def auth_check():
    with open(json_path , "r") as file:
        data = json.load(file)
    return data["auth"], data["count"]

def change_value():
    json_path = pkg_resources.resource_filename('bhagyashree', 'assets/data.json')
    
    with open(json_path, "r") as file:
        data = json.load(file)
        
    data["auth"] = 1
    data["count"] = 1
    
    with open(json_path, "w") as file:
        json.dump(data, file)

def ask_yes_no(text, count):
    temp = input(text)
    
    if count >= 3:
        print(colored("\nok bye\n", "red"))
        sys.exit()
        
    if count >= 2:
        print(colored("\naaaaaaaaaaaa just type yes or no bruh\n".upper(), "yellow"))
        ask_yes_no("YES or NO: ", count+1)
    
    if temp.lower() in ["y", "yes"]:
        return "y"
    
    elif temp.lower() in ["n", "no"]:
        return "n"
    
    else:
        print("invalid input")
        print(yes_no_count)
        ask_yes_no("wanna send me a message? (YES/NO): ", count+1)

def post_auth():
    print("hi")    

def main():
    parser = argparse.ArgumentParser(description="Hi, this is a package made for Bhagyashree Tanwar.")
    parser.add_argument("-d", "--desc", action="store_true", help="gives a description.")
    parser.add_argument("-", "--banana-car", action="store_true", help="draws the banana car.")    
    parser.add_argument("-m", "--message", action="store_true", help="redirects to my link tree.")
    parser.add_argument("-s", "--secret", action="store_true", help="enter your birthday in the format DDMM.")

    args = parser.parse_args()
    
    if not any(vars(args).values()) and not args.secret:
        try:
            is_auth, count = auth_check()
            if not is_auth and count==0:
                dob = input("Type your DOB: ")
                if str(dob) == "2907":
                    change_value()
                    # print(auth_check())
                    post_auth()
                else:
                    print("nope")
            
            elif is_auth:
                post_auth()
        
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
    if args.secret:
        try:
            db = input("Enter the your DOB (DDMM): ")
            
            if str(db)=="2907":
                print(colored("Access granted", "green"))
                time.sleep(1)
                print(colored("Loading cassette...", "yellow"))
                play_audio("assets/audio/loading_cassette.mp3")
                time.sleep(1)
                print(colored("Empty cassette detected.", "red", attrs=["blink"]))
            else:
                print(colored("you're not the one."))
                sys.exit()
        
        except AttributeError:
            print(colored("Type the date after the no input given."))
            
    if args.banana_car:
        print(colored(banana_car, "yellow"))
        
    if args.message:
        yes_no = ask_yes_no("wanna send me a message? (y/n): ", yes_no_count)
        # yes_no = input("wanna send me a message? (y/n): ")
        
        if yes_no.lower() == "y":
            print("loading irc...")
            message_main()

        elif yes_no.lower() == "n":
            sys.exit()

if __name__ == "__main__":
    main()