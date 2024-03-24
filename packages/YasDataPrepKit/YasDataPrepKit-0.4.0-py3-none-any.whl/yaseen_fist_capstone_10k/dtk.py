import pandas as pd

# I used .set_option() to display all columns and rows of my data
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class ReadingData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data_df = None

    def read(self):
        # In here I used the .split() function to split my separate the file extension to select the appropriate read function
        extension = self.file_path.split('.')[-1]
        if extension == 'json':
            self.data_df = self._read_json()
        elif extension == 'csv':
            self.data_df = self._read_csv()
        else:
            print("Invalid file extension")
        return self.data_df

    def _read_json(self):
        return pd.read_json(self.file_path)

    def _read_csv(self):
        return pd.read_csv(self.file_path)

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
            print("No data loaded. Please call the read() method first.")

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
            encoding = pd.get_dummies(self.data_df)
            print(encoding)
        else:
            print("No data loaded. Please call the read() method first.")

    def calculate_mean(self):
        if self.data_df is not None:
            numerical_columns = self.data_df.select_dtypes(include=['int', 'float'])
            means = numerical_columns.mean()
            print("The mean for each numerical column:")
            print(means)
        else:
            print("No data loaded. Please call the read() method first.")

    def calculate_sum(self):
        if self.data_df is not None:
            numerical_columns = self.data_df.select_dtypes(include=['int', 'float'])
            numerical_columns_sum = numerical_columns.sum()
            print("The sum for each numerical column:")
            print(numerical_columns_sum)
        else:
            print("No data loaded. Please call the read() method first.")


""" Example on how to use 
read_data = ReadingData(r"your file path")
data_df = read_data.read()
read_data.handle_missing_values("remove")
print(read_data.data_df)"""
