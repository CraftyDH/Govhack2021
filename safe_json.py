#this file might be unecersarry but it gives me peace of mind of mind

import json
from block import *
def is_object(o):
    return hasattr(o, '__dict__')
    
def convert_data(data):
    if is_object(data): return convert_data(data.__dict__)
    elif type(data) is dict: return {k: convert_data(v) for k, v in data.items()}
    elif type(data) is list or type(data) is tuple: return [convert_data(n) for n in data]
    else: return data

def safe_str(data):
    d = convert_data(data)
    return json.dumps(d)

def safe_dump(data, file):
    return json.dump(convert_data(data), file)

# def load_blockchain(json_in) -> Blockchain:
#     b = Blockchain()
#     b.unconfirmed_transactions = [transaction.Transaction.load_json(n) for n in json_in["unconfirmed_transactions"]]
#     b.unconfirmed_contracts = [transaction.Smart_Contract.load_json(n) for n in json_in["unconfirmed_contracts"]]
#     b.chain = load_chainlist(json_in["chain"])
#     b.contracts_chain = load_chainlist(json_in["contracts_chain"]) 
#     b.difficulty = json_in["difficulty"]
#     b.tax_rate = json_in["tax_rate"]
#     b.unsigned_contracts = [transaction.Smart_Contract.load_json(n) for n in json_in["unsigned_contracts"]] #load json recursive here
#     return b

# def load_json(self, json_dict):
#     if json_dict["next"] == None:
#         ret = ChainList(Block.load_json(json_dict["block"]), None)
#     else:
#         ret = ChainList(Block.load_json(json_dict["block"]), ChainList.load_json(json_dict["next"]))

# 	def load_json(self, json_dict):
# 		ret = 