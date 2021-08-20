from aiohttp import web
import json

import block as b
import users
import transaction

index = open("../website/index.html")
routes = web.RouteTableDef()

#lot of repeated code in routes, fix later
    #add deugging and tests later
    
def safe_dump(inp):
    if type(inp) is not obj: return json.dumps(inp)
    else: return json.dumps(inp.__dict__)

@routes.get('/chain')
async def chain(request):
    bc = b.blockchain
    ret_json = safe_dump(bc)
    return web.Response(text=ret_json)

@routes.get('/block/{index}')
async def block(request):
    index = request.match_info("index")
    block = b.get_block(index) # ?? #why is this confusing?
    ret_json = safe_dump(block)
    return web.Response(text=ret_json)

@routes.get('/mine')
async def mine(request):
    ret = b.mine()
    ret_json = jsafe_dump(ret)
    return web.Response(text=ret_json)

@routes.post('/account')
async def account(request):
    data = request.post()
    user = users.login(data["username"], data["password"])
    ret_json = safe_dump(user)
    return web.Response(text=ret_json)

@routes.post('/modify_username')
async def modify_username(request):
    data = request.post()
    modified = users.modify_username(data["oldusername"], data["newusername"], data["newpass"])
    ret_json = safe_dump(modified)
    return web.Response(text=ret_json)

@routes.post('/modify_password')
async def modify_password(request):
    data = request.post()
    modified = users.modify_password(data["username"], data["oldpass"], data["newpass"])
    ret_json = safe_dump(modified)
    return web.Response(text=ret_json)

@routes.post('/create_account')
async def create_account(request):
    data = request.post()
    created = users.create_user(data["username"], data["password"])
    ret_json = safe_dump(created)
    return web.Response(text=ret_json)

@routes.post('/delete_account')
async def delete_account(request):
    data = request.post()
    deleted = users.delete_user(data["username"], data["password"])
    ret_json = safe_dump(deleted)
    return web.Response(text=ret_json)

@routes.post('/create_transaction')
async def create_transaction(request):
    data = request.post()
    trans = transaction.create_transaction(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    ret_json = safe_dump(trans)
    return web.Response(text=ret_json)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
