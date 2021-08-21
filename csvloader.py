import csv
import string
from random_username.generator import generate_username
from random import *
import transaction
import block

csv_file = "D:/govhackdata/block.csv"
    
    # newuser =  {
    #     "username": username,
    #     "password": password,
    #     "public_key": public_key,
    #     "private_key": private_key,
    # }
#* make sure to generate only one per hash
def generate_user(public_hash):
    return {
        "username" : generate_user(1),
        "passsword": "".join(choice(string.ascii_letters + string.punctuation + string.digits) for x in range(randint(8, 250)))
        "public_key": public_hash,
        "private_key": ""  #generate this
    }

# block_id, block_hash, block_timestamp, difficulty, transaction_hash, transaction_timestamp, sender, receiver, amount, tax

blocks = {} #blockid: block

with open(csv_file, newline='') as f:
    read = csv.csvReader(f)
    next(read)
    for row in read:
        #block_id: 4728042
        #block_hash: 0x2ab52915da4a7bece7fe897c5e9cf0d93a40f42c02e4170438975e8f6205728f
        #block_timestamp: 2017-12-14 06:51:19
        #difficulty: 1637664087773349 (nonce)
        #transaction_hash: 0x838d179a58aaa73127bffb480b49e3d286eb7b73b8149f632e1e9f05042ed27f
        #transaction_timestamp: 2017-12-13 23:19:28
        #sender: 0x03c81b5807b7a11f3be3d364d14dfb7dd818c972
        #receiver: 0x1a0b09c4caaba8a5da6ca6c26a3fcc16e05d24d8
        #amount: 37.142631825483598
        #tax: 0.00067221
        #block == index, transactions, timestamp, previous_hash, nonce=0
        #index set to negative one until pushed to blockchain #! TALK TO JAMIE
        
        #make users
        sender = generate_user(row[6])
        reciever = generate_user(row[7])
        
        #generate transaction
        #! talk to JAMIE
        trans = transaction.create_transaction_no_validation(sender, reciever, row[8])
        
        if row[0] in blocks:
            #transaction already exists
            pass
        else:
            #create block
            pass
