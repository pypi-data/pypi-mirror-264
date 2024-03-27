import requests

def get_token(URL, applicationId, applicationKey):
    # print(APPLICATION_ID, APPLICATION_KEY)
    headers = {
        'accept': 'application/json',
        'applicationId':applicationId,
        'applicationKey':applicationKey
    }

    response = requests.get(URL+'get-token/', headers=headers)
    return response.json()


def get_customers(URL, Token):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.get(URL+'customers', headers=headers)
    return response.text


def add_customers(URL, Token, payload):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.post(URL+'customers/', headers=headers, json=payload)
    return response.text


def add_transactions(URL, Token, payload):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.post(URL+'transactions/', headers=headers, json=payload)
    return response.text


def add_transactions_history(URL, Token, payload):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.post(URL+'transactions-history/', headers=headers, json=payload)
    return response.text


def get_cashback_payments(URL, Token, date_from, date_to):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.get(URL+'cashback-payments?date_from=%s&date_to=%s'% (date_from, date_to), headers=headers)
    return response.text

def get_cashbackpayments(URL, Token, date_from, date_to):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.get(URL+'cashbackpayments?date_from=%s&date_to=%s'% (date_from, date_to), headers=headers)
    return response.text

def get_active_offers(URL, Token):
    headers = {
        'accept': 'application/json',
        'Token': 'Bearer '+Token,
    }
    response = requests.get(URL+'activeoffers', headers=headers)
    return response.text