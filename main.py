from services.checker import CheckAccount
from services.excel import ExcelService
from consts import bank as BankConsts
from helpers import bank as BankHelper
import time

if __name__ == "__main__":
    checker = CheckAccount()
    # Colunms: MÃ NV	TÊN NHÂN VIÊN HƯỞNG	SỐ TÀI KHOẢN NGÂN HÀNG HƯỞNG
    try:
        excel = ExcelService("CHECK STK OFFICE 04.2026.xlsx", "Sheet1")
        excel.prepare_wb()  
    except Exception as e:
        print(f"File Excel: {e}")
        exit(1)
    name_col = 3  # Column index for names (TÊN NHÂN VIÊN HƯỞNG)
    account_col = 4  # Column index for account numbers (SỐ TÀI KHOẢN)
    bank_col = 5 # Column index for bank name (NGÂN HÀNG HƯỞNG)
    curr_row = 8

    max_row = 277

    end_row = min(curr_row + 500, max_row + 1)  # Limit to 50 rows for testing
    not_found = 0

    # Check banks in file
    # for row in range(curr_row + 1, end_row):
    #     bank = excel.read_data(row=row, column=bank_col)
    #     banks_not_found = []
    #     if BankConsts.BankXPath.get(BankHelper.clean_bank_name(bank=bank)) == None:
    #         banks_not_found.append(bank)
        
    # if len(banks_not_found) != 0:
    #     print(f"{len(banks_not_found)} bank(s) not found:")
    #     for bank_not_found in banks_not_found:
    #         print(bank_not_found)
    #     exit(1)

    # # retry fail
    # fail_rows = [57,58]
    # for i in range(110, 121):
    #     fail_rows.append(i)

    # for row in fail_rows:
    #     name = excel.read_data(row=row, column=name_col)
    #     account = excel.read_data(row=row, column=account_col)
    #     bank = excel.read_data(row=row, column=bank_col)
    #     if name == None or account == None or bank == None:
    #         continue
        
    #     name_on_web, result = checker.perform_checking(name, account, bank)
    #     print(row, name, name_on_web, result)

    #     excel.write_data(row, excel.get_max_column - 1, name_on_web)
    #     excel.write_data(row, excel.get_max_column, result)
    #     excel.save()
    #     time.sleep(20)

    for row in range(curr_row + 1, end_row):
        name = excel.read_data(row=row, column=name_col)
        account = excel.read_data(row=row, column=account_col)
        # bank = excel.read_data(row=row, column=bank_col)
        bank = "mbbank"
        if name == None or account == None or bank == None:
            continue
        
        name_on_web, result = checker.perform_checking(name, account, bank)
        print(row, name, name_on_web, result)

        excel.write_data(row, excel.get_max_column - 1, name_on_web)
        excel.write_data(row, excel.get_max_column, result)
        excel.save()
        time.sleep(20)


    checker.teardown_method()
