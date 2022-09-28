import pandas as pd
import io


class DataFileReader:
    """The class reads an xslx and generates data entries"""

    def __init__(self, filename: str, sheet: str):
        """Initialize class

        Args:
            filename (str): name of the registrant file
            sheet (str): name of xlsx sheet with registrant info
        """
        self.df = pd.read_csv(
            io.StringIO(
                "" + pd.read_excel(filename, sheet_name=sheet).to_csv(index=False)
            ),
            header=None,
            skiprows=2,
        ).iloc[2:, [0, 1, 3]]

    def getData(self):
        """Generator that yields registrant information

        Yields:
            _type_: registration line entry for participant
        """
        for __, row in self.df.iterrows():
            name = str(row.iloc[0]) + " " + str(row.iloc[1])
            company = row.iloc[2]
            name = str(name).title()

            yield (name.title(), company)
