import re

with open(r"C:\Users\Administrator\Desktop\1.txt", "r", encoding="utf-8") as f:
    line = f.readline().rstrip()
    list1 = []
    regexp = re.compile(r"(\d+)")
    # 匹配中文
    regexp1 = r"[\u4e00-\u9fa5]+"

    while line:
        # print(line)
        str3 = re.search(regexp1, line)
        print(str3.group())
        line = f.readline().rstrip()