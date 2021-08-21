#, base58
import math
import random
import time # Look at the bottom of your file please @Jamie
import itertools
from hashlib import sha256
from typing import Container

CONST_TRANSACTS_IN_BLOCK_NUM = 10

class Block:
	def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
		# values needed for blockheader
			self.index = index
			self.transactions = transactions #when used in chainlist it stores contracts not transactions (load json recursive)
			self.timestamp = timestamp
			self.previous_hash = previous_hash
			self.nonce = nonce
			self.hash = None #! here jamie
	def compute_hash(self): # Construct block header in order to hash it
		self.trans = ''
		block_header = ""
		#self.trans = sum([str(x.hash) for x in self.transactions])
		for x in self.transactions:
		 	self.trans += str(x.hash) #transactions is a list of strings?
		block_header = self.previous_hash + self.trans + str(self.timestamp) + str(self.nonce)
		self.hash = sha256(block_header.encode()).hexdigest()
		return self.hash
	def __str__(self):
		return "Block(" + ",".join(map(str, [self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce])) + ")"

class ChainList:
	def __init__(self, block, next=None):
		self.block = block #load json recursive here
		self.next = next #load json recursive here
	def iterator(self): #returns iterator for iterating over chain list, use with for loop to iterate over blockchain (this is very ugly but I don't care)
		if self.next == None: return [self.block]
		return [self.block] + self.next.iterator()
	def __iter__(self):
		return iter(self.iterator())
	def index_into(self, index):
		if index < 0: raise Exception("passed index less than 0") #(add negative indexing later?)
		elif index == 0: return self.block
		else: return self.next.index_into(index-1)
	def last_block(self):
		if self.next == None: return self.block
		else: return self.next.last_block()
	def append(self, block, index):
		if self.next == None:
			nextt = ChainList(block)
			block.index = index
			self.next = nextt
			return nextt
		else: return self.next.append(block, index+1)
	def insert_at(self, block, index):
		if index < 0: raise Exception("negative index passed)") # (add negative indexing later?
		elif index == 0:
			new = ChainList(block, self.next) #weird referencing here, might cause bugs
			self.next = new #hopefully this works but it might not
			return new
		elif self.next == None: raise Exception("tried to insert longer than length of chain list")
		else: return self.next.insert_at(self, block, index-1)
	def length(self):
		return sum((1 for n in self.iterator())) #not the best not the worst
	def pop(self):
		if self.next == None: raise Exception("tried to pop from single element list") #this error is on my part due to bad oo. shouldn't matter?
		elif self.next.next == None:
			out = self.next 
			self.next = None #weird referencing, might cause errors (potentially have to write clone routine)
			return out
		else:
			return self.next.pop()
	def pop_at(self, index):
		raise Exception("pop at not implemented yet") #I can't be bothered and it shouldn't come up right?
	def __str__(self):
		return "[" + ", ".join(map(str, iter(self))) + "]" # bit unecersarry, as it returns a list anyway lol (but theoretical issues whatever)

class Blockchain: 
	def __init__(self):
		self.unconfirmed_transactions = []
		self.unconfirmed_contracts = []
		self.chain = None #ChainList
		self.contracts_chain = None #ChainList
		self.difficulty = 2
		self.create_genisis()
		self.tax_rate = .05
		self.unsigned_contracts = []
	def add_SC(self, SC):
		self.unsigned_contracts.append(SC)
		return {"status":"Smart Contract submitted to be signed."}

	def get_unsigned_transactions(self, username):
		arr = []
		for x in self.unsigned_contracts:
			if x.participants["username"] == username:
				arr.append(x)
		return arr

