from services.checker import CheckAccount
from services.excel import ExcelService
import time

if __name__ == "__main__":
    checker = CheckAccount()
    # Colunms: MÃ NV	TÊN NHÂN VIÊN HƯỞNG	SỐ TÀI KHOẢN
    excel = ExcelService("CHECK STK T06.2025.xlsx", "Sheet1")
    excel.prepare_wb()
    name_col = 2  # Column index for names (TÊN NHÂN VIÊN HƯỞNG)
    account_col = 3  # Column index for account numbers (SỐ TÀI KHOẢN)
    curr_row = 149

    end_row = min(curr_row + 100, excel.get_max_row + 1)  # Limit to 50 rows for testing

    for row in range(curr_row + 1, end_row):
        name = excel.read_data(row=row, column=name_col)
        account = excel.read_data(row=row, column=account_col)
        if name == account == None:
            break
        
        name_on_web, result = checker.perform_checking(name, account)
        print(row, name, name_on_web, result)

        excel.write_data(row, excel.get_max_column - 1, name_on_web)
        excel.write_data(row, excel.get_max_column, result)
        
        time.sleep(10)


        # print(name, account)
    excel.save()
    checker.teardown_method()
