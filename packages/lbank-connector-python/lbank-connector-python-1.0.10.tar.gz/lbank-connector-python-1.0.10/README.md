# 安装
* pip install --upgrade lbank-connector-python -i https://pypi.org/simple
## 合约调用
* 需申请好对应的api_key以及api_secret
* 
```python
from lbank.old_api import BlockHttpClient
api_key = ""
api_secret = ""
# 对应的服务地址 正式
base_url = "https://lbkperp.lbank.com"
# 加密方式
sign_method = "RSA"
client = BlockHttpClient(
    sign_method=sign_method,
    api_key=api_key,
    api_secret=api_secret,
    base_url=base_url
)
# 下单api
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