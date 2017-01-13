from __future__ import print_function
from pushbullet import Pushbullet
from urllib import urlencode
from urllib2 import Request
from urllib2 import urlopen
from pushbullet.errors import InvalidKeyError
from json import loads
from config import PUSHBULLET
from config import NEXMO


def send_pb(text):
    """
    Send Pushbullet notifications.

    Args:
        text (string): the text you want to send.

    """

    try:
        pb = Pushbullet(PUSHBULLET['API'])
        s7 = pb.devices[1]  # Gets the device to sent the alert
    except InvalidKeyError:
        print('Wrong Pushbullet API Key')
    except IndexError:
        print('Your PB device doesnt exist')
    else:
        pb.push_note('Caixa.py', str(text), device=s7)
        print('PushBullet alert sent!')


def send_sms(text):
    """
    Send SMS alert.

    Args:
        text (string): the text you want to send.

    """
    NEXMO['PARAMS']['text'] = str(text)
    url = 'https://rest.nexmo.com/sms/json?' + urlencode(NEXMO['PARAMS'])
    request = Request(url)
    request.add_header('Accept', 'application/json')
    response = urlopen(request)

    # Error handling for NEXMO API
    if response.code == 200:
        data = response.read()
        # Decode JSON response from UTF-8
        decoded_response = loads(data.decode('utf-8'))
        # Check if your messages are success
        # print decoded_response
        messages = decoded_response['messages']
        for message in messages:
            if not message['status'] == '0':
                print('SMS Error: ' + message['error-text'])
            else:
                print('SMS alert sent!')

    else:
        print(
            'Unexpected http {code} response from nexmo API, check your config.py file'.response.code)


def alert_balance(old_balance, current_balance):
    """
    Send alert when the balance changes.

    Args:
        old_balance (float): The old balance previously scraped.
        current_balance (float): The new balance scraped.

    """
    if old_balance == current_balance:
        return 0

    if PUSHBULLET['ENABLED']:
        send_pb("Saldo Atual: " + str(current_balance) + "EUR\n"
                + "Saldo Anterior: " + str(old_balance) + "EUR")

    if NEXMO['ENABLED']:
        send_sms("Saldo Atual: " + str(current_balance) + "EUR\n"
                 + "Saldo Anterior: " + str(old_balance) + "EUR\n")

    else:
        print("Balance alert is disabled")

    return 0


def alert_me(transactions):
    """
    Send alert based on the transactions

    Alerts the end user based on the configuration file it can only use one
    method of alerting because we don't want to spam the user.

    Args:
        transactions (list): the list of transactions we want to alert

    """
    if not transactions:
        print("No new transactions")

    elif PUSHBULLET["ENABLED"]:
        for row in transactions:
            type_ = row[0]
            date = row[1]
            amount = row[2]

            send_pb("Tipo: " + type_ + " Data: " + date + " Montante: " + str(amount) + "EUR")

    elif NEXMO['ENABLED']:
        total = 0
        for row in transactions:
            amount = row[2]
            total += amount
        send_sms("Tens " + str(len(transactions)) + " novos movimentos\n" + "Total: "
                 + str(total) + "EUR\n")
    else:
        print("Transaction alert is disabled")
