
# tg-api-autoreg
Developed by: **Alexand Macheck**
[My telegram](https://t.me/youbrain)

**Python** module for automatic registration **Telegram User API**
> **pip install tg-api-autoreg**

**Examples:**
			
Short:
``` python
phone = '+123456789'
proxy = '127.0.0.1:8888'

session = Reigister_api(phone, proxy, send_code=True) # initializing
data = session.get_api(input('code: '))
print(data) # -> dict with all avliable info (with api_id, api_hash)
```

Detailed:
``` python	   
phone = '+123456789'
proxy = '127.0.0.1:8888'

session = Reigister_api(phone, proxy) # initializing

random_hash = seesion.send_code() # Send code request
cookies = session.login(input('confirmation code:')) # passing conf code
session.create_api() # creating new api
session.parse_api_data() # parsing & saving all api_id, api_hash

data = session.api_data()
print(data) # -> dict with all avliable info (with api_id, api_hash)
```