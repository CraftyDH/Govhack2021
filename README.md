# GriffinCoin

## Dataset's used
1. [Ethereum Data from (Dec 2017 - Sep 2020)](https://data.csiro.au/collections/collection/CIcsiro:46394)

We used this data set because...

## Pip requirements
1. aiohttp
2. requests
3. bs4
4. lxml
5. base58
6. random-username

```sh
pip3 install aiohttp requests bs4 lxml hashlib base58
```

## Running
### Run the data scraper
```sh
cd data
## Copy blocks_2020_08_14_09_00_00.csv from the dataset into this folder 
python3 ./data_scraping.py
```

### Run the python server
```sh
python3 ./server.py
# Open browser to localhost:8080
```