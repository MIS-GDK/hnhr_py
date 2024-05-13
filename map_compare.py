import operator
from collections import defaultdict

d1 = defaultdict(list)
d2 = defaultdict(list)
with open(r"C:\Users\Administrator\Desktop\1.txt", encoding="utf-8") as f1:
    line = f1.readline().strip()
    while line:
        id, sum1 = line.split()
        d1[id].append(float(sum1))
        line = f1.readline().strip()

with open(r"C:\Users\Administrator\Desktop\2.txt", encoding="utf-8") as f2:
    line2 = f2.readline().strip()
    while line2:
        id, sum1 = line2.split()
        d2[id].append(float(sum1))
        line2 = f2.readline().strip()
# 需要先比较两个dict的大小，以大的为基本进行比较
# f = lambda x, y: x if len(x) > len(y) else y
sum2 = 0
total = 0
total2 = 0

for i in set(d1.keys()) | set(d2.keys()):
    if round(sum(d1[i]), 2) != round(sum(d2[i]), 2):
        print(
            "key:%s,驾驶舱: %s,用户: %s"
            % (i, round(sum(d1[i]), 2), round(sum(d2[i]), 2))
        )

        total += sum(d1[i]) - sum(d2[i])

print(total)

for i in set(d1.keys()) | set(d2.keys()):
    if round(sum(d1[i]), 2) != round(sum(d2[i]), 2):
        print(i + ",")
# for i in f(d1, d2).keys():
#     result = set(d1[i]) ^ set(d2[i])
#     mylist = [int(i) for i in result]
#     # for i in mylist:
#     #     print(i, type(i))
#     # print(mylist)
#     if result:
#         result.discard(0)
#         # print(mylist)
#         if result:
#             # print(i)
#             # print("key:%s,values:%s" % (i, result))
#             # print("key:%s,values1:%s,values2:%s,result:%s" % (i, d1[i], d2[i], result))
#             print("key:%s,result:%s" % (i, result))
#             print(int(sum(mylist)))
#             sum2 = sum2 + int(sum(mylist))
# print(sum2)
