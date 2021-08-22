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
		self.amount = float(amount)
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
		#print("called validate")
		net_worth = users.get_user_worth(self.sender) #this here
		if net_worth - self.amount < 0: 
			return {"status" : "Insufficient Funds"}
		# transaction = twelve_chars(self.amount)+sha256(self.recipient.publicKey.encode()).hexdigest()+sha256(self.sender.privateKey).encode().hexdigest()
		blockchain.unconfirmed_transactions.append(self.hash)
		return {"status" : "success"}

def twelve_chars(amount):
	# each hash is ed in the 64 characters long, so total msg length is 140 characters #? maybe end instead of ed
	return "0"*(12-len(str(amount))) + str(amount)

def create_transaction(sender, recipient, amount): 
	t = Transaction(sender, recipient, amount)
	tmp = t.validate_transaction()
	if tmp["status"] == "success":
		blockchain.add_transaction(t)
		return tmp
	else:
		return tmp

def create_transaction_no_validation(sender, recipient, amount): 
	t = Transaction(sender, recipient, amount)
	blockchain.add_transaction(t)
	return t


def create_contract(amount: int, sender_private_key : int, recipient_public_key : int, limit : int, dates): # Add an Amount
	if limit == 0:
		tmp = Time_Contract(dates["start_date"], amount, sender_private_key, recipient_public_key, dates)
		blockchain.unsigned_contracts.append(tmp)
		return tmp
	else:
		user = users.find_user_private_key(list(sender_private_key.keys())[0]) #HERE
		tmp = CONST_HEDGEFUND.smart_invest(user, amount, limit) # Since its running infinitley, 
		blockchain.unsigned_contracts.append(tmp)
		return tmp

def get_all_contracts(username, pending):
	# status types: "pending", "active", "fulfilled", "declined"
	#contracts should be on blockchain and hedgefund
	user = users.get_user_by_username(username)
	contracts = []
	# if username in CONST_HEDGEFUND.invested_users:
	# 	contracts.append(CONST_HEDGEFUND)
	if pending == "active":
		for block in blockchain.contracts_chain:
			for contract in block.transactions:
				if contract.status != "active": continue
				elif user["private_key"] in contract.senders: contracts.append(contract)
				elif user["public_key"] in contract.recipients: contracts.append(contract)
	elif pending == "pending":
		for contract in blockchain.unsigned_contracts + blockchain.unconfirmed_contracts:
			if user["private_key"] in contract.senders: contracts.append(contract)
			elif user["public_key"] in contract.recipients: contracts.append(contract)
	elif pending == "fulfilled":
		for block in blockchain.contracts_chain:
			for contract in block.transactions:
				if contract.status != "fulfilled": continue
				elif user["private_key"] in contract.senders: contracts.append(contract)
				elif user["public_key"] in contract.recipients: contracts.append(contract)
	elif pending == "declined":
		raise Exception("ERROR TRYING TO FIND DECLINED TRANSACTIONS NOT IMPLEMENTED")
	else:
		raise Exception("pending not found with " + str(pending))
	return list(set(contracts))

ID_COUNT = 0
class Smart_Contract:
	# did format -> { publickey : amount_contributed }
	# senders -> {"node1":25, "node2":30}
	# recipients -> {"node3":55}
	# amount -> 55

	def __init__(self, date, senders, recipients):
		self.date = date 
		self.senders = senders #senders parameter is just id
		self.recipients = recipients #recipients parameter is just id
		self.limit = [v for k,v in recipients.items()][0]
		if isinstance(self, Time_Contract): self.limit = "N/A"
		self.amount = 0
		self.amTime_Contractount = 0
		global ID_COUNT
		self.id = ID_COUNT
		ID_COUNT+=1
		# {'4884b436627b0c6168163032f28395386ca42163e0dfb2ff25c438b42c33cb41': '012344'}
		for v in self.senders.values(): #? what is senders
			#print(v)
			self.amTime_Contractount += int(v) 
		self.validate()
		self.status = "pending"
		particiSTR = ''
		for x in [self.senders,self.recipients]:
			for y in x.items():
				particiSTR += str(y)
		self.hash = sha256((str(self.id)+particiSTR).encode()).hexdigest()
		self.tax = blockchain.tax_rate * self.amount

	@staticmethod
	def find_contract_with_hedge_public_key(public_key, hedge_fund):
		for block in blockchain.contracts_chain:
			for contract in block.transactions:
				if (public_key in contract.senders) and (hedge_fund["public_key"] in contract.recipients) or (public_key in contract.recipients) and (hedge_fund["public_key"] in contract.sends):
					return contract
		return None

	@staticmethod
	def get_pending_contracts():
		return blockchain.unconfirmed_contracts

	def validate(self): # Flag for Jonte to fix probs tonnes of bugs idk @Jonte
		#find user object
		n_users = users.load_user_json()
		self.senderArr = []
		for private_key in self.senders.keys(): 
			for user in n_users:
				if user["private_key"] == private_key:
					self.senderArr.append(user)
					break
		if len(self.senderArr) == 0: #!= len(self.senders.keys())
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
			if x['private_key'] == "5429ea8d2ad67e97a5ace9c4782a536311ac735d0c5c0be11b63c512ec652e48": continue
			if net_wallet <= self.amount:
				return {"status": x["username"]+" Has Insufficient Funds"}
		# push to blockchain
		self.sign_request()

	def decline_contract(self):
		self.status = "declined"
		blockchain.unsigned_contracts.remove(self)
		return
		
	def sign_request(self):
		blockchain.add_SC(self) 
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


        # n.start_date,
        # n.end_date,
