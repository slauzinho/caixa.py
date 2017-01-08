from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from config import ACCOUNT_NR, PASSWORD, USERNAME, PUSHBULLET
from account import Account
from alerts import alert_balance
from alerts import alert_me

driver = webdriver.PhantomJS('/usr/local/bin/phantomjs')
driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/login.seam")

def selenium_op():
    ## Login commands
    driver.find_element_by_id('loginForm:username').send_keys(USERNAME)
    driver.find_element_by_id('loginForm:password').send_keys(PASSWORD)
    driver.find_element_by_id('loginForm:submit').click()

    ## Select account
    driver.get("https://m.caixadirecta.cgd.pt/cdoMobile/private/contasordem/asminhascontas/movimentos/movimentos.seam")
    select = Select(driver.find_element_by_id('consultaMovimentosForm:selConta'))
    select.select_by_value(ACCOUNT_NR)

    ## Select account balance
    saldo_aux = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[2]/div[2]/label').text
    saldo = float(saldo_aux.replace(" EUR", "").replace(".", "").replace(",", "."))

    ## Select table of moviments
    table = driver.find_element(By.XPATH, '//*[@id="consultaMovimentosForm"]/div[3]/table/tbody')
    rows = table.find_elements(By.TAG_NAME, 'tr') # Select all rows from the table

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

    return Account(transaction, saldo)

def main():
    a = Account([],0).load()
    b = selenium_op()
    alert_balance(a.saldo, b.saldo)
    a.update(b)
    a.save()
    alert_me(a.new_mov)


if __name__ == '__main__':
    main()
