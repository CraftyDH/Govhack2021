import users
from block import blockchain
from hashlib import sha256
import time

class Transaction:
	def __init__(self , sender, recipient, amount, hash=0): #user dictionary
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.time = time.asctime()
		if hash == 0:
			self.hash = twelve_chars(self.amount)+sha256(self.recipient.publicKey.encode()).hexdigest()+sha256(self.sender.privateKey).encode().hexdigest()
		else:
			self.hash = hash
		self.tax = blockchain.tax_rate * self.amount

	def validate_transaction(self, user):
		net_worth = blockchain.get_user_worth(user) #this here
		if net_worth - self.amount < self.amount: 
			return {"status" : "Insufficient Funds"}
		# transaction = twelve_chars(self.amount)+sha256(self.recipient.publicKey.encode()).hexdigest()+sha256(self.sender.privateKey).encode().hexdigest()
		blockchain.unconfirmed_transactions.append(self.hash)
		return {"status" : "success"}

def twelve_chars(amount):
	# each hash is ed in the 64 characters long, so total msg length is 140 characters #? maybe end instead of ed
	return "0"*(12-len(str(amount))) + str(amount)
 
def create_transaction(self, sender, recipient, amount): 
	t = Transaction(sender, recipient, amount)
	return t.validate_transaction()

def create_transaction_no_validation(self, sender, recipient, amount):
	return Transaction(sender, recipient, amount)

#create_contract (with sender_public_key, recipient_public_key, date_closed, amount_in, amount_out)
def create_contract(self, sender_public_key, recipient_public_key, date_closed, amount_in, amount_out): #! amount_in not passed, JONTE there has been a change here
	sc = Smart_Contract(time.asctime(), sender_public_key, recipient_public_key, "time", amount_out) #! date passed as -1
	return sc.validate_transaction()

class Smart_Contract:
	# didc format -> { publickey : amount_contributed }
	# senders -> {"node1":25, "node2":30}
	# recipients -> {"node3":55}
	# amount -> 55
	def __init__(self, date, senders, recipients, condition_type, condition_argument):
		self.date = date #?is date necersarry?
		self.senders = senders #! I have passed senders and receiver ids rather than the dictionaries themselves. 
		self.recipients = recipients
		self.amount = 0
		self.condition_type = condition_type
		self.condition_argument = condition_argument

		for k, v in self.senders:
			self.amount += v
		for k, v in self.recipients:
			self.amount += v	

		#find user object
		nusers = users.load_user_json()
		user = None
		for senderK, senderV in self.senders:
			for n in nusers:
				if n.public_key == senderK.public_key:
					user = n
					break
			else: 
				raise Exception("user not found")
		blockchain.get_user_worth(user)


	def query_condition(self):
		#time.asctime([t]) has format of Sun Jun 20 23:21:05 1993'
		if self.condition_type == "time":
			if self.condition_argument <= time.asctime():
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

	def execute():
		pass

	def release():
		pass