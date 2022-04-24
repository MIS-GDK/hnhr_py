import re

with open(
    r"C:\Users\Administrator\Desktop\timeErp-INFO-2021-11-18.0.log",
    "r",
    encoding="utf-8",
) as f:
    set1 = set()
    with open(r"C:\Users\Administrator\Desktop\1.txt", "w+", encoding="utf-8") as f2:
        line = f.readline()
        # str1 = re.search("英克销售发票单细单ID不存在------退单号为：", line)
        # print(str1)
        while line:
            str1 = re.search("英克销售发票单细单ID不存在------退单号为：", str(line))
            if str1:
                find_str = str(line).strip()[list(str1.span())[1] :]
                l1 = len(set1)
                set1.add(find_str)
                if l1 != len(set1):
                    f2.write(find_str + "\n")
            line = f.readline()
