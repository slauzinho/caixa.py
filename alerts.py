from pushbullet import Pushbullet
import urllib
import urllib2
from config import PUSHBULLET, NEXMO


def send_pb(text):
    pb = Pushbullet(PUSHBULLET['API'])
    s7 = pb.devices[1] # Gets the device to sent the alert
    pb.push_note("Caixa.py", str(text), device=s7)

# Sends an sms with a chosen text to the number provided on the config file
def send_sms(text):
    NEXMO["PARAMS"]["text"] = text
    url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(NEXMO['PARAMS'])
    request = urllib2.Request(url)
    request.add_header('Accept', 'application/json')
    response = urllib2.urlopen(request)

# Sends an alert to all enabled devices on the config file with the old balance
# and the new one.
def alert_balance(old_balance, current_balance):
    if old_balance == current_balance:
        return 0

    if PUSHBULLET['ENABLED']:
        send_pb("Saldo Atual: " + str(current_balance) + "EUR\n" \
                + "Saldo Anterior: " + str(old_balance) + "EUR")

    if NEXMO['ENABLED']:
        send_sms("Saldo Atual: " + str(current_balance)+ "EUR\n" \
                 + "Saldo Anterior: " + str(old_balance) + "EUR\n")

    else:
        print ("Balance alert is disabled")

    return 0

# Sends an alert to only one device, if you have Pushbullet enable you will not
# get an SMS alert.
def alert_me(transactions):
    if not transactions:
        print ("No new transactions")

    elif PUSHBULLET["ENABLED"]:
        for row in transactions:
            type_ = row[0]
            date = row[1]
            amount = row[2]

            send_pb("Tipo: "+ type_ + " Data: " + date + " Montante: " + str(amount) + "EUR")

        print ("Notifications sent!")

    elif NEXMO['ENABLED']:
        total = 0
        for row in transactions:
            amount = row[2]
            total += amount
        send_sms("Tens " + str(len(transactions)) + " novos movimentos\n" + "Total: " \
                 + str(amount) + "EUR\n")
    else:
        print ("Transaction alert is disabled")
