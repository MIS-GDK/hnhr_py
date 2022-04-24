import re

with open(r"C:\Users\Administrator\Desktop\客户资料.txt", "r", encoding="utf-8") as f:
    line = f.readline().rstrip()
    list1 = []
    regexp = re.compile(r"(\d+)")
    # 匹配中文
    regexp1 = r"[\u4e00-\u9fa5]+"
    # 匹配数字
    regexp2 = r"[0-9]+"
    # 匹配带区号座机 区号是4+7 或者3+8格式 或者 匹配不带区号座机或者手机号
    regexp3 = r"\d{3}-\d{8}|\d{4}-\d{7,8}|\d{7,11}"
    while line:
        # print(line)
        list2 = line.split("\t")
        if len(line) != 0:
            """分割电话号码与住址"""
            str3 = re.search(regexp3, list2[2].replace("--", "-"))
            if str3 is None:
                list2.insert(3, "")
            else:
                list2.insert(3, str3.group())
            str4 = list2[2].replace(list2[3], "")
            list2[2] = str4.replace(" ", "")

            """分割银行信息"""
            str1 = re.split(regexp, list2[4].replace("-", ""))
            str1.pop()
            list2.pop(4)
            list2.append(str1[0])
            list2.append(str1[1])
            print(list2)
            with open(r"C:\Users\Administrator\Desktop\5.txt", "a+") as f2:
                for i in list2:
                    f2.write(i + "\t")
                f2.write("\n")
        line = f.readline().rstrip()