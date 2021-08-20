from aiohttp import web
import json

import block
import users
import transaction

index = open("../website/index.html")
routes = web.RouteTableDef()

#lot of repeated code in routes, fix later
    #add deugging and tests later

@routes.get('/chain')
async def chain(request):
    bc = block.blockchain
    ret_json = json.dumps(bc.__dict__)
    return web.Response(text=ret_json)

@routes.get('/block/{index}')
async def block(request):
    index = request.match_info("index")
    block = block.get_block(index)
    ret_json = json.dumps(block.__dict__)
    return web.Response(text=ret_json)

@routes.get('/mine')
async def mine(request):
    block.mine()
    ret_json = json.dumps(block.__dict__)
    return web.Response(text=ret_json)

@routes.post('/account')
async def account(request):
    data = request.post()
    user = users.login(data["username"], data["password"])
    ret_json = json.dumps(user.__dict__)
    return web.Response(text=ret_json)

@routes.post('/modify_username')
async def modify_username(request):
    data = request.post()
    modified = users.modify_username(data["oldusername"], data["newusername"], data["newpass"])
    ret_json = json.dumps(modified)
    return web.Response(text=ret_json)

@routes.post('/modify_password')
async def modify_password(request):
    data = request.post()
    modified = users.modify_password(data["username"], data["oldpass"], data["newpass"])
    ret_json = json.dumps(modified)
    return web.Response(text=ret_json)

@routes.post('/create_account')
async def create_account(request):
    data = request.post()
    created = users.create_user(data["username"], data["password"])
    ret_json = json.dumps(created)
    return web.Response(text=ret_json)

@routes.post('/delete_account')
async def delete_account(request):
    data = request.post()
    deleted = users.delete_user(data["username"], data["password"])
    ret_json = json.dumps(deleted) #might be unecersarry, although it's probably safer (deleted output is boolean)
    return web.Response(text=ret_json)

@routes.post('/create_transaction')
async def create_transaction(request):
    data = request.post()
    trans = transaction.create_transaction(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    ret_json = json.dumps(trans)
    return web.Response(text=ret_json)

app = web.Application()
app.add_routes(routes)
web.run_app(app)