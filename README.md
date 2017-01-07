# caixa.py

This is a very simple scraper made using selenium with Phantomjs as headless browser.
The script will log into caixadirecta mobile webpage and it will check the 10th most
recent transactions, it will then send you a notification using PushBullet API telling
you the new ones.

### Basic Configuration:
You should edit the config.py file with your caixadirecta credentials.
If you dont want the send PushBullet notifications you can edit the dict
to "ENABLED": False.
