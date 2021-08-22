import csv
import string
from random_username.generate import generate_username
from random import *
import transaction
import block
import users as u
import json

csv_file = "data/block.csv"
#* make sure to generate only one per hash

CONST_USERS = {}
def generate_user(public_hash):
    if (public_hash in CONST_USERS):
        return CONST_USERS[public_hash]
    else:
        username = generate_username(1)
        password =  "".join(choice(string.ascii_letters + string.punctuation  + string.digits) for x in range(randint(8, 250)))
        newuser = u.create_user(username, password, public_hash)['user']
        CONST_USERS[public_hash] = newuser
        return newuser

# block_id, block_hash, block_timestamp, difficulty, transaction_hash, transaction_timestamp, sender, receiver, amount, tax

CONST_BLOCKS = {} #blockid: block

with open(csv_file, newline='') as f:
    read = csv.reader(f)
    for row in read:
        #make CONST_USERS
        sender = generate_user(row[6])
        reciever = generate_user(row[7])
        #generate transaction
        trans = transaction.create_transaction_no_validation(sender, reciever, row[8])
        if row[0] in CONST_BLOCKS:
            #transaction already exists
            CONST_BLOCKS[row[0]].transactions.append(trans)
        else:
            #create block
            CONST_BLOCKS[row[0]] = block.Block(-1, [trans], row[5], -1, row[3])
    b = block.blockchain
    CONST_BLOCKS_list = [v for k,v in CONST_BLOCKS.items()]
    for n in sorted(CONST_BLOCKS_list, key=(lambda n: n.timestamp)): #maybe reversed? (probably not)
        proof = b.proof_of_work(n)
        b.add_block(n, proof)
    i = iter(b)
    prev = next(i)
    prev.compute_hash()
    for n in i:
        n.compute_hash()
        n.prev_hash = prev.hash
        prev = n
    
    users = u.load_user_json() 
    for _,user in CONST_USERS.items():
        users.append(user)
    u.modify_json(users)


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
#index set to negative one until pushed to blockchain 