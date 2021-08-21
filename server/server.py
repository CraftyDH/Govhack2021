from aiohttp import web
import json

#import block
#b = block.blockchain
#import transaction
from safe_json import safe_str
import users

routes = web.RouteTableDef()

"""
@routes.get('/chain')
async def chain(request):
    bc = b
    ret_json = safe_str(bc)
    return web.Response(text=ret_json)

@routes.get('/block/{index}')
async def block(request):
    index = request.match_info["index"]
    # block = b.get_block(index)
    ret_json = safe_str(block)
    return web.Response(text=ret_json)

@routes.get('/mine')
async def mine(request):
    # ret = b.mine()
    ret_json = safe_str(ret)
    return web.Response(text=ret_json)
"""
@routes.post('/account')
async def account(request):
    data = await request.post()
    user = users.login(data["username"], data["password"])
    ret_json = safe_str(user)
    return web.Response(text=ret_json)

@routes.post('/modify_username')
async def modify_username(request):
    data = await request.post()
    modified = users.modify_username(data["oldusername"], data["newusername"], data["password"])
    ret_json = safe_str(modified)
    return web.Response(text=ret_json)

@routes.post('/modify_password')
async def modify_password(request):
    data = await request.post()
    modified = users.modify_password(data["username"], data["oldpass"], data["newpass"])
    ret_json = safe_str(modified)
    return web.Response(text=ret_json)

@routes.post('/create_account')
async def create_account(request):
    data = await request.post()
    created = users.create_user(data["username"], data["password"])
    ret_json = safe_str(created)
    return web.Response(text=ret_json)

@routes.post('/delete_account')
async def delete_account(request):
    data = await request.post()
    deleted = users.delete_user(data["username"], data["password"])
    ret_json = safe_str(deleted)
    return web.Response(text=ret_json)

"""
@routes.post('/create_transaction')
async def create_transaction(request):
    data =await request.post()
    trans = transaction.create_transaction(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    ret_json = safe_str(trans)
    return web.Response(text=ret_json)
"""

app = web.Application()
app.add_routes(routes)
web.run_app(app)
