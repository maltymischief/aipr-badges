import pandas as pd
import io

class DataFileReader():
    def __init__(self, filename, sheet):
        self.df = pd.read_csv(
            io.StringIO(
                u""+pd.read_excel(
                    filename, 
                    sheet_name=sheet).to_csv(index=False)), 
                    header=None, 
                    skiprows=2
        ).iloc[2:, [0,1,3]]

    def getData(self):    
        for __, row in self.df.iterrows():
            name = str(row.iloc[0]) + " " + str(row.iloc[1])
            company = row.iloc[2]
            name = str(name).title()
    
            yield (name.title(), company)

