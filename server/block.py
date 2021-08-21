import hashing
#, base58
import math
import random
import time # Look at the bottom of your file please @Jamie
import itertools

#can we split this file into multiple. like one for server and make calls into a deeper file for blockchain
#yes

#! OI USE snake_case NOT CamelCase JAMIE

class Block:
	def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
		# values needed for blockheader
			self.index = index
			self.transactions = transactions
			self.timestamp = timestamp
			self.previous_hash = previous_hash
			self.nonce = nonce

	def compute_hash(self):
	# Construct block header in order to hash it
		self.trans = ''
		block_header = ""
		for x in self.transactions:
			self.trans += x
			block_header = self.previous_hash + self.trans + str(self.timestamp) + str(self.nonce)
		return hashing.hash(block_header)

class ChainList:
	def __init__(self, block, next=None):
		self.block = block
		self.next = next
	def iterator(self): #returns iterator for iterating over chain list, use with for loop to iterate over blockchain (this is very ugly but I don't care)
		if self.next == None: return [self.block]
		return [self.block] + self.next.iterator()
	def index_into(self, index):
		if index < 0: raise Exception("passed index less than 0") #(add negative indexing later?)
		elif index == 0: return self.block
		else: return self.next.index_into(index-1)
	def last_block(self):
		if self.next == None: return self.block
		else: return self.next.last_block()
	def append(self, block):
		if self.next == None:
			nextt = ChainList(block)
			self.next = nextt
			return nextt
		else: return self.next.append(block)
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
		raise Exception("pop at not implemented yet") #i can't be bothered and it shouldn't come up right?

# blockchain = Blockchain()
class Blockchain: 
	def __init__(self):
		self.unconfirmed_transactions = []
		self.chain = None
		self.difficulty = 2
		self.create_genisis()

	def create_genisis(self):
		block = Block(0, [], time.time_ns(), "0")
		block.hash = block.compute_hash()
		self.chain = ChainList(block)
		return 1

	@property
	def last_block(self):
		return self.chain.last_block()

	def get_block(self, index):
		return self.chain.index_into(index)

	def proof_of_work(self, block):
		print("POW initiated\nTarget: "+'0'*Blockchain.difficulty+"\n")
		# Hash at nonce 0
		compute_hash = block.compute_hash()
		# Hash nonce from 1...n (where n is amount of hashes to get target hash)
		while not compute_hash.startswith('0'*Blockchain.difficulty):
			block.nonce += 1
			compute_hash = block.compute_hash()
			print("Nonce: "+str(block.nonce)+"\nHash: "+str(compute_hash)+"\n========")
		return compute_hash

	def add_block(self, block, proof):
		previous_hash = self.last_block.hash
		if previous_hash != block.previous_hash:
			return False
		if not self.is_valid_proof(block, proof):
			return False

		# we want this to only take the fisrt 50 elements, where the transactions have been sorted by amount
		self.unconfirmed_transactions = self.unconfirmed_transactions[50:]

		block.hash = proof
		self.chain.append(block)
		return 1

	def is_valid_proof(self, block, block_hash):
		return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())


	def mine(self):
		if not self.unconfirmed_transactions:
			print("ERROR: No transactions to mine")
			return False
		lastBlock = self.last_block
		new_block = Block(index=last_block.index + 1,
		
							# we want this to only take the fisrt 50 elements, where the transactions have been sorted by amount
							transactions=self.unconfirmed_transactions[:50],

							timestamp=time.time_ns(),
							previous_hash=last_block.hash)
		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		return new_block.index

blockchain = Blockchain()