class Time_Contract(Smart_Contract):
	def __init__(self, date, amount, senders, recipients, dates : dict):
		super().__init__(date, senders, recipients)		
		self.transaction_timestamps = Time_Contract.create_transaction_dates(dates)
		self.amount = amount
		self.start_date = dates['start_date']
		self.increment = int(dates['increment'])
		self.end_date = dates['end_date']

	@staticmethod
	def create_transaction_dates(dates) -> list:
		start_str = dates['start_date']
		increment = int(dates['increment'])
		end_str = dates['end_date']

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

	def fulfilled(self) -> bool:
		return (len(self.transaction_timestamps) - self.get_num_previous_transactions == 0)

mutex = threading.Lock()

class HedgeFund:
	def __init__(self):
		user = users.login("HedgeFund", "hedgefund") # if its already been stored in the json file just read from it
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
				self.invested_users[user][0] += int(added_money)
				self.wallet += added_money
				self.check_threshold_exceeded(user)
			mutex.release()

	def check_threshold_exceeded(self, user):
			if self.invested_users[user][1] <= self.invested_users[user][0]: # invested_users = {"public_key": [invested_amount, limit/threshold]}
				user_dict = users.get_user_by_public_key(user)
				create_transaction(self.details["private_key"], user_dict["public_key"], self.invested_users[user][0]) # Give user money back
				del self.invested_users[user]
				Smart_Contract.find_contract_with_hedge_public_key(user, self.details)

	def smart_invest(self, user, investment, limit) -> Smart_Contract:
		mutex.acquire()
		if (user["public_key"] in self.invested_users):
			self.invested_users[user["public_key"]][0] += int(investment) # If the user already exists in the invested users, we assume they want to invest more money into the hedge fund
		else:
			self.invested_users[user["public_key"]] = [int(investment), limit] # If they don't exist, then we assume they are a new investor and add them to the dict
		mutex.release()
		return Smart_Contract(time.asctime(), {self.details["private_key"]: limit}, {user["public_key"]: limit})

	# def get_limit(self, public_key):
	# 	n = self.invested_users[public_key]
	# 	return n[1]
		
CONST_HEDGEFUND_SLEEP_TIME = 5 # seconds
CONST_HEDGEFUND = HedgeFund()

# class Bank(HedgeFund):
# 	def __init__(self):
# 		super().__init__() # Define stuff in like comments
# 		self.intrest = 1.25
# 		# self.invested = { 
# 		# 		"public_key" : [invested_amount, init_investment_amount, [start_date, end_date] => []]
# 		# }

# 	def _increment_user_investment(self):
# 		while True: 
# 			time.sleep(CONST_HEDGEFUND_SLEEP_TIME)
# 			mutex.acquire()
# 			for user in self.invested_users.keys():
# 				added_money = self.intrest * self.invested_users[user][0]
# 				self.invested_users[user][0] += added_money
# 				self.wallet += added_money
# 				# total_amount / interval
# 			mutex.release() 

# 	def smart_invest(self, user, investment, dates : dict) -> Smart_Contract:
# 		mutex.acquire()
# 		if (user["public_key"] in self.invested_users):
# 			self.invested_users[user["public_key"]][0] += investment # If the user already exists in the invested users, we assume they want to invest more money into the hedge fund
# 		else:
# 			self.invested_users[user["public_key"]] = [investment, investment, [dates["start_date"], int(dates["interval"]), dates["end_date"]]] # If they don't exist, then we assume they are a new investor and add them to the dict
# 		mutex.release()
		
# 		return Time_Contract(time.asctime(),{self.details["public_key"]: limit}, {user["public_key"]: limit})


#data["contract_id"], data["private_key"]
def sign_transaction(id, private_key): #param
	for x in blockchain.get_unsigned_transactions():
		if x.id == id:
			x.sign(private_key)
			break
	else:
		return {"status": "failed signing contract"}
	return {"status": "success"}
def decline_transaction(id, private_key): #param
	for x in blockchain.get_unsigned_transactions():
		if x.id == id:
			x.decline(private_key)
			break
	else:
		return {"status": "failed declining contract"}
	return {"status": "success"}