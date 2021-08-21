from aiohttp import web
import json

import block
b = block.blockchain
import transaction as t
from safe_json import safe_str
import users

routes = web.RouteTableDef()

routes.static('/static', 'website/static')
routes.static('/dashboard', 'website/dashboard')

@routes.get('/')
async def root(request):
    with open("website/index.html") as f:
        return web.Response(
            text=f.read(),
            content_type = "text/html"
        )

@routes.get('/anim.html')
async def anim(request):
    with open("website/anim.html") as f:
        return web.Response(
            text=f.read(),
            content_type = "text/html"
        )

@routes.get('/login')
async def login(request):
    with open("website/login.html") as f:
        return web.Response(
            text=f.read(),
            content_type = "text/html"
        )

@routes.get('/chain')
async def chain(request):
    if b == None: return web.Response(text=safe_str({"status": "block does not exist"}))
    ret_json = safe_str({"status": "success", "blockchain": b})
    return web.Response(text=ret_json, content_type="application/json")

@routes.get('/block/{index}')
async def block(request):
    index = request.match_info["index"]
    try:
        int_index = int(index)
        block = b.get_block(int_index)
        ret_json = safe_str({"status": "success", "block": block})
        return web.Response(text=ret_json, content_type = "application/json")
    except ValueError:
        return web.json_response({"status": "failed block request"})

@routes.get('/mine')
async def mine(request):
    ret = b.mine()
    ret_json = safe_str(ret)
    return web.Response(text=ret_json, content_type="application/json")

@routes.post('/login')
async def account(request):
    data = await request.post()
    user = users.login(data["username"], data["password"])
    # user.balance = b.get_user_worth(data["username"])
    return web.json_response(user)

@routes.post('/modify_password')
async def modify_password(request):
    data = await request.post()
    modified = users.modify_password(data["username"], data["oldpass"], data["newpass"])
    return web.json_response(modified)

@routes.post('/create_account')
async def create_account(request):
    data = await request.post()
    created = users.create_user(data["username"], data["password"])
    return web.json_response(created)

@routes.post('/delete_account')
async def delete_account(request):
    data = await request.post()
    deleted = users.delete_user(data["username"], data["password"])
    return web.json_response(deleted)

@routes.post('/create_transaction')
async def create_transaction(request):
    data = await request.post()

    if not data['recipient_public_key']: # If the passed recipient key is empty then it won't be in the database
        ret_json = safe_str({"status": "invalid recipient public key"}) 
        return web.Response(text=ret_json, content_type="application/json")
    if data["amount"]: # Here we check if the amount parameter is given as none we just pass it as 0 to the transaction class
        trans = t.create_transaction_no_validation(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    else: # If data['amount'] == null/None 
        trans = t.create_transaction_no_validation(data["sender_private_key"], data["recipient_public_key"], 0)
    b.mine_transactions() # running here
    ret_json = safe_str({"status": "success", "transaction": trans})
    return web.Response(text=ret_json, content_type="application/json")

@routes.post('/get_user_transactions')
async def get_transaction(request):
    data = await request.post()
    username = data["username"]
    ret_trans = [n for block in b.chain for n in block.transactions]
    ret_trans = list(filter(lambda n: n.sender["username"] == username or n.recipient["username"] == username, ret_trans))
    ret_json = safe_str({"status": "success", "transactions": ret_trans})
    return web.Response(text=ret_json, content_type="application/json")

@routes.get('/{username}/get_transactions_data')
async def get_transaction_data(request):
    username = request.match_info["username"]
    ret_trans = [n for block in b.chain for n in block.transactions]
    ret_trans = list(filter(lambda n: (n.sender["username"] == username) != (n.recipient["username"] == username), ret_trans))
    ret_trans = [[n.sender["username"], n.recipient["username"], n.amount, n.hash, round(n.tax,2), n.time] for n in ret_trans]
    ret_json = safe_str({"data": ret_trans})
    return web.Response(text=ret_json, content_type="application/json")

@routes.post('/get_unsigned_transactions')
async def get_unsigned_transactions(request):
    try:
        data = await request.post()
        username = data["username"]
        trans = b.get_unsigned_transactions(username)
        ret_json = safe_str({"status": "success", "transactions": trans})
    except: # DANGER DANGER DANGER
        ret_json = safe_str({"status": "failed getting unsigned user transactions"})
    finally:
        return web.Response(text=ret_json, content_type="application/json")


@routes.post('/get_balance')
async def get_balance(request):
    username = (await request.post())["username"]
    user_worth = b.get_user_worth(username)
    if (user_worth):
        ret_json = safe_str({
            "status": "success",
            "balance": user_worth
        })
        return web.Response(text=ret_json, content_type="application/json")

    return {
        "status" : "Failed. User not found / Balance not found"
    }

@routes.post('/get_usernames')
async def get_usernames(request):
    usernames = users.get_usernames()
    if usernames == False:
        return web.json_response({"status": "failed getting usernames"})
    ret_json = safe_str({"status": "success", "usernames": usernames})
    return web.Response(text=ret_json, content_type="application/json")


# parameters: {
#   "date": "Sun Jun 20 23:21:05 1993",
#   "senders": [
#     [*Pubkey0*, amount_contributed], ...
#   ],
#   "recipients": [
#     [*Pubkey1*, amount_contributed], ...
#   ],
#   "condition_type": "time" | "withdrawl" | "stop_limit", (one of these 3)
#   "condition_argument": "Sun Jun 20 23:21:05 1993" | ("salary" | "lumpsum") | "6969"
# }

@routes.post("/create_smart_contract")
async def post_smart_contract(request):
    data = await request.post()
    print("data is " + str(data))
    #params = data["parameters"]
    if not data['start_date']:
        dates = None
    else:   
        dates = {
            "start_date": data["start_date"],
            "increment" : data["increment"],
            "end_date" : data["end_date"]
        }
    sender_arr = json.loads(data["sender_arr"])
    recipient_arr = json.loads(data["recipient_arr"])
    print(sender_arr, recipient_arr)
    contract =  t.create_contract(data["amount"], sender_arr, recipient_arr, int(data['limit']), dates)
    ret_json = safe_str({"status": "success", "contract": contract})
    return web.Response(text=ret_json, content_type="application/json")
    
    # return {'status': "failed creating contract"}


@routes.post('/get_all_contracts')
async def get_all_contracts(request): # add error checking
    contracts = b.get_all_contracts()
    if contracts:
        ret_json = safe_str({"status": "success", "contracts": contracts})
        return web.Response(text=ret_json, content_type="application/json")
    return web.Response(text={
        "status": "failed getting contracts"
    })

@routes.post('/sign_contract')
async def sign_transaction(request):
    data = await request.post()    
    ret_json = safe_str(sign_contract(data["contract_id"], data["private_key"]))
    return web.Response(text=ret_json, content_type="application/json")


app = web.Application()
app.add_routes(routes)
web.run_app(app)
