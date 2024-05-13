# Filename: func_doc.py
def printMax(x, y):
    """Prints the maximum of two numbers.

    The two values must be integers."""
    x = int(x)  # convert to integers, if possible
    y = int(y)
    if x > y:
        print(x, "is maximum")
    else:
        print(y, "is maximum")


printMax(3, 5)
print(printMax.__doc__)


import sys

print('The command line arguments are:')
for i in sys.argv:
    print(i)

print('\n\nThe PYTHONPATH is', sys.path, '\n')


i = "REPLICAT    RUNNING     R_EP_XT     00:00:00      00:00:01".split()
print(i)
print(str('00:00:00').split(":"))
