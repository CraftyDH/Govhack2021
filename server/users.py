import sys
sys.path.insert(1, "../dependencies")
#import block, transactions, base58
import json
from safe_json import safe_dump
import hashing
from threading import Lock
mutex = Lock()

#add mutexes here
def append_json(user_data, fp):
    mutex.acquire()
    with open(fp, "r+") as f:
        data = json.load(f)
        data.append(user_data)
        f.seek(0)
        safe_dump(data, f)
    mutex.release()

def modify_json(new_data, fp):
    mutex.acquire()
    with open(fp, "w") as f:
        # f.seek(0)
        safe_dump(new_data, f)
    mutex.release()

CONST_USER_JSON = "./json/user.json"
def load_user_json():
    mutex.acquire() #mutex so no reading at the same time as writing
    out = {} #fail case is dangerous
    with open(CONST_USER_JSON, "r") as f:
        out = json.load(f)
    mutex.release()
    return out

# Functions for retrieving User data and inserting User data.

def create_user(username: str, password: str): 
    #! JAMIE FIX THIS
    # private_key = sha256(base58.b58encode(str(username).encode("ascii"))).hexdigest()
    # public_key = str(sha256(sha256(private_key.encode()).hexdigest().encode()).hexdigest())
    # check to see if username is not inside the database

    private_key = hashing.hash(username) #? what? why is hashing hashing the username
    public_key = hashing.hash(private_key)

    file = open(CONST_USER_JSON)
    users = json.load(file)
    for user in users:
        if (user["username"] == username):
            return {"username": None}
    
    newuser =  {
        "username": username,
        "password": password,
        "public_key": public_key,
        "private_key": private_key,
        "local_ledger": []
    }

    append_json(newuser, CONST_USER_JSON)
    return newuser

def get_user(username: str):
    users = load_user_json()
    for user in users:
        if (user["username"] == username):
            return {
                "username": username,
                "password": user["password"],
                "public_key": user["public_key"],
                "private_key": user["private_key"],
                "local_ledger": user["local_ledger"]
                }
    return {"status": "no user found"}

# Modifying the JSON database

def modify_username(username: str, new_username: str, password: str) -> bool:
    users = load_user_json()
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                user["username"] = new_username
                modify_json(users, CONST_USER_JSON)
                return {"message": "success"}
            return {"message": "incorrect password"}
    return {"status": "no user found"} # User doesn't exist

def modify_password(username: str, password: str, new_password: str) -> bool:
    users = load_user_json()
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                user["password"] = new_password
                modify_json(users, CONST_USER_JSON)
                return {"status": "success"}
            return {"status": "incorrect password"}
    return {"status": "no user found"}

def delete_user(username: str, password : str) -> bool:
    users = load_user_json()
    for (index, user) in enumerate(users):
        if user["username"] == username:
            if user["password"] == password:
                del users[index]
                modify_json(users, CONST_USER_JSON)
                return {"status": "success"}
            return {"status": "incorrect password"}
    return {"status": "no user found"}


def add_to_local_ledger(username: str, password: str, transact) -> bool: # Adding local transactions to the local ledger
    users = load_user_json()
    for user in users:
        if (user["username"] == username):
            if (user["password"] == password):
                user["local_ledger"].append(transact)
                modify_json(users, CONST_USER_JSON)
                return {"status": "success"}
            return {"status": "incorrect password"}
    return {"status": "no user found"}

# Handling Login's and Transactions

def login(username: str, password: str): # -> User: # this is the same process as get_user?
    users = load_user_json()
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                return {"status": "success"}
            return {"status": "incorrect password"}
    return {"status": "no user found"}
