# My first python program in 1301 GSU, learning about print statements made this small project
# since I was bored in class took thursday and friday around 2-3 hours 
# 08/30/24
"""

print(f"Hello, {first_name.capitalize()} {last_name.capitalize()}. You are studying {major} at GSU!")"""

#, first_name, last_name, major
import copy
import json

def save_data(data):
    with open('user.json', 'w') as f:
        json.dump(data, f, indent=4)

def get_data():
    with open('user.json', 'r') as f:
        data = json.load(f)
        return data
    
def append_data(data, **kwargs):
    for key, value in kwargs.items():
        data[key] = copy.deepcopy(value)
    save_data(data)

def get_user_id():
    data = get_data()
    return 0 if len(data) == 0 else len(data["users"])

def pass_match(username, password, re_password, data):
    if password == re_password:
        new_user = User(**{"_user_id":Number_users(), "_username":username, "_password":password})
        append_data(data, **{"username":[username], "password":[password],"users_codes":[{"username":username, "password":password, "user_id":new_user._user_id}], "users":{new_user._user_id:copy.deepcopy(new_user.__dict__)}})
        print("user created")
        print(f"this is your user info: {new_user}")
    else:
        while password != re_password:
            print("Passwords do not match! Re-enter password again")
            password = input("What would you like your password to be?\n")
            re_password = input("Re-enter your password\n")
        pass_match(username, password, re_password, data)

def createUser(data):
    username = input("What would you like you username to be?\n")
    while username in User.all_users["username"]:
        username  = input(f"username:{username} already exsists! Enter new a username!\n")
    password = input("What would you like your password to be?\n")
    while password in User.all_users["password"]:
        password = input(f"password:{password} already being used! Enter new a password!\n")
    re_password = input("Re-enter your password\n")
    pass_match(username, password, re_password, data)

def auth_user(data):
    username = input("What is your username?\n")
    password = input("what is your password?\n")
    for user_dict in User.all_users["users_codes"]:
        if username == user_dict["username"] and password == user_dict["password"]:
            user_id = user_dict["user_id"]
            user_dict = User.all_users["users"][str(user_id)]
            print("user authenticated!")
            current_user = User(is_new=False,**user_dict)
            return current_user
    return "invalid credentials! User not authenticated"

def add_new_info(new_info, current_user, data):
    added_info = input(f"What is the {new_info} information?\n")
    if len(added_info) > 0:
        data["users"][str(current_user._user_id)][new_info] = added_info
    print(data["users"][str(current_user._user_id)])
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
                ask_to_add = input(f"What you like to add {view_info}")
                if ask_to_add in ["yes", "Yes"]:
                    add_new_info(view_info, current_user)
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
            cls.all_users[key] = data[key]
display_prompt()