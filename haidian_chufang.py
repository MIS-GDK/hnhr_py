import xlwt
import openpyxl
from openpyxl import load_workbook


def open_txt(address, filename):
    d1 = {}
    with open(address + "/" + filename, "r", encoding="UTF-8") as f:
        line = f.readline().strip()
        while line:
            id, sum1 = line.split()
            print(id, sum1)
            line = f.readline().strip()


def write_excel_xlsx(path, sheet_name):
    workbook = load_workbook(path)
    sheet = workbook.active
    lst = []
    lst1 = []
    for row in sheet:
        for cell in row:
            lst1.append(cell.value)
        lst.append(lst1)
        lst1 = []
    # print(lst[1:])

    with open("C:/Users/Administrator/Desktop/1.txt", "r", encoding="UTF-8") as f:
        line = f.readline().strip()
        while line:
            sales1, sale2 = line.split()
            for i in range(len(lst)):
                if lst[i][0] == sales1:
                    lst[i][1] = sale2
            line = f.readline().strip()
    for i in lst:
        print(i[1])
    workbook.save(path)


# open_txt("C:/Users/Administrator/Desktop", "1.txt")
write_excel_xlsx("C:/Users/Administrator/Desktop/10-11.xlsx", "Sheet2")
