import requests
from bs4 import BeautifulSoup as soup

# New data format
# block_id, block_hash, block_timestamp, difficulty, transaction_hash, transaction_timestamp, sender, receiver, amount, tax
# Made by Manindra
CONST_DATA_PATH = "block_data.csv"
CONST_NEW_DATA_PATH = "block.csv"
CONST_HEADERS = {
'authority': 'scrapeme.live',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-user': '?1',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
# Initalize the new CSV file
# with open(CONST_NEW_DATA_PATH, "w") as w:
#     w.write("block_id, block_hash, block_timestamp, difficulty, transaction_hash, transaction_timestamp, sender, receiver, amount, tax\n")

def scrape_transactions(transact) -> list:
    transaction_children = list(transact.children)
    transaction_hash = transaction_children[1].find("a").text
    timestamp_tx = transaction_children[4].find("span").text
    sender = transaction_children[6].find("a").text
    receiver = transaction_children[8].find("a").text
    amount = transaction_children[9].text.split()[0]
    tax = transaction_children[10].text
    return [transaction_hash, timestamp_tx, sender, receiver, amount, tax]


with open(CONST_DATA_PATH, "r") as f:
    for line in f:
        if not (line.split(",")[0] == "block_number"):
            block = line.split(",")
            id = int(block[0])
            timestamp = block[1]
            difficulty = int(block[3])
            hash = block[10].replace("\\", "0")
            # get the transaction data using the Etherium API                 
            response = requests.get(f"https://etherscan.io/txs?block={id}", headers=CONST_HEADERS).text
            website = soup(response, "lxml")
            transactions_element = website.find("tbody")
            if (transactions_element):
                transactions = transactions_element.children
                for transact in transactions:
                    if (transact != "\n"):
                        if not (list(transact.children)[1].find("span", class_="text-danger")):
                            transaction_data = scrape_transactions(transact)
                            with open(CONST_NEW_DATA_PATH, "a") as a:
                                a.write(f"{id}, {hash}, {timestamp}, {difficulty}, {transaction_data[0]}, {transaction_data[1]}, {transaction_data[2]}, {transaction_data[3]}, {transaction_data[4]}, {transaction_data[5]}\n")
                            print(f"Scraped block: {id}")
                            