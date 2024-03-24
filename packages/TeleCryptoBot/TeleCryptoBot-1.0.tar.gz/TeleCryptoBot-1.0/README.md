## **Module CryptoBot API(non-official)**
**Docs:** https://help.crypt.bot/crypto-pay-api

**Install**
``` bash
pip install TeleCryptoBot
```

**Examples**
``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")

info_profile = crypto.getMe()
balance = crypto.getBalance()

print(info_profile, balance, sep='\n')
```
``` python
import TeleCryptoBot

crypto = TeleCryptoBot.TeleCryptoBot("0000:qwertyuiop")

invoice = crypto.createInvoice(asset="USDT", amount=1.0)
print(invoice)
```
