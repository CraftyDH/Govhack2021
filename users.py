import sys
sys.path.insert(1, "../dependencies")
from block import *
from transaction import *
from safe_json import safe_dump
import json
from threading import Lock
from hashlib import sha256
import base58

mutex = Lock()

CONST_USER_JSON = "./json/user.json"

# #add mutexes here
# def append_json(user_data, fp):
#     mutex.acquire()
#     with open(fp, "r+") as f:
#         data = json.load(f)
#         data.append(user_data)
#         # f.seek(0)
#         safe_dump(data, f)
#     mutex.release()

def modify_json(new_data, fp):
    mutex.acquire()
    with open(fp, "w") as f:
        # f.seek(0)
        safe_dump(new_data, f)
    mutex.release()

def load_user_json() -> dict:
    mutex.acquire() #mutex so no reading at the same time as writing
    out = {} #fail case is dangerous
    with open(CONST_USER_JSON, "r") as f:
        out = json.load(f)
    mutex.release()
    return out

# Functions for retrieving User data and inserting User data.

def create_user(username: str, password: str, public_key = None): 
    if " " in username or len(username) < 5:
        return {"status": "invalid username"}

    if len(password) <= 5 or len(password) >= 255:
        return {"status": "1invalid password"}

    private_key = sha256(base58.b58encode(str(username).encode("ascii"))).hexdigest()

    if not (public_key):
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
    users.append(newuser)

    modify_json(users, CONST_USER_JSON)
    return {
        "status": "success",
        "user": newuser
    }

def get_usernames():
    usernames = []
    users = load_user_json()
    for user in users:
        if user["username"] not in usernames:
            usernames.append(user["username"])
    return usernames if usernames else False

def get_user_by_public_key(public_key):
    users = load_user_json()
    for user in users:
        if user["public_key"] == public_key:
            return user

def get_user_by_username(username): # these already exist but i dont know how to use them look at line 154 (line 154 is public key)
    users = load_user_json()
    for user in users:
        if user["username"] == username:
            return user
    raise Exception("no user found with username")

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
    return [
        {
            "hashed_public_key": hash_key(n["public_key"]), 
            "hashed_private_key": hash_key(n["private_key"]),
            "user": n
        } for n in users
    ]

# Getting User details

def find_user_public_key(public_key):
    try:
        return next(filter(lambda n: n["public_key"] == public_key, load_user_json()))
    except StopIteration:
        return False
    
def find_user_private_key(private_key):
    try:
        return next(filter(lambda n: n["private_key"] == private_key, load_user_json()))
    except StopIteration:
        return False
    

# Calculating user value

def get_user_worth_from_transactions(user : dict) -> float: # This is used for the periodic but unpredictable hedge Fund transfers as well as general transfers
    accumulated_balance = 0
    for block in blockchain.chain:
        for transaction in block.transactions:
            if (transaction.sender == user): # Nvm i forgor  that i wrote this shit
                accumulated_balance -= transaction.amount
            elif (transaction.recipient == user):
                accumulated_balance += transaction.amount
    return accumulated_balance

def get_user_worth_from_smart_contracts_periodic(user: dict) -> float: # This is used for static, fixed transfer dates
    for block in blockchain.contracts_chain:
        for contract in block.transactions:
            if type(contract) == Time_Contract:
                if (user["public_key"] in contract.senders):
                    contribution_amount = contract.senders[user["public_key"]] * (-1)
                elif (user["public_key"] in contract.recipients):
                    contribution_amount = contract.recipients[user["public_key"]]
                return contract.get_num_previous_transactions() * contribution_amount
    return 0

def get_user_worth(user: dict) -> float:
    return round(get_user_worth_from_transactions(user) + get_user_worth_from_smart_contracts_periodic(user), 2)

def get_user_transactions(user : dict):
    for block in blockchain.chain:
        for transaction in block.transactions:
            if (transaction.sender == user):
                pass
            elif (transaction.recipient == user):
                pass
    return [transaction.amount for block in blockchain.chain for transaction in block.transactions if (transaction.sender == user) or (transaction.recipient == user)]

def get_all_contracts():
    return [contract for block in blockchain.contracts_chain for contract in block.transactions]