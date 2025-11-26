from services.checker import CheckAccount
from services.excel import ExcelService
import time

if __name__ == "__main__":
    checker = CheckAccount()
    # Colunms: MÃ NV	TÊN NHÂN VIÊN HƯỞNG	SỐ TÀI KHOẢN
    try:
        excel = ExcelService("ATM T10 2025 OFFICE (1).xlsx", "Sheet2")
        excel.prepare_wb()  
    except Exception as e:
        print(f"File Excel: {e}")
        exit(1)
    name_col = 3  # Column index for names (TÊN NHÂN VIÊN HƯỞNG)
    account_col = 4  # Column index for account numbers (SỐ TÀI KHOẢN)
    curr_row = 1

    max_row = 28

    end_row = min(curr_row + 150, max_row + 1)  # Limit to 50 rows for testing

    for row in range(curr_row + 1, end_row):
        name = excel.read_data(row=row, column=name_col)
        account = excel.read_data(row=row, column=account_col)
        if name == None or account == None:
            continue
        
        name_on_web, result = checker.perform_checking(name, account)
        print(row, name, name_on_web, result)

        excel.write_data(row, excel.get_max_column - 1, name_on_web)
        excel.write_data(row, excel.get_max_column, result)
        excel.save()
        time.sleep(20)


        # print(name, account)
    checker.teardown_method()
