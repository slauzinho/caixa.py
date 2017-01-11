![caixa.py](http://i.imgur.com/XOeQUG9.png)
# Welcome to caixa.py

This is a very simple script that gives you the latest transactions for your CaixaDirecta Account.
- Gives you your current account balance.
- Gives you a list of your last transactions
- Sends an alerts using [Pushbullet](https://www.pushbullet.com) or [Nexmo SMS](https://www.nexmo.com)

Before using
------------
1. pip install -r requirements.txt
2. install [phantomjs](http://phantomjs.org/download.html)
3. configure the config.py file with the alerts details ([Pushbullet](https://www.pushbullet.com) API or [Nexmo SMS](https://www.nexmo.com) API)

Basic usage
------------
Simply put your account details as arguments when calling the script:
```bash
python caixa.py -u [username] -p [password]
```
Optional commands
------------------
- Create Excel files:
```bash
python caixa.py -u [username] --excel
```
By using the flag --excel we can create a table in Excel with our transactions and transactions date. If you dont choose a password   the script will create the file based on the data previously saved.

- Custom filenames
```bash
python caixa.py -u [username] -p [password] -f [filename]
```
```bash
python caixa.py -u [username] -f [filename] --excel
```
To do list
----------
- [x] Add sms alert
- [ ] Scan more then 1 account
- [ ] Generate an Excel table with all the transactions

