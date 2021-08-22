import users as u, threading as th, time

CONST_SLEEP = 5 * 60

def start_thread():
    t = th.Thread(target=loop)

def loop():
    while True: # So every 5 minutes it goes through all the users and updates their net worth based on transactions and smart contracts
        time.sleep(CONST_SLEEP)
        users = u.load_user_json()
        new_users = [u.get_user_worth(user) for user in users]
        u.modify_json(new_users, u.CONST_USER_JSON)

    
"""

 - make bank objects alongside hedgefund
    - we should stick to only one hedgefund?

 - contract validation 
    - doing now Jonte

  - contract status
   ^pending, signed or declined
    - what?

 - when a new user is created, we need to give it a transaction of a starting balance
    - Jonte is doing this one
    - after making admin account add that address to users.py
    - done
"""


# cmartcontract.status = "fulfilled"