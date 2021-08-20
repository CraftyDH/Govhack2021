from hashlib import sha256
#, base58
import math
import random
import time # Look at the bottom of your file please @Jamie
import itertools

#can we split this file into multiple. like one for server and make calls into a deeper file for blockchain
#yes

class Block:
	def __init__(self, index, transactions, timestamp, previousHash, nonce=0):
		# values needed for blockheader
			self.index = index
			self.transactions = transactions
			self.timestamp = timestamp
			self.previousHash = previousHash
			self.nonce = nonce

	def computeHash(self):
	# Construct block header in order to hash it
		self.trans = ''
		for x in self.transactions:
			self.trans += x
			blockHeader = self.previousHash + self.trans + str(self.timestamp) + str(self.nonce)
		
		return sha256(blockHeader.encode()).hexdigest()

class ChainList:
	def __init__(self, block, next=None):
		self.block = block
		self.next = next
	def iterator(self): #returns iterator for iterating over chain list, use with for loop to iterate over blockchain (this is very ugly but I don't care)
		if self.next == None: return [self.block]
		return [self.block] + self.next.iterator()
		
"""
chain {
    next varchar(1000) NULL, -- chain
    current varchar(1000) -- block
}
"""
# blockchain = Blockchain()
class Blockchain: #NOTE: DO NOT OVERRIDE __DICT__
	def __init__(self):
		self.unconfirmedTransactions = []
		self.chain = [] #replace with chainlist?
		self.difficulty = 2
		self.createGenisis()

	def createGenisis(self):
		block = Block(0, [], time.time_ns(), "0")
		block.hash = block.computeHash()
		self.chain.append(block)
		return 1
	
	def lastBlock(self):
		return self.chain[-1]

	def getBlock(self, index):
		return self.chain[index]

	def proofOfWork(self, block):
		print("POW initiated\nTarget: "+'0'*Blockchain.difficulty+"\n")
		# Hash at nonce 0
		computeHash = block.computeHash()
		# Hash nonce from 1...n (where n is amount of hashes to get target hash)
		while not computeHash.startswith('0'*Blockchain.difficulty):
			block.nonce += 1
			computeHash = block.computeHash()
			print("Nonce: "+str(block.nonce)+"\nHash: "+str(computeHash)+"\n========")
		return computeHash

	def addBlock(self, block, proof):
		previousHash = self.lastBlock.hash
		if previousHash != block.previousHash:
			return False
		if not self.isValidProof(block, proof):
			return False

		# we want this to only take the fisrt 50 elements, where the transactions have been sorted by amount
		self.unconfirmedTransactions = self.unconfirmedTransactions[50:]

		block.hash = proof
		self.chain.append(block)
		return 1

	def isValidProof(self, block, block_hash):
		return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())


	def mine(self):
		if not self.unconfirmedTransactions:
			print("ERROR: No transactions to mine")
			return False
		lastBlock = self.lastBlock
		new_block = Block(index=lastBlock.index + 1,
		
							# we want this to only take the fisrt 50 elements, where the transactions have been sorted by amount
							transactions=self.unconfirmedTransactions[:50],

							timestamp=time.time_ns(),
							previous_hash=lastBlock.hash)
		proof = self.proofOfWork(new_block)
		self.add_block(new_block, proof)
		return new_block.index

blockchain = Blockchain()
