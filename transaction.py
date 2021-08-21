import users
from block import blockchain
from hashlib import sha256
import time

Const_ID = 0

class Transaction:
	def __init__(self, sender, recipient, amount, hash=0): #user dictionary
		self.sender = users.find_user_private_key(sender)
		self.recipient = users.find_user_public_key(recipient)
		self.amount = int(amount)
		self.time = time.asctime()
		if hash == 0:
			# self.recipient.encode() is encoding ID instead of public key 
			part_1 = str(twelve_chars(self.amount))
			part_2 = str(sha256(self.recipient["public_key"].encode()).hexdigest())
			part_3 = str(sha256(self.sender["private_key"].encode()).hexdigest())
			self.hash = sha256((part_1 + part_2 + part_3).encode()).hexdigest()
		else:
			self.hash = hash
		self.tax = blockchain.tax_rate * self.amount

	def validate_transaction(self):
		net_worth = blockchain.get_user_worth(self.sender) #this here
		# net_worth = 1000 # JASON MONEY HERE put it here for cheating
		if net_worth - self.amount < self.amount: 
			return {"status" : "Insufficient Funds"}
		# transaction = twelve_chars(self.amount)+sha256(self.recipient.publicKey.encode()).hexdigest()+sha256(self.sender.privateKey).encode().hexdigest()
		blockchain.unconfirmed_transactions.append(self.hash)
		return {"status" : True}

def twelve_chars(amount):
	# each hash is ed in the 64 characters long, so total msg length is 140 characters #? maybe end instead of ed
	return "0"*(12-len(str(amount))) + str(amount)

def create_transaction(sender, recipient, amount): 
	t = Transaction(sender, recipient, amount)
	# return t.validate_transaction()
	return t.cheat_transaction()

def create_transaction_no_validation(sender, recipient, amount):
	t = Transaction(sender, recipient, amount)
	blockchain.add_transaction(t)
	return t

"""

#create_contract (with sender_public_key, recipient_public_key, date_closed, amount_in, amount_out)
def create_contract(date, amount: int, times : list, sender_public_key : dict, recipient_public_key : dict, condition_type, condition_argument): # Add an Amount
	global Const_ID
	Const_ID += 1
	if condition_type == "withdrawl" and condition_argument == "salary":
		for i in times:
			sc = Smart_Contract(time.asctime(), sender_public_key, recipient_public_key, condition_type, condition_argument, Const_ID)
	try:
		sc = Smart_Contract(time.asctime(), sender_public_key, recipient_public_key, condition_type, condition_argument, Const_ID)
		return True
	except:
		return False
	pass


class Smart_Contract:
	# did format -> { publickey : amount_contributed }
	# senders -> {"node1":25, "node2":30}
	# recipients -> {"node3":55}
	# amount -> 55

	def __init__(self, date, senders, recipients, condition_type, condition_argument, id):
		self.date = date #?is date necersarry?
		self.senders = senders #! WHAT TYPE?
		self.recipients = recipients
		self.amount = 0
		self.condition_type = condition_type
		self.condition_argument = condition_argument
		self.id = id
		#find net value of SC
		for k, v in self.senders:
			self.amount += v
		self.validate()
		self.validation_keys = {}

	def validate(self):
		#find user object
		nusers = users.load_user_json()
		self.senderArr = []
		for senderK, senderV in self.senders:
			for n in nusers:
				if n["public_key"] == senderK.public_key:
					self.senderArr.append(n)
					break
			else:
				raise Exception("sender not found")
		self.recipientArr = []
		for recipientK, recipientV in self.recipients:
			for n in nusers:
				if n["public_key"] == recipientK.public_key:
					self.recipientArr.append(n)
					break
			else:
				raise Exception("recipient not found")			
		
		self.participants = self.recipientArr + self.senderArr

		# we now have two arrays containing the JSON objects 
		for x in self.senderArr:
			net_wallet = blockchain.get_user_worth(x)
			if net_wallet <= self.amount:
				return {"status": x["username"]+" Has Insufficient Funds"}
		

	def sign_request(self):
		blockchain.add_SC(self) #! WHAT IS ADD_
		return True

	def query_condition(self):
		#time.asctime([t]) has format of Sun Jun 20 23:21:05 1993'
		if self.condition_type == "time":
			if self.condition_argument <= time.asctime():
				self.execute()
				return {"status": "Smart Contract Fulfilled"}
			else:
				return {"status": "Smart Contract Not Fulfilled"}

		elif self.condition_type == "withdrawl":
			if self.condition_argument == "salary":
				pass
			elif self.condition_argument == "lumpsum":
				pass

		# Hedgefund specific
		elif self.condition_type == "stop_limit":
			#self.condition_argument ->	the number to stop at, the number should be derived from a function which slowly increases tan int which is supposed to be an investment account
			pass
		# Edge Case
		else:
			raise Exception("Other query condition not implemented: " + str(self.condition_type))

	def sign(self, user_id):
		#check if user_id exists in participants
		#check if user_id doesn't exist in signatures
		#add to signatures
		#if len(signatures) == len(participants): return Done
		if user_id in self.validation_keys: return {"status": "failed, already signed document"}
		self.validation_keys.append(user_id)
		if len(self.validation_keys) == len(self.senderArr + self.recipientArr):
			return {"status": "finished"}
		return {"status": "not finished"}

	def execute():
		pass

	def release():
		pass

"""