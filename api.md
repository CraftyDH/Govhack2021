# Create Account
POST /create_account
HTTP_FORM Params
username: String no space, at least 5 character (in case space might becomes %20 when url encoding)
password: String 8-255 characters

return:
## Success
{
  "status": "success",
  "user": {
    "username": "jonte2",
    "password": "password",
    "public_key": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
    "private_key": "df091bfc73489f2c86f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6",
    "local_ledger": []
  }
}
## Failure
{"status": "invalid username"}
{"status": "invalid password"}
{"status": "user exists"} // Already exists

## Modify Password
POST /modify_password
HTTP_FORM Params
username: String
oldpass: String
newpass: String

## Success
{"status": "succuss"}

## Failures
{"status": "incorrect password"}
{"status": "no user found"}

# Delete User
POST /delete_user
HTTP_FORM Params
username: String
password: String

## Success
{"status": "succuss"}

## Failures
{"status": "incorrect password"}
{"status": "no user found"}

# Login
POST /login
HTTP_FORM Params
username: String
password: String

## Success
{
  "status": "success",
  "user": {
    "username": "jonte2",
    "password": "password",
    "public_key": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
    "private_key": "df091bfc73489f2c86f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6",
    "local_ledger": []
  }
}
## Failure
{"status": "user deleted"}
{"status": "incorrect password"}
{"status": "no user found"}

# Get Blockchain
GET /chain

## Success
{
  "status": "success",
  "blockchain": {
    "chain": {
        nextblock,
        current
    },
    "unconfirmed-transactions": [{
      "sender": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
      "recipient": "f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6df091bfc73489f2c86",
      "amount": 200
    }, ...]
  }
}

## Failure
{"status": "block does not exist"}

# Get Block
GET /block/{id}

#! NOTE TRANSACTIONS WILL NOW BE PASSED AS A HASH

## Success
{
  "status": "success",
  "block": {
    "index": "15",
    "transactions":{
      "sender": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
      "recipient": "f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6df091bfc73489f2c86",
      "amount": 200,
      "hash": "f7317df47ab0ead1180d61289049da8f7b8f888153b95b58efa8ab5e4723c09f",
      "time": "Sun Jun 20 23:21:05 1993", #ascii time
      "tax": 10
    }, ...],
    "timestamp": "Sun Jun 20 23:21:05 1993", #ascii time
    "previous_hash": "f7317df47ab0ead1180d61289049da8f7b8f888153b95b58efa8ab5e4723c09f",
    "nonce": "339399"
  }
}

## Failure
{"status": "failed block request"}


## Transactions
POST /create_transaction
HTTP_FORM Params
sender_private_key: String/Int (hex key)
recipient_public_key: String/Int (hex key)
password: String

## Success
{
  "status": "success",
  "transaction": {
    "sender": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
		"recipient": "f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6df091bfc73489f2c86",
		"amount": 200,
		"hash": "f7317df47ab0ead1180d61289049da8f7b8f888153b95b58efa8ab5e4723c09f",
		"time": "Sun Jun 20 23:21:05 1993", #ascii time
    "tax": 10
  }
}

## Failure
{"status": "failed to create transaction"}


## Transactions
POST /get_user_transactions
HTTP_FORM Params
username: String

## Success
{
  "status": "success"
  "transactions": [
    "transaction": {
    "sender": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
		"recipient": "f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6df091bfc73489f2c86",
		"amount": 200,
		"hash": "f7317df47ab0ead1180d61289049da8f7b8f888153b95b58efa8ab5e4723c09f",
		"time": "Sun Jun 20 23:21:05 1993", #ascii time
    "tax": 10
    }, ...
  ]
}

## Failure
{"status": "get_user_transactions failed"}

## Unsigned Transactions
POST /get_unsigned_user_transactions
HTTP_FORM Params
username: String

## Success
{
  "status": "success" 
  "transactions": [
    "transaction": {
    "sender": "9049da8f7b8f8f7317df47ab0ead1180d612888153b95b58efa8ab5e4723c09f",
		"recipient": "f876c0edf79b72d3fc6fa0199f396d7c4eb55ea4a20ec6df091bfc73489f2c86",
		"amount": 200,
		"hash": "f7317df47ab0ead1180d61289049da8f7b8f888153b95b58efa8ab5e4723c09f",
		"time": "Sun Jun 20 23:21:05 1993", #ascii time
    "tax": 10
    }, ...
  ]
}

## Failure
{"status": "failed getting unsigned user transactions" }


## GetUserBalance
POST /get_balance
HTTP_FORM Params
username: String

## Success
{"status": "success", "balance": 999}
## Failure
{"status": "failed getting user balance"}


## GetUsernames
POST /get_usernames

## Success
{"status": "success", "usernames": [String, ...], "public_keys": [Int,...]}
## Failure
{"status": "failed getting usernames"}


## Smart Contract
POST /create_smart_contract
HTTP_FORM Params
{
  'amount': int, 
  sender_arr: String,
  recipient_arr : String, 
  'limit': '0',
  'start_date': '08/31/2021',
  'increment': '1', 
  'end_date': '09/01/2021'
}

## Success
{"status": "success", "contract": SMART_CONTRACT}

## Failure
{"status": "failed creating contract"}

## Get all contracts
POST /get_all_contracts
HTTP_FORM Params
username: String

## Success
{
  "status": "success", 
  "contracts": [{
    "date": "Sun Jun 20 23:21:05 1993",
    "senders": [
      [*Pubkey0*, amount_contributed], ...
    ],
		"recipients": [
      [*Pubkey1*, amount_contributed], ...
    ],
		"amount": 999,
		"condition_type": "time" | "withdrawl" | "stop_limit", (one of these 3)
		"condition_argument": "Sun Jun 20 23:21:05 1993" | ("salary" | "lumpsum") | "6969",
		"id": 15
  }, ...]
}

## Failure
{"status": "failed getting contracts"}

## Sign Contract
POST /sign_contract
HTTP_FORM Params
private_key: String/Int (hex key)
contract_id: Int


## Success
{
  "status": "success"
}

## Success
{"status": "success"}
## Failure
{"status": "failed signing contract"}
