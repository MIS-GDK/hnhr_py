# s = ["a", "b", "c", "d"]
# content = " "
# content = ",".join(("'{0}'".format(w) for w in s))
# print(content)
from numpy.core.arrayprint import _leading_trailing
import pandas as pd
import numpy as np
import math

s = pd.Series([1, 3, 5, np.nan, 6, 8])
print(s[[0, 1]])

frame = pd.DataFrame(np.random.rand(4, 4), index=list("abcd"), columns=list("ABCD"))
# print(frame)
# print(frame["a":"b"])
# print(frame[0:1])
