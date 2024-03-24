import pandas as pd
import numpy as np
import re

# I used .set_option() to display all columns and rows of my data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class ReadingData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_df = None

    def read(self):
        # In here I used the .split() function to separate the file extension to select the appropriate read function
        extension = self.file_path.split('.')[-1]
        if extension == 'json':
            self.data_df = self._read_json()
        elif extension == 'csv':
            self.data_df = self._read_csv()
        elif extension == 'excel':
            self.data_df = self._read_csv()
        else:
            print("Invalid file extension")
        return self.data_df

    def _read_json(self):
        return pd.read_json(self.file_path, orient='index')

    def _read_csv(self):
        return pd.read_csv(self.file_path, sep=',')

    def _read_excel(self):
        return pd.read_excel(self.file_path)

    def handle_missing_values(self, strategy):
        # This function takes one parameter to check whether to remove or impute missing values
        # Also added a condition to check whether data_df has any data or not
        if self.data_df is not None:
            if strategy == 'remove':
                self.values_remove()
            elif strategy == 'impute':
                self.values_impute()
            else:
                print("Invalid strategy. Please choose 'remove' or 'impute'.")

        else:
            print("No data loaded. please make sure you called the read() method")

    def values_remove(self):
        self.data_df = self.data_df.select_dtypes(include=['int', 'float']).dropna()
        print("Number of NaN values after handling missing values:")
        print(self.data_df.isnull().sum())

    def values_impute(self):
        numerical_columns = self.data_df.select_dtypes(include=['int', 'float'])
        self.data_df = numerical_columns.fillna(numerical_columns.mean())
        print("Number of NaN values after handling missing values:")
        print(self.data_df.isnull().sum())

    def encode_categorical_data(self):
        # In here I used the one_hot encoding which categorize my columns and rows in a certain way and gives me binary output
        if self.data_df is not None:
            return pd.get_dummies(self.data_df)
        else:
            print("No data loaded. please make sure you called the read() method")

    def calculate_mean(self):
        if self.data_df is not None:
            numerical_columns = self.data_df.select_dtypes(include=['int', 'float'])
            return f"The mean for the column: {numerical_columns.mean()}"
        else:
            print("No data loaded. please make sure you called the read() method")

    def calculate_sum(self):
        if self.data_df is not None:
            numerical_columns = self.data_df.select_dtypes(include=['int', 'float'])
            return f"The sum for the column: {numerical_columns.sum()}"
        else:
            print("No data loaded. please make sure you called the read() method")

    def max_min_value(self):
        if self.data_df is not None:
            max_min_num = self.data_df.select_dtypes(include=['int', 'float'])
            max_num = max_min_num.max()
            min_num = max_min_num.min()
            return f"The Maximum{max_num}\nand the Minimum{min_num}"
        else:
            print("No data loaded. please make sure you called the read() method")

    def median_value(self):
        if self.data_df is not None:
            median_num = self.data_df.select_dtypes(include=['int', 'float'])
            return f"The median is: {median_num.median()}"
        else:
            print("No data loaded. please make sure you called the read() method")

    def mode_value(self):
        if self.data_df is not None:
            mode_num = self.data_df.select_dtypes(include=['int', 'float'])
            return f"The mode is: {mode_num.mode()}"
        else:
            print("No data loaded. please make sure you called the read() method")

    def var_value(self):
        if self.data_df is not None:
            var_num = self.data_df.select_dtypes(include=['int', 'float'])
            var_num = np.var(var_num, axis=0)
            return f"The variance is: {var_num}"
        else:
            print("No data loaded. Please make sure you called the read() method")

    def std_deviation(self):
        if self.data_df is not None:
            std_dev = self.data_df.select_dtypes(include=['int', 'float'])
            std_dev = np.std(std_dev, axis=0)
            return f"The standard deviation is: {std_dev}"
        else:
            print("No data loaded. Please make sure you called the read() method")

    def cor_coefficient(self):
        if self.data_df is not None:
            cor_coef = self.data_df.select_dtypes(include=['int', 'float'])
            cor_coef = np.std(cor_coef, axis=0) / np.mean(cor_coef)
            return f"The correlation coefficient is: {cor_coef}"
        else:
            print("No data loaded. Please make sure you called the read() method")


read_data = ReadingData(r"E:\Business_Data.csv")
df = read_data.read()
print(df)
print(read_data.cor_coefficient())
