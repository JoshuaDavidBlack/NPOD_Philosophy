import pandas as pd

df = pd.DataFrame({'age': [20, 32], 'state': ['NY', 'CA'], 'point': [64, 92]},
                  index=['Alice', 'Bob'])

for i in df['age']:
    print(i)
df['age']
