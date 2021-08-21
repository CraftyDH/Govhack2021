import sys
sys.path.insert(1, "../dependencies")
import block, transaction
from safe_json import safe_dump
import json
from threading import Lock
from hashlib import sha256
import base58

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
    if " " in username or len(username) < 5:
        return {"status": "invalid username"}

    if len(password) <= 5 or len(password) >= 255:
        return {"status": "invalid password"}

    private_key = sha256(base58.b58encode(str(username).encode("ascii"))).hexdigest()
    public_key = str(sha256(sha256(private_key.encode()).hexdigest().encode()).hexdigest())

    users = load_user_json()
    for user in users:
        if (user["username"] == username):
            return {"status": "user exists"}
    
    newuser =  {
        "username": username,
        "password": password,
        "public_key": public_key,
        "private_key": private_key,
    }
    append_json(newuser, CONST_USER_JSON)
    return {
        "status": "success",
        "user": newuser
    }

# Modifying the JSON database
def modify_password(username: str, password: str, new_password: str) -> bool:
    users = load_user_json()
    if len(password) <= 5 or len(password) >= 255:
        return {"status": "invalid password"}

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
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                user["password"] = None
                modify_json(users, CONST_USER_JSON)
                return {"status": "success"}
            return {"status": "incorrect password"}
    return {"status": "no user found"}


def login(username: str, password: str):
    users = load_user_json()
    for user in users:
        if user["username"] == username and user["password"] == None:
            return {"status": "user deleted"}
        elif user["username"] == username and user["password"] == password:
            return {
                "status": "success",
                "user": {
                    "username": username,
                    "password": user["password"],
                    "public_key": user["public_key"],
                    "private_key": user["private_key"],
                }
            }
        elif user["username"] == username:
            return {"status": "incorrect password"}
    return {"status": "no user found"}

def hash_key(key):
    return sha256(key.encode()).hexdigest()
    

def get_private_public_keys():
    users = load_user_json()
    return [{ 
            "hashed_public_key": hash_key(n["public_key"]), 
            "hashed_private_key": hash_key(n["private_key"]),
            "user": n
        } for n in users
    ]