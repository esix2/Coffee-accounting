import pandas as pd
def personBalance(Person): 
        df = pd.read_csv('PeopleBalance') 
        names = df['Name']
	return float(df.loc[names == Person,'Balance'])

