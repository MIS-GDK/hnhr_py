from pypinyin import pinyin
import pyodbc

# 输入name
def get_pinyin_first_alpha(name):
    return "".join([i[0][0].upper() for i in pinyin(name)])


list1 = []

with open(r"C:\Users\Administrator\Desktop\budget_system.txt", encoding="utf-8") as f1:
    line = f1.readline()
    while line:
        list1.append(line.split())
        line = f1.readline()

print(pyodbc.drivers())
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=192.168.0.16;DATABASE=ysdata;UID=ysadmin;PWD=0wM71IakpU&1s&"
)

cursor = conn.cursor()
mynumber = 19926
str1 = "BM000"
for mylist in list1:
    print(mylist)
    mysqlstr = "insert into bmdoc(bmid,bmbh,bm,zjm,hw,denglrq,beactive) values ('%s','%s','%s','%s','%s','%s','%s')" % (
        str1 + str(mynumber),
        mylist[0],
        mylist[1] + mylist[0],
        get_pinyin_first_alpha(mylist[1]),
        "",
        "",
        "是",
    )
    # print(mysqlstr)
    cursor.execute(mysqlstr)
    mynumber = mynumber + 1
# 提交
conn.commit()
# 关闭连接
conn.close()