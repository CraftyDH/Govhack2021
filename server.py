from aiohttp import web
import json
import os
import block
b = block.blockchain
import transaction as t
from safe_json import safe_str
import users, update_net_worths
import csv
import uuid

update_net_worths.start_thread()

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


@routes.post('/login')
async def account(request):
    data = await request.post()
    user = users.login(data["username"], data["password"])
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
        trans = t.create_transaction(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    else: # If data['amount'] == null/None 
        trans = t.create_transaction(data["sender_private_key"], data["recipient_public_key"], 0)
    
    if trans["status"] != "success":
        return web.json_response(trans)
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
    ret_trans = [[n.sender["username"], n.recipient["username"], n.amount, str(uuid.uuid4()), round(n.tax,2), n.time] for n in ret_trans]
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
    user_worth = users.get_user_worth(username)
    if (user_worth):
        ret_json = safe_str({
            "status": "success",
            "balance": user_worth
        })
        return web.Response(text=ret_json, content_type="application/json")

    return {
        "status" : "Failed. User not found / Balance not found"
    }

@routes.get('/get_usernames')
async def get_usernames(request):
    usernames = users.get_usernames()
    public_keys = users.get_public_keys()
    if not usernames:
        return web.json_response({"status": "failed getting usernames"})
    ret_json = safe_str({"status": "success", "usernames": usernames,'public_keys':public_keys})
    return web.Response(text=ret_json, content_type="application/json")

@routes.get('/{username}/get_all_contracts/{pending}')
async def get_all_contracts(request):
    username = request.match_info["username"]
    pending = request.match_info["pending"]
    
    # pending
    # active
    contracts = t.get_all_contracts(username, pending)
    print("contracts = " + str([n.__dict__.keys() for n in contracts]))
    [print(n.senders) for n in contracts]
    ret_json = [{
        "ID": n.id,
        "Senders": ", ".join(map(lambda i: users.find_user_private_key(i)["username"], n.senders)), 
        "Recipients": ", ".join(map(lambda i: users.find_user_public_key(i)["username"], n.recipients)),
        "Amount": n.amount,
        "Increment": (n.increment if isinstance(n, t.Time_Contract) else "N/A"), #isinstance()
        "Limit": n.limit,
        "StartDate": (n.start_date if isinstance(n, t.Time_Contract) else "N/A"),
        'EndDate': (n.end_date if isinstance(n, t.Time_Contract) else "N/A"),
        'Status': n.status
    } for n in contracts]
    """columns: [
        {title: "id" },
        { title: "Senders" },
        { title: "Recipients" },
        { title: "Amount" },
        { title: "Increment" },
        { title: "Limit" },
        { title: "Start Date" },
        { title: "End Date" },
        { title: "Status" },
    ], """
    ret_json = safe_str({"data": ret_json})
    return web.Response(text=ret_json, content_type="application/json")

@routes.post("/create_smart_contract")
async def post_smart_contract(request):
    data = await request.post()
    print("data is " + str(data))
    if data['limit'] == 0:
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
    contract = t.create_contract(data["amount"], sender_arr, recipient_arr, int(data['limit']), dates)
    ret_json = safe_str({"status": "success", "contract": contract})
    return web.Response(text=ret_json, content_type="application/json")
    
    # return {'status': "failed creating contract"}

"""
@routes.post('/{user}/get_all_contracts/{pending}')
async def get_all_contracts(request): # add error checking
    contracts = b.get_all_contracts(request.match_info["user"])

    if request.match_info["pending"] == "pending":
        ##
        pass
    elif request.match_info["pending"] == "active":
        ##
        pass

    if contracts:
        ret_json = safe_str({"status": "success", "data": contracts})
        return web.Response(text=ret_json, content_type="application/json")
    return web.Response(text={
        "status": "failed getting contracts"
    })
"""

@routes.post('/sign_contract')
async def sign_transaction(request):
    data = await request.post()    
    ret_json = safe_str(t.sign_contract(data["contract_id"], data["private_key"]))
    return web.Response(text=ret_json, content_type="application/json")

@routes.post('/decline_contract')
async def decline_transaction(request):
    data = await request.post()    
    ret_json = safe_str(t.decline_contract(data["contract_id"], data["private_key"]))
    return web.Response(text=ret_json, content_type="application/json")

from itertools import groupby


@routes.post('/get_group_data')
async def get_group_data(request):
    await request.post()
    f = open("data/block.csv", newline='')
    read = csv.reader(f)
    i = iter(read)
    next(i)
    lines = []
    for n in i: lines.append(n[2])
    g = groupby(lines)
    g = [len(list(v)) for k,v in g]
    return web.json_response(g)

app = web.Application()
app.add_routes(routes)

web.run_app(app, port=os.environ.get('PORT', 8080))

# import dashboard

