import pandas as pd
df = pd.DataFrame({
    "A": ["foo", "foo", "foo", "foo", "foo",
          "bar", "bar", "bar", "bar"],
    "B": ["one", "one", "one", "two", "two",
          "one", "one", "two", "two"],
    "C": ["small", "large", "large", "small",
          "small", "large", "small", "small",
          "large"],
    "D": [1, 2, 2, 3, 3, 4, 5, 6, 7],
    "E": [2, 4, 5, 5, 6, 6, 8, 9, 9]})
count = df.shape[0]
pivot_table = df.pivot_table(index='A', columns='B', values='D', aggfunc='count')
pivot_table = pivot_table.apply(lambda x: x / count)
print(pivot_table)