# to be called as get_SC_participants(SC, "senders")
# or get_SC_participants(SC, "recipients")
#Hey Jamie, could we have a method get_unsigned_transactions(self, username), yea

	def get_SC_participants(self, SC):
		return {"senders":SC.senderArr, "recipients": SC.recipientArr}

	# def sign_contract(self, ...):
	# 	pass

	def __iter__(self):
		return iter(self.chain)

	def create_genisis(self):
		block = Block(0, [], time.time_ns(), "0")
		block.hash = block.compute_hash()
		self.chain = ChainList(block)
		b2 = Block(0, [], time.time_ns(), "0")
		b2.hash = b2.compute_hash()
		self.contracts_chain = ChainList(b2)
		return 1

	@property
	def last_block(self):
		return self.chain.last_block()

	@property
	def last_contract_block(self):
		return self.contracts_chain.last_block()

	def get_block(self, index):
		return self.chain.index_into(index)

	def get_block(self, index):
		return self.contracts_chain.index_into(index)

	def proof_of_work(self, block):
		print("POW initiated\nTarget: "+'0'*self.difficulty+"\n")
		# Hash at nonce 0
		compute_hash = block.compute_hash()
		# Hash nonce from 1...n (where n is amount of hashes to get target hash)
		while not compute_hash.startswith('0'*self.difficulty):
			block.nonce += 1
			compute_hash = block.compute_hash()
			print("Nonce: "+str(block.nonce)+"\nHash: "+str(compute_hash)+"\n"+"="*(len(str(compute_hash))))
		return compute_hash

	def add_block(self, block, proof):
		#auto called here
		previous_hash = self.last_block.hash
		if previous_hash != block.previous_hash:
			return False
		if not self.is_valid_proof(block, proof):
			return False
		self.unconfirmed_transactions = self.unconfirmed_transactions[50:]
		block.hash = proof
		self.chain.append(block, 0)
		return True

	def add_contracts_block(self, block, proof):
		#auto called here
		previous_hash = self.last_contract_block.hash
		if previous_hash != block.previous_hash:
			return False
		if not self.is_valid_proof(block, proof):
			return False
		self.unconfirmed_contracts = self.unconfirmed_contracts[CONST_TRANSACTS_IN_BLOCK_NUM:]
		block.hash = proof
		self.contracts_chain.append(block, 0)
		
		return True

	def is_valid_proof(self, block, block_hash):
		return (block_hash.startswith('0' * self.difficulty) and block_hash == block.compute_hash())

	def mine_transactions(self):
		print("mine transactions called")
		if self.unconfirmed_transactions == []: 
			return {"status":"No transactions to mine"}
		last_block = self.last_block
		new_block = Block(index=last_block.index + 1,
			# we want this to only take the first CONST_TRANSACTS_IN_BLOCK_NUM elements, where the transactions have been sorted by amount
			transactions=self.unconfirmed_transactions[:CONST_TRANSACTS_IN_BLOCK_NUM], 
			timestamp=time.time_ns(),
			previous_hash=self.last_block.hash
		)
		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		return {"status": "success"}

	def mine_contracts(self):
		if self.unconfirmed_contracts == []: return {"status":"No contracts to mine"}
		last_block = self.last_contract_block
		new_block = Block( 
			index=last_block.index + 1,			
			transactions=self.unconfirmed_contracts[:CONST_TRANSACTS_IN_BLOCK_NUM], # we want this to only take the first CONST_TRANSACTS_IN_BLOCK_NUM elements, where the transactions have been sorted by amount
			timestamp=time.time_ns(),
			previous_hash=last_block.hash
		)
		for n in self.unconfirmed_contracts:
			n.status = "active"
		proof = self.proof_of_work(new_block)
		self.add_contracts_block(new_block, proof)
		return {"status": "success"}

	def add_transaction(self, trans):
		self.unconfirmed_transactions.append(trans)
		return #! NOT RETURNING ANYTHING

	def add_contract(self, contract):
		self.unconfirmed_contracts.append(contract)
		self.mine_contracts()
		return {"status": "Contract mining called"}

blockchain = Blockchain() #! POTENTIAL ERROR WITH EMPTY FILE. CHECK LATer

BLOCK_JSON_FILE = "../json/block.json"
def store_chain():
 	safe_dump(blockchain, BLOCK_JSON_FILE)

def load_chain():
 	json_in = json.loads(open(BLOCK_JSON_FILE, "r").read())
 	return Blockchain.load_json(json_in)