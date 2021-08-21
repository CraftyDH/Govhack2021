import users
from block import blockchain

class Transaction:
	def __init__(self, sender, recipient, amount): #user dictionary
		self.sender = sender
		self.recipient = recipient
		self.amount = amount

	# Since a blockchain holders wallet is technically made up of the previous transactions to such wallet,
	# when transacting, a sender is really sending a previously received transaction of greater value 
	# (or multiple of smaller value to add up to the desired amount) than the amount which they desire to send to another wallet. 
	def validate_transaction(self, user):
		net_worth = blockchain.get_user_worth(user) #this here
		total = 0
		
		# Sort ledger values from higher to lower in order to find sum of transactions as efficiently as possible.
		for x in self.sender.ledger.sort(reverse=True):
			if total < self.amount:
				total += x
		if total < self.amount: 
			return {"status" : "Insufficient Funds"}
		transAmount = total

		# Ledger Logic i.e(neutralize input, send recipients output, give sender change)
		self.sender.ledger.append(0 - transAmount)
		self.recipient.ledger.append(self.amount)
		self.sender.ledger.append(transAmount-self.amount)
		
		sigScript = self.sender.privateKey + self.sender.publicKey + self.recipient.publicKeyHash
		transaction = self.recipient.publicKey + self.sender.privateKey + sigScript + str(self.amount)

		blockchain.unconfirmed_transactions.append(transaction)
		return  {"status" : "Transactions Successfully created"}


def create_transaction(self, sender, recipient, amount): 
	t = Transaction(sender, recipient, amount)
	return t.validate_transaction()

#create_contract (with sender_private_key, recipient_public_key, date_closed, amount_in, amount_out)
def create_contract(self, sender_private_key, recipient_public_key, date_closed, amount_in, amount_out):
	pass

#this file is a mess and we need jamie on it ASAP
	#cause it's missing blockchain implementation. That is what needs to be in this file
	#handle local ledgers as well when you change this file

#don't forget to add functions that keep getting deleted for the server api

#also add smart contracts here as well
class Smart_Contract:
	def __init__(self, sender):
		return