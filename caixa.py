from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from argparse import ArgumentParser
from selenium.common.exceptions import NoSuchElementException
from os import sys
from config import ACCOUNT_NR
from account import Account
from alerts import alert_balance
from alerts import alert_me
from excel import create_excel


def read_user_pw():
    """
    Read the username and password

    Returns:
        args (dict): stores the username and password values

    """
    parser = ArgumentParser()
    parser.add_argument('-u', '--username',
                        help='Nome de utilizador da caixadirecta',
                        required=True)
    parser.add_argument('-p', '--password',
                        help='Password para o nome de utilizador.')
    parser.add_argument('--excel',
                        help='Cria ficheiro em excel com movimentos.',
                        action='store_true')
    parser.add_argument('-f', '--file',
                        help='The name of the file you want to create.')

    args = vars(parser.parse_args())

    return args


def caixa_scraper(username, password):
    """
    Scrapes data.

    This function is used to get all the data from our transactions most recent
    transactions.

    Args:
        username (string): username used to login.
        password (string): password used to login.

    Returns:
        Account with the transactions and the current balance.

    """
    driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
    driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/login.seam")

    # Login commands
    driver.find_element_by_id('loginForm:username').send_keys(username)
    driver.find_element_by_id('loginForm:password').send_keys(password)
    driver.find_element_by_id('loginForm:submit').click()

    # Select account
    driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/private/contasordem/asminhascontas/movimentos/movimentos.seam")
    try:
        select = Select(driver.find_element_by_id('consultaMovimentosForm:selConta'))

    except NoSuchElementException:
        print('Wrong username/password')
        sys.exit(0)

    try:
        select.select_by_value(ACCOUNT_NR)

    except NoSuchElementException:
        print('Wrong account number, please check the config.py file')
        sys.exit(0)

    # Select account balance
    saldo_aux = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[2]/div[2]/label').text
    saldo = float(saldo_aux.replace(" EUR", "").replace(".", "").replace(",", "."))

    # Select table of moviments
    table = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[3]/table/tbody')
    try:
        rows = table.find_elements(By.TAG_NAME, 'tr')  # Select all rows from the table

    except NoSuchElementException:  # If it cant select a row it means there arent any moviments
        return Account()

    transaction = []

    # For each row extract the type, date and value of the transaction
    for row in rows:
        fstcol = row.find_elements(By.TAG_NAME, 'td')[0].text.split('\n')
        tipo = fstcol[0]  # the type is always before the <br> tag
        data = fstcol[1]  # the date is always after the <br> tag

        # Convert the string to a float ex: "-200,00" to -200.00
        montante = float(row.find_elements(By.TAG_NAME, 'td')[1].text.replace(" ", "").replace(",", "."))

        transaction.append((tipo, data, montante))

    driver.quit()

    return Account(transactions=transaction, saldo=saldo)


def main():
    args = read_user_pw()
    file_name = args['username']

    # you should use a filename if we have one
    if args['file']:
        file_name = args['file']

    old_account = Account.load(file_name)

    # if we get a password we can scrape the data
    if args['password']:
        new_account = caixa_scraper(args['username'], args['password'])
        alert_balance(old_account.saldo, new_account.saldo)
        old_account.update(new_account)
        old_account.save(file_name)
        alert_me(old_account.new_mov)

    # if excel flag is active lets create a table
    if args['excel']:
        data_exc = old_account.create_dict()
        create_excel(data_exc, file_name)


if __name__ == '__main__':
    main()
