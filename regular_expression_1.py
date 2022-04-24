import re

str1 = "安徽省合肥市桃花工业园繁华大道与文山路交口工投立恒工业广场C2幢东第3-4层0551-65336493"
str2 = '<span class="read-count">阅读数：641</span>'
str3 = "020-85653333"
# 匹配带区号座机 区号是4+7 或者3+8格式 或者 匹配不带区号座机或者手机号
regexp1 = r"\d{3}-\d{8}|\d{4}-\d{7,8}|\d{7,11}"

regexp2 = r'(?<=<span class="read-count">阅读数：)\d+'

regexp3 = "0\d{3}-\d{8}$"
regexp4 = "(0\d{3})-(\d{8})"
pattern = re.compile(regexp4)

"""分割电话号码与住址"""
str_result1 = pattern.search(str1)
str_result2 = re.search(regexp3, str1)
print(str_result2)
print(str_result1.group(0))


pattern2 = re.compile(r"\d+")  # 查找数字
result2 = pattern2.findall("runoob 123 google 456")
result3 = pattern2.search("runoob 123 google 456")

print(result2, result3)
