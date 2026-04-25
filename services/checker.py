from time import sleep

from consts import bank as BankConsts
from exceptions import bank as CheckerExceptions
from helpers import bank as CheckerHelpers

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckAccount:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://vcbdigibank.vietcombank.com.vn/auth")
        wait = WebDriverWait(self.driver, 60)  # Wait for up to 60 seconds
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'home-page'))  # Change 'dashboard' to an actual element ID after login
        )
        sleep(2)
        self.driver.get("https://vcbdigibank.vietcombank.com.vn/transfer/domestic")
        sleep(2)
        self.bank_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["bank_input"])
        
    def _choose_bank(self, bank: str):
        self.bank_input.clear()
        self.bank_input.send_keys("a")

        bank_scroll = self.driver.find_element(By.XPATH, BankConsts.BankXPath["bank_scroll"])
        self.driver.execute_script("arguments[0].scrollTop = 0;", bank_scroll)

        bank_found = False

        while not bank_found:
            try:
                bank = bank_scroll.find_element(By.XPATH, BankConsts.BankXPath.get(CheckerHelpers.clean_bank_name(bank=bank)))

                bank_found = True
                bank.click()
            except:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 72", bank_scroll)
                sleep(0.1)

        sleep(2)
        # sleep(1)
        # bank_input.send_keys(Keys.RETURN)
        # sleep(1)

    def _input_account(self, account: str):
        self._did_model_appear()
        account_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["account_input"])
        account_input.clear()
        sleep(5)
        self._did_model_appear()
        account_input.send_keys(account)
        account_input.send_keys(Keys.RETURN)
        sleep(5)

    def _did_model_appear(self) -> bool:
        # TODO: need checking if work?
        try:
            modal = self.driver.find_element(By.XPATH, BankConsts.BankXPath["modal"])
            sleep(0.5)
            retry_btn = modal.find_element(By.XPATH, BankConsts.BankXPath["modal_retry"])
            retry_btn.click()
            sleep(0.5)
            return True
        except:
            return False
        
    
    def _get_name_on_web(self) -> str:
        name_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["name_input"])
        sleep(1)
        return name_input.get_attribute("value")

    def check_account(self, name: str, account: str, bank: str) -> tuple[str, str]:
        try:
            self._choose_bank(bank=bank)
            self._input_account(account)
            # check if no account
            if self._did_model_appear():
                raise CheckerExceptions.CannotFoundAccount("Không tìm được account hoặc vượt limit")

            name_on_bank = self._get_name_on_web()
            account_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["account_input"])
            account_input.clear()

            if CheckerHelpers.uppercase_to_lower(name_on_bank) != CheckerHelpers.vietnamese_to_lower(name):
                raise CheckerExceptions.AccountNotMatch(name_on_bank, "Tên không khớp")
            
            return name_on_bank, "Thành công"
        
        except CheckerExceptions.CannotFoundAccount as e1:
            return "", e1.args[0]
        
        except CheckerExceptions.AccountNotMatch as e2:
            return e2.account, e2.args[0]
            

    def perform_checking(self, name: str, account: str, bank: str):
        try: 
            return self.check_account(name, account, bank)
        except:
            return "", "Không thành công"


    def teardown_method(self):
        self.driver.quit()