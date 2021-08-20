import sys
sys.path.insert(1, "../dependencies")
from hashlib import *
import block, base58, json, transaction

CONST_USER_JSON = "/server/json/user.json"

"""
account {
    username varchar(15) unique primary key,
    password varchar(20),
    publicKey varchar(100) unique,
    privateKey varchar(100) unique,
    local_ledger varchar(1000), --chain
}
"""
# Miscellaneous 

class User(object):
    username: str
    password: str
    def __init__(self, username: str, password: str, private_key, local_ledger: block.BlockChain):
        self.username = username
        self.password = password
        self.private_key = private_key
        self.local_ledger = local_ledger 

def append_json(user_data, fp):
    with open(fp, "r+") as f:
        data = json.load(f)
        data.append(user_data)
        f.seek(0)
        json.dump(data, f)

def modify_json(new_data, fp):
    with open(fp, "r+") as f:
        f.seek(0)
        json.dump(new_data)

# Functions for retrieving User data and inserting User data.

def create_user(username: str, password: str): 
    private_key = sha256(base58.b58encode(str(username).encode())).hexdigest()
    public_key = str(sha256(sha256(private_key.encode()).hexdigest().encode()).hexdigest())
    # check to see if username is not inside the database
    users = json.load(CONST_USER_JSON)
    for user in users:
        if (user["username"] == username):
            return False
        if ("old_username" in user):
            if (user["old_username"] == username):
                return False
    #
    append_json(User(username, password, public_key, private_key).__dict__, CONST_USER_JSON)
    return User(username, password, public_key, private_key)

def get_user(username: str): 
    users = json.load(CONST_USER_JSON)
    for user in users:
        if (user["username"] == username):
            return User(username, user["password"], user["public_key"], user["private_key"], user["local_ledger"])
    return None

# Modifying the JSON database

def modify_username(username: str, password: str, new_username: str) -> bool:
    users = json.load(CONST_USER_JSON)
    for user in range(len(users)):
        if (users[user]["username"] == username) and (users[user]["password"] == password):
            users[user]["username"] = new_username
            users[user]["old_username"] = username
            modify_json(users, CONST_USER_JSON)
            return True
    return False # User doesn't exist

def modify_password(username: str, password: str, new_password: str) -> bool:
    users = json.load(CONST_USER_JSON)
    for user in range(len(users)):
        if (users[user]["username"] == username) and (users[user]["password"] == password):
            users[user]["password"] = new_password
            modify_json(users, CONST_USER_JSON)
            return True
    return False # User doesn't exist

def delete_user(username: str, password : str) -> bool:
    users = json.load(CONST_USER_JSON)
    for user in range(len(users)):
        if (users[user]["username"] == username) and (users[user]["password"] == password):
            del users[user]
            modify_json(users, CONST_USER_JSON)
            return True

def add_to_local_ledger(username: str, transact: transaction) -> bool: # Adding local transactions to the local ledger
    users = json.load(CONST_USER_JSON)
    for user in range(len(users)):
        if (users[user]["username"] == username):
            users[user]["local_ledger"].append(transact)
            modify_json(users, CONST_USER_JSON)
            return True
    return False

# Handling Login's and Transactions

def login(username: str, password: str) -> User: # -> User: # this is the same process as get_user?
    users = json.load(CONST_USER_JSON)
    for user in users:
        if (user["username"] == username) and (user["password"] == password):
            return True
    return False # User doesn't exist
    


