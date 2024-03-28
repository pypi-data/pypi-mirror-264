# Installation
* pip install --upgrade lbank-connector-python -i https://pypi.org/simple
## Contract Call
* You need to apply for the corresponding api_key and api_secret
* 
```python
from lbank.old_api import BlockHttpClient
api_key = ""
api_secret = ""
# service address
base_url = "https://lbkperp.lbank.com"
# Encryption method
sign_method = "RSA"
client = BlockHttpClient(
    sign_method=sign_method,
    api_key=api_key,
    api_secret=api_secret,
    base_url=base_url
)
# Order api
order_url = "/cfd/openApi/v1/prv/placeOrder"
order_data = {
    "clientOrderId": f"{order_id}",
    "offsetFlag": 0,
    "orderPriceType": 4,
    "origType": 0,
    "price": 2000,
    "side": "BUY",
    "symbol": "ETHUSDT",
    "volume": 0.01,
}
res = client.http_request("POST", order_url, order_data)
print(res)
```