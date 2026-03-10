
import requests
import random
from faker import Faker

fake = Faker()

URL = "http://localhost:8000/expenses"

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0NEBleGFtcGxlLmNvbSIsImV4cCI6MTc3MzEyOTY4OH0.90beqbHrBSEMNFp5NEuYtNYCWQuWepm2hfKydnZmVRw"

categories = [
    "food",
    "transport",
    "rent",
    "entertainment",
    "utilities",
    "other"
]

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

for i in range(100):

    payload = {
        "amount": round(random.uniform(50, 2000), 2),
        "description": fake.sentence(nb_words=3),
        "category": random.choice(categories)
    }

    r = requests.post(URL, json=payload, headers=headers)

    print(i+1, r.status_code)