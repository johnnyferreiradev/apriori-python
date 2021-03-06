import pandas as pd
import openpyxl
from mlxtend.frequent_patterns import apriori, association_rules
import sys
import numpy as np

# loading dataset
wookbook = openpyxl.load_workbook("dataset.xlsx")
worksheet = wookbook.active

columns = []
dataset = []

for i in range(0, worksheet.max_row):
    row_values = []
    for col in worksheet.iter_cols(1, worksheet.max_column):
        if i == 0:
            columns.append(col[i].value)
        if i > 0:
            row_values.append(col[i].value)
    if i > 0:
        dataset.append(row_values)

df = pd.DataFrame(dataset, columns=columns)

class Apriori:
    """Apriori Class. Its has Apriori steps."""
    threshold = 0.4
    df = None

    def __init__(self, df, threshold=None, transform_bol=False):
        """Apriori Constructor. 

        :param pandas.DataFrame df: transactions dataset (1 or 0).
        :param float threshold: set threshold for min_support.
        :return: Apriori instance.
        :rtype: Apriori
        """

        self._validate_df(df)

        self.df = df
        if threshold is not None:
            self.threshold = threshold

        if transform_bol:
            self._transform_bol()

    def _validate_df(self, df=None):
        """Validade if df exists. 

        :param pandas.DataFrame df: transactions dataset (1 or 0).
        :return: 
        :rtype: void
        """

        if df is None:
            raise Exception("df must be a valid pandas.DataDrame.")


    def _transform_bol(self):
        """Transform (1 or 0) dataset to (True or False). 

        :return: 
        :rtype: void
        """

        for column in self.df.columns:
            self.df[column] = self.df[column].apply(lambda x: True if x == 1 else False)


    def _apriori(self, use_colnames=False, max_len=None, count=True):
        """Call apriori mlxtend.frequent_patterns function. 

        :param bool use_colnames: Flag to use columns name in final DataFrame.
        :param int max_len: Maximum length of itemsets generated.
        :param bool count: Flag to count length of the itemsets.
        :return: apriori DataFrame.
        :rtype: pandas.DataFrame
        """
    
        apriori_df = apriori(
                    self.df, 
                    min_support=self.threshold,
                    use_colnames=use_colnames, 
                    max_len=max_len,
                )
        if count:
            apriori_df['length'] = apriori_df['itemsets'].apply(lambda x: len(x))

        return apriori_df

    def run(self, use_colnames=False, max_len=None, count=True):
        """Apriori Runner Function.

        :param bool use_colnames: Flag to use columns name in final DataFrame.
        :param int max_len: Maximum length of itemsets generated.
        :param bool count: Flag to count length of the itemsets.
        :return: apriori DataFrame.
        :rtype: pandas.DataFrame
        """

        return self._apriori(
                        use_colnames=use_colnames,
                        max_len=max_len,
                        count=count
                    )

    def filter(self, apriori_df, length, threshold):
        """Filter Apriori DataFrame by length and  threshold.

        :param pandas.DataFrame apriori_df: Apriori DataFrame.
        :param int length: Length of itemsets required.
        :param float threshold: Minimum threshold nrequired.
        :return: apriori filtered DataFrame.
        :rtype:pandas.DataFrame
        """
        
        if 'length' not in apriori_df.columns:
            raise Exception("apriori_df has no length. Please run the Apriori with count=True.")

        return apriori_df[ (apriori_df['length'] == length) & (apriori_df['support'] >= threshold) ]


if 'ID' in df.columns: del df['ID'] # ID is not relevant to apriori 

apriori_runner = Apriori(df, threshold=0.1, transform_bol=True)
apriori_df = apriori_runner.run(use_colnames=True)
print(apriori_df)
apriori_df.to_excel('apriori_df.xlsx')

association_rules_result = association_rules(apriori_df, metric='confidence', min_threshold=0.1, support_only=False)
print(' ')
print(association_rules_result)
association_rules_result.to_excel('association_rules_result.xlsx')