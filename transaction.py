import users
from block import blockchain
from hashlib import sha256
import time

CONST_ID = 0

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
	
	@staticmethod
	def load_json(self, json):
		pass

	def validate_transaction(self):
		net_worth = users.get_user_worth(self.sender) #this here
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


#(self, date, senders, recipients, condition_argument, id, transaction_timestamps, contract_length)
def create_contract(date, amount: int, sender_public_key : dict, recipient_public_key : dict, condition_type, condition_arguments): # Add an Amount
	global CONST_ID
	if condition_type == "time":
		return Time_Contract(date, sender_public_key, recipient_public_key, condition_arguments["time_stamp"], condition_arguments["stop_date"], CONST_ID)
	elif condition_type == "stop_limit":
		Stop_Limit(date, sender_public_key, recipient_public_key, CONST_ID)
	CONST_ID += 1



class Smart_Contract:
	# did format -> { publickey : amount_contributed }
	# senders -> {"node1":25, "node2":30}
	# recipients -> {"node3":55}
	# amount -> 55

	def __init__(self, date, senders : dict, recipients : dict, id):
		self.date = date 
		self.senders = senders 
		self.recipients = recipients
		self.id = id
		self.amount = 0
		#find net value of SC
		for k, v in self.senders:
			self.amount += v
		self.validate()

	@staticmethod
	def load_json(self, json):
		pass # he is creating a new constructor, if you go to 

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

		self.validation_keys = {x["private_key"]:False for x in self.participants}


		# we now have two arrays containing the JSON objects 
		for x in self.senderArr:
			net_wallet = users.get_user_worth(x)
			if net_wallet <= self.amount:
				return {"status": x["username"]+" Has Insufficient Funds"}
		# push to blockchain
		self.sign_request()

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

	def sign(self, privkey):
		for k in self.validation_keys.keys():
			if privkey == k:
				self.validation_keys[k] = True
				self.query_signatures()
				return {"status": "Successful Signature"}
		return {"status": "Failed Signature: invalid private key"}

	def query_signatures(self):
		for x in self.validation_keys.values():
			if x == False:
				return {"status":"Constract is not signed"}
		blockchain.add_contract(self)
		return {"status":"Constract Completely Signed, Processing now!"}


class Stop_Limit(Smart_Contract) :
	def __init__(self, date, amount, senders, recipients, condition_argument : int, id):
		Smart_Contract.__init__(self, date, amount, senders, recipients, id)
		self.limit = condition_argument

	def amount_till_limit(self):
		pass

class Time_Contract(Smart_Contract):
	def __init__(self, date, amount, senders, recipients, condition_argument : dict, id):
		Smart_Contract.__init__(self, date, amount, senders, recipients, id)
		self.transaction_timestamps = Time_Contract.create_transaction_dates(condition_argument)
		
	@staticmethod
	def create_transaction_dates(dates: dict) -> list:
		start = dates['start_date']
		increment = dates['increment']
		end = dates['end_date']
		start = time.strptime(start)
		end = time.strptime(end)
		start_sec = time.mktime(start)
		end_sec = time.mktime(end)
		result = []
		while(start_sec < end_sec):
			result.append(time.asctime(time.localtime(start_sec)))
			start_sec += increment * 24 * 60 * 60
		return result

	def get_num_previous_transactions(self) -> int:
		timestamps = [time.strptime(x) for x in self.transaction_timestamps]
		now = time.strptime(time.asctime())
		amount = 0
		for i in timestamps:
			if i < now:
				amount+=1
		return amount
		

class HedgeFund:
	def __init__(self):
		users.create_user("HedgeFund","hedgefund")
		self.wallet = users.get_user_worth()

	def invest(self):
		pass
		
