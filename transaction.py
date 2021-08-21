from aiohttp.web import HostSequence
import users
from block import blockchain
from hashlib import sha256
import time, random
import threading
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
"""
sender_private_key
recipient_public_key,
amount,
start,
end,
limit,
if the user submits a Time_contract:
	dates = {
		"start_date" : date,
		"increment" : 3 days,
		"end_date" : date
	}
otherwise:
	None

var data= {
	amount:amount,
	sender_private_key:[sender_private_key],
	recipient_public_key:[recipient_public_key],
	limit:limit,
	dates: limit==0 ? 	{
		start_date: start,
		increment:increment,
		end_date: end
	}:null
}
"""
def create_contract(amount: int, sender_private_key : int, recipient_public_key : int, limit : int, dates): # Add an Amount
	global CONST_ID, CONST_HEDGEFUND
	if limit == 0:
		return Time_Contract(dates["start_date"], amount, sender_private_key, recipient_public_key, dates, CONST_ID)
	elif recipient_public_key:
		# add user to hedgefund
		# check publickey == hedgefund.public_key
		user = users.find_user_private_key(sender_private_key)
		CONST_HEDGEFUND.smart_invest(user, amount, limit) # Since its running infinitley, 
	CONST_ID += 1

def sign_contract(contract_id, user_private_key): #! WHAT KINDA KEY????
	pass

class Smart_Contract:
	# did format -> { publickey : amount_contributed }
	# senders -> {"node1":25, "node2":30}
	# recipients -> {"node3":55}
	# amount -> 55

	def __init__(self, date, senders, recipients, id):
		self.date = date 
		self.senders = senders #senders parameter is just id
		self.recipients = recipients #recipients parameter is just id
		self.id = id
		self.amount = 0
		self.amTime_Contractount= 0
		# {'4884b436627b0c6168163032f28395386ca42163e0dfb2ff25c438b42c33cb41': '012344'}
		for v in self.senders.values(): #? what is senders
			print(v)
			self.amTime_Contractount += int(v) 
		self.validate()

	@staticmethod
	def load_json(self, json):
		pass # he is creating a new constructor, if you go to 

	def validate(self): # Flag for Jonte to fix probs tonnes of bugs idk @Jonte
		#find user object
		n_users = users.load_user_json()
		self.senderArr = []
		for private_key in self.senders.keys():
			for user in n_users:
				if user["private_key"] == private_key:
					self.senderArr.append(user)
					break
			else:
				raise Exception("sender not found")
		
		self.recipientArr = []
		for public_key in self.recipients.keys():
			for n in n_users:
				if n["public_key"] == public_key:
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


class Time_Contract(Smart_Contract):
	def __init__(self, date, amount, senders, recipients, dates : dict, id):
		Smart_Contract.__init__(self, date, senders, recipients, id)
		self.transaction_timestamps = self.create_transaction_dates(dates)
		self.amount = amount

	@staticmethod
	def create_transaction_dates(dates) -> list:
		start_str = dates['start_date']
		increment = int(dates['increment'])
		end_str = dates['end_date']

	#   File "C:\Program Files\WindowsApps\PythonSoftwareFoundatio`n.Python.3.9_3.9.1776.0_x64__qbz5n2kfra8p0\lib\_strptime.py", line 349, in _strptime
	#     raise ValueError("time data %r does not match format %r" %
	# ValueError: time data '08/31/2021' does not match format '%a %b %d %H:%M:%S %Y'

		start = time.strptime(start_str, "%m/%d/%Y")
		end = time.strptime(end_str,"%m/%d/%Y")
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
				amount += 1
		return amount

mutex = threading.Lock()

class HedgeFund:
	def __init__(self):
		user = users.login("HedgeFund", "hedgefund") # if its already been stored in the json file just read from it
		if user['status'] != "success":
			raise Exception(user['status'])
		
		self.details = user["user"]
		self.wallet = 1000
		self.invested_users = {}
		t = threading.Thread(target=self._increment_user_investment)
		t.start()
		
	def _increment_user_investment(self): # Run this method like every 5 mins or something (I removed user parameter from this function)
		while True: 
			time.sleep(CONST_HEDGEFUND_SLEEP_TIME)
			mutex.acquire()
			for user in self.invested_users.keys():
				added_money = random.randrange(50)
				self.invested_users[user][0] += added_money
				self.wallet += added_money
				if self.invested_users[user][1] <= self.invested_users[user][0]: # invested_users = {"public_key": [invested_amount, limit/threshold]}
					user_dict = users.get_user_by_public_key(user)
					create_transaction_no_validation(self.details["private_key"], user_dict["public_key"], self.invested_users[user][0]) # Give user money back
					del self.invested_users[user]
			mutex.release()

	def smart_invest(self, user, investment, limit) -> Smart_Contract:
		mutex.acquire()
		if (user["public_key"] in self.invested_users):
			self.invested_users[user["public_key"]][0] += investment # If the user already exists in the invested users, we assume they want to invest more money into the hedge fund
		else:
			self.invested_users[user["public_key"]] = [investment, limit] # If they don't exist, then we assume they are a new investor and add them to the dict
		# self, date, senders : dict, recipients : dict, id)
		# below is jamies code, idk what its for
		mutex.release()
		return Smart_Contract(time.asctime(), {"sender": investment}, {"HedgeFund": investment})
		
CONST_HEDGEFUND_SLEEP_TIME = 5 # seconds
CONST_ID = 0
CONST_HEDGEFUND = HedgeFund()

# class Bank(HedgeFund):
# 	def __init__(self):
# 		HedgeFund.__init__() # Define stuff in like comments
		