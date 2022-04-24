from pypinyin import pinyin
import pyodbc

# 输入name
def get_pinyin_first_alpha(name):
    return "".join([i[0][0].upper() for i in pinyin(name)])


list1 = []

with open(r"C:\Users\Administrator\Desktop\1.txt", encoding="utf-8") as f1:
    line = f1.readline()
    while line:
        list1.append(line.split())
        line = f1.readline()

print(list1[0])
print(pyodbc.drivers())
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=192.168.0.16;DATABASE=ysdata;UID=ysadmin;PWD=0wM71IakpU&1s&"
)

cursor = conn.cursor()
# cursor.execute(
#     "select  RTRIM(s.spmch),RTRIM(zjm),beactive,RTRIM(yishj),RTRIM(jingd),RTRIM(chbjs),RTRIM(shpchd),RTRIM(shengccj),RTRIM(bzqfs) from dbo.spkfk s where s.spid <> 'X'  and s.sptm like '分销部' and s.beactive = '是' order by s.spid DESC"
# )
# list1 = cursor.fetchall()
# print(list1)
mynumber = 2740
# mynumber2 = 100
str1 = "SPH0000"
# print(list1[1][0])
for mylist in list1:
    # print(mylist)
    mysqlstr = "insert into spkfk(spid,spbh,sptm,spmch,zjm,beactive,shpchd,shengccj,hshjj,jj,shj,lshj,zgshj,hshsj,jsj) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
        str1 + str(mynumber),
        mylist[0],
        mylist[2],
        mylist[1],
        get_pinyin_first_alpha(mylist[1]),
        '是',
        mylist[3],
        mylist[2],
        '1','1','1','1','1','1','1'
    )
    # print(mysqlstr)
    cursor.execute(mysqlstr)
    mynumber = mynumber + 1
# 提交
conn.commit()
# 关闭连接
conn.close()