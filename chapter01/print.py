# My first python program in 1301 GSU, learning about print statements made this small project
# since I was bored in class took thursday and friday around 2-3 hours 
# 08/30/24
"""

print(f"Hello, {first_name.capitalize()} {last_name.capitalize()}. You are studying {major} at GSU!")"""

#, first_name, last_name, major
import copy
import getpass
import json
import string
import random
import csv
import hashlib


def save_data(data):
    with open('user.json', 'w') as f:
        json.dump(data, f, indent=4)

def get_data():
    with open('user.json', 'r') as f:
        data = json.load(f)
        return data
    
def append_data(data, **kwargs):
    for key, value in kwargs.items():
        if key == "users":
            num = list(value.keys())[0]
            if "users" not in data.keys():
                data["users"] = {}
            data["users"][num] = copy.deepcopy(value.get(num))
            continue
        if key in data.keys():
            data[key].append(copy.deepcopy(value))
        else:
            data[key] = [copy.deepcopy(value)]
    save_data(data)

def get_user_id():
    data = get_data()
    return 0 if len(data) == 0 else len(data["users"])

def generate_salt():
    array = []
    random_string = string.ascii_uppercase + string.ascii_lowercase + string.punctuation
    for c in random_string:
        array.append(c)
    random.shuffle(array)
    return_string = ""
    for index, c in enumerate(array):
        if index < 14:
            return_string+=c
        else:
            break
    with open("salt.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([return_string])
    data = []
    with open("salt.csv", "r") as reader_file:
        reader = csv.reader(reader_file)
        for line in reader:
            data.append(line)
        random.shuffle(data)
        with open("salt.csv", "w") as writer_file:
            writer = csv.writer(writer_file)
            for line in data:
                writer.writerow(line)
    return return_string



def pass_match(username, password, re_password, data):
    if password == re_password:
        salt = generate_salt()
        print(salt)
        salted_password = salt + password
        hashed_password_object = hashlib.sha256(salted_password.encode())
        hashed_password = hashed_password_object.hexdigest()
        new_user = User(**{"_user_id":Number_users(), "_username":username, "_password":hashed_password})
        append_data(data, **{"username": username, "password":hashed_password,"users_codes":{"username":username, "password":hashed_password, "user_id":new_user._user_id}, "users":{new_user._user_id:new_user.__dict__}})
        print("user created")
        print(f"this is your user info: {new_user}")
    else:
        while password != re_password:
            print("Passwords do not match! Re-enter password again")
            password = getpass.getpass("What would you like your password to be?\n")
            re_password = getpass.getpass("Re-enter your password\n")
        pass_match(username, password, re_password, data)

def password_check(password):
    password_conditions = [False, False, False]
    if len(password) > 8:
        password_conditions[2] = True
    for c in password:
        if c in string.punctuation:
           password_conditions[0] = True
        elif c in string.ascii_uppercase:
            password_conditions[1] = True
    for condition in password_conditions:
        if condition == False:
            return False
    return True

def createUser(data):
    username = input("What would you like you username to be?\n")
    while username in User.all_users["username"]:
        username  = input(f"username:{username} already exsists! Enter new a username!\n")
    password = getpass.getpass("What would you like your password to be?\nPassword needs to have 9 or more characters, 1 special character, and 1 uppercase character.\n")
    while not password_check(password):
        password = getpass.getpass(f"password not string enough! Enter a stronger password.\nPassword needs to have 9 or more characters, 1 special character, and 1 uppercase character.\n")
    while password in User.all_users["password"]:
        password = getpass.getpass(f"password already being used! Enter new a password!\n")
    re_password = getpass.getpass("Re-enter your password\n")
    pass_match(username, password, re_password, data)

def auth_pass(user_dict):
    user_id = user_dict["user_id"]
    user_dict = User.all_users["users"][str(user_id)]
    print("user authenticated!")
    current_user = User(is_new=False,**user_dict)
    return current_user

def auth_user(data):
    username = input("What is your username?\n")
    password = getpass.getpass("what is your password?\n")
    salts = []
    with open("salt.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            salts.append(line)
    for user_dict in User.all_users["users_codes"]:
        if username == user_dict["username"]:
            hashed_password = hash(password)
            for salt in salts:
                print(salt[0])
                print(salt[0]+password)
                salted_password = salt[0] + password
                hashed_password_object = hashlib.sha256(salted_password.encode())
                hashed_password = hashed_password_object.hexdigest()
                print(hashed_password)
                if hashed_password == user_dict["password"]:    
                    return auth_pass(user_dict)
            if hashed_password == user_dict["password"]:
                return auth_pass(user_dict)
    print("invalid credentials! User not authenticated")
    auth_user(data)

def add_new_info(new_info, current_user, data):
    added_info = getpass.getpass(f"What is the {new_info} information?\n")
    if len(added_info) > 0:
        data["users"][str(current_user._user_id)][new_info] = added_info
    save_data(data)
    print("new information added")

def display_prompt():
    data = get_data()
    User.create_lists(data) 
    user_id = 0
    command = input("What would you like to do? type 'create user', 'add info', 'view info', 'view all info', 'leave'.\n")
    if command == "leave":
        return
    elif command == "create user":
        createUser(data)
    elif command == "add info":
        current_user = auth_user(data)
        if isinstance(current_user, str):
            return current_user
        new_info = input("What new info would you like to add to your account?\n")
        add_new_info(new_info, current_user, data)
    elif command == "view info":
        current_user = auth_user(data)
        if isinstance(current_user, str):
            print(current_user)
        else:
            view_info = input("What info would you like to view?\n")
            if view_info in current_user.__dict__.keys():
                print(f"{view_info} : {current_user.__dict__[view_info]}")
            else:
                print(f"{view_info} information is not stored on that user?\n")
                ask_to_add = input(f"Would you like to add {view_info}?\n")
                if ask_to_add in ["yes", "Yes"]:
                    add_new_info(view_info, current_user, data)
    elif command == 'view all info':
        current_user = auth_user(data)
        if isinstance(current_user, str):
            print(current_user)
        else:
            for key in current_user.__dict__.keys():
                if not key in ['_user_id', '_username', '_password']:
                    info = current_user.__dict__[key]
                    print(f"{key} information is {info}")
    display_prompt()

class Number_users:
    _number_users = get_user_id()
    is_new = True
    def __new__(self):
        if __class__.is_new:
            Number_users._number_users +=1
            return Number_users._number_users

class User():
    all_users = {"username":[], "password":[], "users_codes":[], "users":{}}
    def __init__(self, is_new=True, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if is_new:
            User.all_users["users"][self._user_id] = copy.deepcopy(self.__dict__)
            User.all_users["users_codes"].append({"username":self._username, "password":self._password, "user_id":self._user_id})
            User.all_users['username'].append(self._username)
            User.all_users["password"].append(self._password)
        ##self.id = number_users + 1
    def __str__(self):
        print(User.all_users)
        return f"user id {self._user_id}: username {self._username}, password {self._password}"
    @classmethod
    def create_lists(cls, data):
        if len(data) == 0:
            return
        for key in cls.all_users.keys():
            cls.all_users[key] = copy.deepcopy(data[key])
display_prompt()