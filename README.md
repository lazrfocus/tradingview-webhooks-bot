forked from robswc/tradingview-webhooks-bot and hacked/modified for my own use

# Tradingview-webhooks-bot

tradingview-webhooks-bot is a trading bot, written in python that allows users to place trades with tradingview's webhook alerts.

---
### Quick Start Guide

1. pip3 install ccxt flask pytz
2. pip3 install python-ftx **req. to be deleted soon**  (python-ftx from https://github.com/wanth1997/python-ftx.git)
12. install ftx-cli from https://github.com/duskcodes/ftx-cli **req. to be deleted soon**
3. create api_keys.py file and follow format of api_keys_example.py w/ the keys for your exchange
4. create/login to ngrok.com account
5. download and install latest ngrok
6. make sure ngrok is authenticated with authcode listed on ngrok install page

7. run `./ngrok http 5000` (or whichever port you want to use)
8. then run `webhook-bot.py` to start webhook server on 5000 (change port inside .py file)

9. bulk setup tradingview alerts using ./atat  https://github.com/alleyway/add-tradingview-alerts-tool
10. check .zshrc for example aliases for manual order entry aliases
11. run wallet and pnl to check wallet status and positions

commands: long [..], short [..], exlong [..], exshort [..], exlongs, exshorts, pnl_automonitor
```bash
	./atat add-alerts --delay 250 config_longenter.yml && ./atat add-alerts --delay 250 config_longadd.yml && ./atat add-alerts --delay 250 config_longexit.yml && ./atat add-alerts --delay 250 config_longtp.yml && ./atat add-alerts --delay 250 config_shortenter.yml && ./atat add-alerts --delay 250 config_shortadd.yml && ./atat add-alerts --delay 250 config_shortexit.yml && ./atat add-alerts --delay 250 config_shortTP.yml
```
12. **the tradingview webhook address will be the ngrok address + /webhook**
ie: https://1234-45-789-000-00.ngrok.io/webhook
