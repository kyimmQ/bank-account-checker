from time import sleep, time

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
        sleep(5)
        self.driver.get("https://vcbdigibank.vietcombank.com.vn/transfer/domestic")
        sleep(15)
        self._choose_bank()
        
    def _choose_bank(self):
        bank_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["bank_input"])
        bank_input.send_keys("a")

        bank_scroll = self.driver.find_element(By.XPATH, BankConsts.BankXPath["bank_scroll"])

        mbank_found = False

        while not mbank_found:
            try:
                bank = bank_scroll.find_element(By.XPATH, BankConsts.BankXPath["mbbank"])

                mbank_found = True
                bank.click()
            except:
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 5 * 72", bank_scroll)
                sleep(1)

        sleep(2)
        # sleep(1)
        # bank_input.send_keys(Keys.RETURN)
        # sleep(1)
    
    def _input_account(self, account: str):
        account_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["account_input"])
        account_input.clear()
        sleep(5)
        self._handle_dialogs()
        account_input.send_keys(account)
        account_input.send_keys(Keys.RETURN)

    def _handle_dialogs(self, quiet_seconds: int = 4, timeout: int = 40) -> bool:
        # Dismiss every dialog VCB shows until none appears for `quiet_seconds`.
        # Returns True if an error dialog ("Thử lại") was seen, i.e. the lookup failed.
        error_seen = False
        quiet = 0
        deadline = time() + timeout
        while quiet < quiet_seconds and time() < deadline:
            sleep(1)
            try:
                # card-like number: "same as card number, continue?" -> Tiếp tục
                btn = self.driver.find_element(By.XPATH, BankConsts.BankXPath["modal_card_continue"])
                # JS click: the button animation makes a native click flaky
                self.driver.execute_script("arguments[0].click();", btn)
                quiet = 0
                continue
            except:
                pass
            try:
                # lookup error dialog -> Thử lại
                self.driver.find_element(By.XPATH, BankConsts.BankXPath["modal"])
                retry_btn = self.driver.find_element(By.XPATH, BankConsts.BankXPath["modal_retry"])
                self.driver.execute_script("arguments[0].click();", retry_btn)
                error_seen = True
                quiet = 0
            except:
                quiet += 1
        return error_seen
        
    
    def _get_name_on_web(self) -> str:
        name_input = self.driver.find_element(By.XPATH, BankConsts.BankXPath["name_input"])
        sleep(1)
        return name_input.get_attribute("value")

    def check_account(self, name: str, account: str) -> tuple[str, str]:
        try:
            # card-style numbers (16+ digits) hit VCB's flaky card lookup, so retry them
            attempts = 3 if len(account) >= 16 else 1
            lookup_failed = True
            for _ in range(attempts):
                self._input_account(account)
                lookup_failed = self._handle_dialogs()
                if not lookup_failed:
                    break
            # no account, or the lookup errored every time
            if lookup_failed:
                raise CheckerExceptions.CannotFoundAccount("Không tìm được account hoặc vượt limit")

            name_on_bank = self._get_name_on_web()

            if CheckerHelpers.uppercase_to_lower(name_on_bank) != CheckerHelpers.vietnamese_to_lower(name):
                raise CheckerExceptions.AccountNotMatch(name_on_bank, "Tên không khớp")
            
            return name_on_bank, "Thành công"
        
        except CheckerExceptions.CannotFoundAccount as e1:
            return "", e1.args[0]
        
        except CheckerExceptions.AccountNotMatch as e2:
            return e2.account, e2.args[0]
            

    def perform_checking(self, name: str, account: str):
        try: 
            return self.check_account(name, account)
        except:
            return "", "Không thành công"


    def teardown_method(self):
        self.driver.quit()