SDK for working with the MTHMR CashBack application.

Functional:

- get Token
- add customers data
- add transactions data
- read customers data
- read data on accrued cashbacks

Examples of using:

```python
from mthmrcashback import mthmr_query

URL = "issued when connecting to the application"
applicationId = "issued when connecting to the application"
applicationKey = "issued when connecting to the application"

Token = mthmr_query.get_token(URL, applicationId, applicationKey)

# Adding Customers:
#   "customer_id" - your internal customer_id

dataCustomers=[
  {
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
    "birthday": "1995-03-15",
    "gender": "Male",
    "location_id": 1
  },
  {
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d2",
    "birthday": "1983-05-01",
    "gender": "Female",
    "location_id": 1
  }
]
addCustomers = mthmr_query.add_customers(URL, Token, dataCustomers)

# Reading Customers:

customers = mthmr_query.get_customers(URL, Token)

# Adding Transactions:

# "transaction_id" - unique transaction ID
# "description" - description of the transaction
# "customer_id" - your internal customer_id
# "date" - transaction date GMT
# "merchant_name" - merchant Name,
# "amount" - transaction amount

dataTransactions=[
  {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac12001",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_name": 'Merhant Name',
    "amount": 100
   },
   {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac120003",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d2",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_name": 'Merhant Name',
    "amount": 150
   }
]
addTransactions = mthmr_query.add_transactions(URL, Token, dataTransactions)


# Adding Transactions History:

# "transaction_id" - unique transaction ID
# "description" - description of the transaction
# "customer_id" - your internal customer_id
# "date" - transaction date GMT
# "merchant_name" - merchant Name,
# "amount" - transaction amount

dataTransactionsHistory=[
  {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac12001",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_name": 'Merhant Name',
    "amount": 100
   },
   {
    "transaction_id": "b65cca2a-6809-11ee-8c99-0242ac120003",
    "description": "description",
    "customer_id": "a8de52aa-49e7-4e5c-bb66-1c82ac1d551d2",
    "date": "2023-10-11T10:27:03.987662",
    "merchant_name": 'Merhant Name',
    "amount": 150
   }
]
addTransactionsHistory = mthmr_query.add_transactions_history(URL, Token, dataTransactionsHistory)


# Receiving Active Offers data:

activeOffers = mthmr_query.get_active_offers(URL, Token)


# Receiving CashBack data:

# date_from = "2023-01-01"
# date_to = "2024-02-01"

cashBack = mthmr_query.get_cashback_payments(URL, Token, date_from, date_to)

```