from services.checker import CheckAccount
from services.excel import ExcelService
import time

if __name__ == "__main__":
    checker = CheckAccount()
    # Colunms: STT	MÃ NV	TÊN NHÂN VIÊN HƯỞNG	SỐ TÀI KHOẢN
    excel = ExcelService("test.xlsx", "stk")
    excel.prepare_wb()
    name_col = 3  # Column index for names (TÊN NHÂN VIÊN HƯỞNG)
    account_col = 4  # Column index for account numbers (SỐ TÀI KHOẢN)

    for row in range(2, excel.get_max_row + 1):
        name = excel.read_data(row=row, column=name_col)
        account = excel.read_data(row=row, column=account_col)
        if name == account == None:
            break
        
        name_on_web, result = checker.perform_checking(name, account)
        print(name, name_on_web, result)
        time.sleep(2)

        excel.write_data(row, excel.get_max_column - 1, name_on_web)
        excel.write_data(row, excel.get_max_column, result)

        # print(name, account)

    excel.save()
    checker.teardown_method()
