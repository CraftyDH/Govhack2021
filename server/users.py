import hashlib
import block
CONST_USER_JSON = "/json/user.json"

"""
account {
    username varchar(15) unique primary key,
    password varchar(20),
    publicKey varchar(100) unique,
    privateKey varchar(100) unique,
    local_ledger varchar(1000), --chain
}
"""

from pysondb import db

class User(object):
    username: str
    password: str
    def __init__(self, username: str, password: str, private_key, local_ledger: block.BlockChain):
        self.username = username
        self.password = password
        self.private_key = private_key
        self.local_ledger = local_ledger # Make this a struct its fine

    # @staticmethod
    # def create_user(username: str, password: str) -> User:
    #     return User(username, password, "private_key", "public_key")
    
    def check_password(self, password) -> bool:
        return self.password == password
    
    def set_password(self, password) -> self:
        self.password = password
        return self
        ## Update JSON
        
    def set_username(self, username) -> None:
        self.username = username
        ## Update JSON

# class User:
#     def __init__(self, file_path):
#         self.db = db.getDb(file_path)
    
#     def create_user(self, username: str, password: str, public_key, private_key, local_ledger=None): #use None for ledger
#         self.db.add({"username": username, "password": password, })
        
#     def get_user(self, username):
#         return self.db.getBy({"username": username})

#     def check_password(self, username, password):
#         user = self.get_user(username)
#         return user.password == password

#     def update_user(self, username):
        

def create_user(username: str, password: str) -> User: #return boolean true for correctly made user and false for incorrectly made user
    private_key = sha256(base58.b58encode(str(username).encode())).hexdigest()
    public_key = str(sha256(sha256(private_key.encode()).hexdigest().encode()).hexdigest())
    #public_key_hash = str(sha256(public_key.encode()).hexdigest()) # Daniel can you pip hashlib
    return User(username, password, public_key, private_key)

def get_user(username: str): 
    json.loads(CONST_USER_JSON)
    return User(username, password, public_key, private_key, local_ledger)

def save_user(user):
    # Save user stuff
    pass

def modify_username(username: str, password: str, new_username: str) -> bool:
    user = get_user(username, password)
    user.username = new_username
    save_user(user)
    return True

def modify_password(username: str, old_pass: str, new_pass: str) -> bool:
    user = get_user(username, old_pass)
    user.password = new_pass
    save_user(user)

def delete_user(username: str) -> bool:
    pass

def login(username: str, password: str) -> User: # -> User: #this is the same prcoess as get_user?
    pass
    
def add_to_local_ledger(username: str) -> bool: # Adding local transactions to the local ledger
    pass

