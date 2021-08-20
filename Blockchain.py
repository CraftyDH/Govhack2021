import time
import eventlet
import threading
import logging
import concurrent.futures
import random
import json
from hashlib import sha256
import base58
import hashlib, math, sympy

class Block:
		def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
			# Initiate peripheral values needed for blockheader
				self.index = index
				self.transactions = transactions
				self.timestamp = timestamp
				self.previous_hash = previous_hash
				self.nonce = nonce

		def compute_hash(self):
			# Construct block header in order to hash it
				self.trans = ''
				for x in self.transactions:
					self.trans += x
				blockHeader = self.previous_hash + self.trans + str(self.timestamp) + str(self.nonce)
				
				return sha256(blockHeader.encode()).hexdigest()


class Blockchain:
	def __init__(self):
		self.unconfirmed_transactions = ['98cb2f68536196078ee04ec5a89eb875ba19ce2e22b44dae3055712a91c7606e']
		self.chain = []
		# A genisis block is the very first block in the blockchain
		self.create_genisis_block()
		self.minedata = {"nonce":[],"hash":[]}

	# The genesis block is unique in that it cannot have a previous hash, and therefore, is treated in its own function.
	def create_genisis_block(self):
		genisis_block = Block(0, [], time.time_ns(), "0")
		genisis_block.hash = genisis_block.compute_hash()
		self.chain.append(genisis_block)
		return 
	# Simple function and decorator to find the latest block.
	@property
	def last_block(self):
		return self.chain[-1]

	# Target difficulty for proof of work is set.
	difficulty = 2

	#The brute force of our mining functionality, the POW system. 
	def proof_of_work(self, block):
		# First, set values to later be displayed on webpage.
		self.minedata["blockMined"] = []
		noncedat = self.minedata["nonce"] = []
		hashdat = self.minedata["hash"] = []
		startmsg = self.minedata["start"] = []
		# Set target hash to be displayed on webpage 
		startmsg.append("POW initiated... Target: "+str('0'*Blockchain.difficulty))
		print("POW initiated\nTarget: "+'0'*Blockchain.difficulty+"\n")
		# Hash at nonce 0
		computed_hash = block.compute_hash()
		noncedat.append(block.nonce)
		hashdat.append(computed_hash)
		# Hash nonce from 1...n (where n is amount of hashes to get target hash)
		while not computed_hash.startswith('0'*Blockchain.difficulty):
			block.nonce += 1
			computed_hash = block.compute_hash()
			noncedat.append(block.nonce)
			hashdat.append(computed_hash)
			print("Nonce: "+str(block.nonce)+"\nHash: "+str(computed_hash)+"\n========")
		self.minedata["blockMined"] = "Target of "+str(blockchain.difficulty)+" zeros met! Block mined!"
		return computed_hash

	# Function to add valid block to blockchain
	def add_block(self, block, proof):
		previous_hash = self.last_block.hash
		if previous_hash != block.previous_hash:
			return False
		if not self.is_valid_proof(block, proof):
			return False
		# Normally bitcoin would only take a cirtain amount of transactions out of pool,
		# but due to sample size and continueity for panel, we will just empty entire pool into block. 
		self.unconfirmed_transactions = []
		block.hash = proof
		self.chain.append(block)
		return
	
	# This function validates that the target is met and checks against injectection of block hash.
	def is_valid_proof(self, block, block_hash):
		return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

	# Mine function overseeing our POW system 
	def mine(self):
		if not self.unconfirmed_transactions:
			# An empty block cannot be mined, so dont allow it
			print("ERROR: No transactions to mine")
			self.minedata["blockMined"] = "ERROR: No transactions to mine"
			return False
		# Collection/application of peripheral data for the new block
		last_block = self.last_block
		new_block = Block(  index=last_block.index + 1,
							transactions=self.unconfirmed_transactions,
							timestamp=time.time_ns(),
							previous_hash=last_block.hash)
		proof = self.proof_of_work(new_block)
		self.add_block(new_block, proof)
		return new_block.index

blockchain = Blockchain()

# Since we are building our blockchain environment for a web environment used by panel members,
# we initiate a user class to properly handle user events and data. 
class User:
	def __init__(self,username,id):
		self.username = username
		self.id = id
		# Notice how ledger is an array instead of a value, this array will track in/outcoming transactions 
		# to calculate the net worth of a wallet, in traditional blockchain style. ( ͡° ͜ʖ ͡°)>⌐■-■
		self.ledger = [50]
		# Not the exact method used in bitcoin to calculate private and public keys, but security needs not to be so intensive
		self.privateKey = sha256(base58.b58encode(str(str(self.id)+self.username).encode())).hexdigest()
		self.publicKey = str(sha256(sha256(self.privateKey.encode()).hexdigest().encode()).hexdigest())
		self.publicKeyHash = str(sha256(self.publicKey.encode()).hexdigest())

# Initialize Users
user0 = User("jamie_coolguy_humble", 1)
user1 = User("edwin_griffin", 2)
user2 = User("matthew_alger", 3)
user3 = User("adrian_herrara", 4)
user4 = User("panelist5", 5)
userList = [user0,user1,user2,user3,user4]

# Transaction handling
def pay(userlist, sender, recipPubKeyHash, amountstr, sid):
	amount = int(amountstr)
	# No negitive inputs to give yourself someone else's money.
	if amount < 0: 
		return sio.emit("tranactionResponse", "Please enter a valid number.", room=sid)
	
	# Find recipient
	recipient = None
	for x in userlist:
		if x.publicKeyHash == recipPubKeyHash:
			recipient = x
	if recipient == None: 
		return False 

	# Since a blockchain holders wallet is technically made up of the previous transactions to such wallet,
	# when transacting, a sender is really sending a previously received transaction of greater value 
	# (or multiple of smaller value to add up to the desired amount) than the amount which they desire to send to another wallet. 

	transAmount = None
	total = 0
	for x in sender.ledger:
		total += x
		if x >= amount:
			transAmount = x
	# if we need to combine transactions, find which ones
	if transAmount == None:
		if total >= amount:
			total = 0
			# Sort ledger values from greatest to least great in order to find sum of transactions as efficiently as possible.
			for x in sender.ledger.sort(reverse=True):
				if total < amount:
					total += x
			if total < amount: 
				return sio.emit("tranactionResponse",[0,"Insufficient funds to make transaction"], room=sid)
			transAmount = total

	# Ledger Logic i.e(neutralize input, send recipients output, give sender change)
	sender.ledger.append(0-transAmount)
	recipient.ledger.append(amount)
	sender.ledger.append(transAmount-amount)

	# Create traditional trasaction records. (ง ͡ʘ ͜ʖ ͡ʘ)ง 
	# sigScipt = priv key and pub key (from sender), hash of public key (from recipient) 
	# trasaction = public key (from recipient), private key (from sender), sigScript, amount
	sigScript = sender.privateKey + sender.publicKey + recipient.publicKeyHash
	transaction = recipient.publicKey + sender.privateKey + sigScript + amountstr

	blockchain.unconfirmed_transactions.append(transaction)
