from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from config import ACCOUNT_NR
from account import Account
from alerts import alert_balance
from alerts import alert_me
from argparse import ArgumentParser
from selenium.common.exceptions import NoSuchElementException
from os import sys

driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/login.seam")


# Function responsable for getting the login details from the arguments of the
# script. We need both the username and password otherwise the script wont run.
def read_user_pw():
    parser = ArgumentParser()
    parser.add_argument('-u', '--username', help="Nome de utilizador da caixadirecta", required=True)
    parser.add_argument('-p', '--password', help="Password para o nome de utilizador", required=True)
    args = vars(parser.parse_args())

    return args

def selenium_op(username, password):
    ## Login commands
    driver.find_element_by_id('loginForm:username').send_keys(username)
    driver.find_element_by_id('loginForm:password').send_keys(password)
    driver.find_element_by_id('loginForm:submit').click()

    ## Select account
    driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/private/contasordem/asminhascontas/movimentos/movimentos.seam")
    try:
        select = Select(driver.find_element_by_id('consultaMovimentosForm:selConta'))

    except  NoSuchElementException:
        print ('Wrong username/password')
        sys.exit(0)

    try:
        select.select_by_value(ACCOUNT_NR)

    except NoSuchElementException:
        print ('Wrong account number, please check the config.py file')
        sys.exit(0)

    ## Select account balance
    saldo_aux = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[2]/div[2]/label').text
    saldo = float(saldo_aux.replace(" EUR", "").replace(".", "").replace(",", "."))

    ## Select table of moviments
    table = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[3]/table/tbody')
    try:
        rows = table.find_elements(By.TAG_NAME, 'tr') # Select all rows from the table

    except NoSuchElementException: # If it cant select a row it means there arent any moviments
        return Account()

    transaction = []

    ## For each row extract the type, date and value of the transaction
    for row in rows:
        fstcol = row.find_elements(By.TAG_NAME, 'td')[0].text.split('\n')
        tipo = fstcol[0] # the type is always before the <br> tag
        data = fstcol[1] # the date is always after the <br> tag

        ## Convert the string to a float ex: "-200,00" to -200.00
        montante = float(row.find_elements(By.TAG_NAME, 'td')[1].text.replace(" ", "").replace(",", "."))

        transaction.append((tipo, data, montante))



    driver.quit()

    return Account(transactions=transaction, saldo=saldo)

def main():
    args = read_user_pw()
    old_account = Account.load() # Load the previous transactions and balance
    new_account = selenium_op(args['username'], args['password']) # gets the new
    alert_balance(old_account.saldo, new_account.saldo) # lets alert the user
    old_account.update(new_account)
    old_account.save()
    alert_me(old_account.new_mov) # sends alert with the new transactions

if __name__ == '__main__':
    main()
