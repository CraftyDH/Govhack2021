import users
from block import blockchain

class Transaction:
	def __init__(self, sender, recipient, amount):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount

def create_transaction(self, sender, recipient, amount): 
	#this is not right, it needs to be added to the blockchain or something
	#return Transaction(sender, recipient, amount)
	pass

#create_contract (with sender_private_key, recipient_public_key, date_closed, amount_in, amount_out)
def create_contract(self, sender_private_key, recipient_public_key, date_closed, amount_in, amount_out):
	pass

#this file is a mess and we need jamie on it ASAP
	#cause it's missing blockchain implementation. That is what needs to be in this file
	#handle local ledgers as well when you change this file
	
#don't forget to add functions that keep getting deleted for the server api

#also add smart contracts here as well
