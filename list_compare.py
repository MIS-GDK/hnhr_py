list1 = []
list2 = []
with open(r"C:\Users\Administrator\Desktop\1.txt", encoding="utf-8") as f1:
    line = f1.readline()
    while line:
        list1.append(line.strip())
        line = f1.readline()

with open(r"C:\Users\Administrator\Desktop\2.txt", encoding="utf-8") as f2:
    line = f2.readline()
    while line:
        list2.append(line.strip())
        line = f2.readline()
# print(len(set(list2)))
# result = set(list1) ^ set(list2)
result = set(list1) & set(list2)
print(len(result))
for i in result:
    print(i)
