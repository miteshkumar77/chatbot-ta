import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

var = pd.read_excel('A:\\DataEX.xls')
print(var)
mylist = var[20220232].tolist()
df = pd.DataFrame.from_dict(Counter(mylist), orient='index', columns=['number of queries'])
df.plot.bar(xticks=1)



