from aiohttp import web
import json

import block
b = block.blockchain
import transaction
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
    return web.Response(text=ret_json)

@routes.get('/block/{index}')
async def block(request):
    index = request.match_info["index"]
    try:
        int_index = int(index)
        block = b.get_block(int_index)
        ret_json = safe_str({"status": "success", "block": block})
        return web.Response(
            text=ret_json,
            content_type = "application/json"
        )
    except ValueError:
        return web.json_response({"status": "failed block request"})

@routes.get('/mine')
async def mine(request):
    ret = b.mine()
    ret_json = safe_str(ret)
    return web.Response(text=ret_json, context_type="application/json")

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
    trans = transaction.create_transaction(data["sender_private_key"], data["recipient_public_key"], data["amount"])
    if trans["status"] != "success":
        return web.json_response(trans)
    ret_json = safe_str({"status": "success", "transaction": trans})
    return web.json_response(trans)

@routes.post('/get_local_transactions')
async def get_transaction():
    pass

app = web.Application()
app.add_routes(routes)
web.run_app(app)
