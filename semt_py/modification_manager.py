import pandas as pd
from dateutil import parser
import re

class ModificationManager:
    """
    A class to manage and apply various modifications to a DataFrame.

    This class provides methods to modify DataFrame columns, such as converting
    date formats, changing data types, and reordering columns. It also includes
    methods to retrieve information about available modifiers.
    """

    def __init__(self):
        self.modifiers = {
            'iso_date': self.iso_date,
            'lower_case': self.lower_case,
            'drop_na': self.drop_na,
            'rename_columns': self.rename_columns,
            'convert_dtypes': self.convert_dtypes,
            'reorder_columns': self.reorder_columns
        }

    def get_modifier_list(self):
        """
        Retrieve the list of available modifiers.

        Returns:
        -------
        list
            A list of available modifier names.

        Usage:
        -----
        manager = ModificationManager()
        modifier_list = manager.get_modifier_list()
        print(modifier_list)
        """
        return list(self.modifiers.keys())

    def get_modifier_description(self, modifier_name):
        """
        Retrieve the description of a specific modifier.

        Parameters:
        ----------
        modifier_name : str
            The name of the modifier.

        Returns:
        -------
        str
            A description of the modifier.

        Usage:
        -----
        manager = ModificationManager()
        description = manager.get_modifier_description('iso_date')
        print(description)
        """
        descriptions = {
            'iso_date': "Convert a date column to ISO 8601 format (YYYY-MM-DD).",
            'lower_case': "Convert all string values in a column to lowercase.",
            'drop_na': "Remove rows with missing values.",
            'rename_columns': "Rename columns according to a given mapping.",
            'convert_dtypes': "Convert column data types according to a given mapping.",
            'reorder_columns': "Reorder columns according to a specified order."
        }
        return descriptions.get(modifier_name, "Modifier not found.")

    def get_modifier_parameters(self, modifier_name):
        """
        Retrieve the parameters required for a specific modifier along with usage example.

        Parameters:
        ----------
        modifier_name : str
            The name of the modifier.

        Returns:
        -------
        dict
            A dictionary containing:
            - 'parameters': Dictionary of required parameters and their types
            - 'usage': String showing example usage of the modifier
            - 'example_values': Dictionary showing example values for each parameter

        Usage:
        -----
        manager = ModificationManager()
        info = manager.get_modifier_parameters('rename_columns')
        print(info['usage'])
        """
        parameter_info = {
            'iso_date': {
                'parameters': {'df': 'DataFrame', 'date_col': 'str'},
                'usage': "manager = ModificationManager()\ndf, message = manager.modify('iso_date', df=df, date_col='date_column')\n# or directly:\ndf, message = manager.iso_date(df, date_col='date_column')",
                'example_values': {'df': 'your_dataframe', 'date_col': "'2023-01-01'"}
            },
            'lower_case': {
                'parameters': {'df': 'DataFrame', 'column': 'str'},
                'usage': "manager = ModificationManager()\ndf = manager.modify('lower_case', df=df, column='text_column')\n# or directly:\ndf = manager.lower_case(df, column='text_column')",
                'example_values': {'df': 'your_dataframe', 'column': "'name_column'"}
            },
            'drop_na': {
                'parameters': {'df': 'DataFrame'},
                'usage': "manager = ModificationManager()\ndf = manager.modify('drop_na', df=df)\n# or directly:\ndf = manager.drop_na(df)",
                'example_values': {'df': 'your_dataframe'}
            },
            'rename_columns': {
                'parameters': {'df': 'DataFrame', 'column_rename_dict': 'dict'},
                'usage': "manager = ModificationManager()\ndf = manager.modify('rename_columns', df=df, column_rename_dict={'old_name': 'new_name'})\n# or directly:\ndf = manager.rename_columns(df, {'old_name': 'new_name'})",
                'example_values': {'df': 'your_dataframe', 'column_rename_dict': "{'old_name': 'new_name', 'old_name2': 'new_name2'}"}
            },
            'convert_dtypes': {
                'parameters': {'df': 'DataFrame', 'dtype_dict': 'dict'},
                'usage': "manager = ModificationManager()\ndf = manager.modify('convert_dtypes', df=df, dtype_dict={'column_name': 'int64'})\n# or directly:\ndf = manager.convert_dtypes(df, {'column_name': 'int64'})",
                'example_values': {'df': 'your_dataframe', 'dtype_dict': "{'age': 'int64', 'price': 'float64'}"}
            },
            'reorder_columns': {
                'parameters': {'df': 'DataFrame', 'new_column_order': 'list'},
                'usage': "manager = ModificationManager()\ndf = manager.modify('reorder_columns', df=df, new_column_order=['col1', 'col2'])\n# or directly:\ndf = manager.reorder_columns(df, ['col1', 'col2'])",
                'example_values': {'df': 'your_dataframe', 'new_column_order': "['id', 'name', 'age']"}
            }
        }
        
        modifier_info = parameter_info.get(modifier_name, "Modifier not found.")
        return self._format_modifier_info(modifier_info)

    def _format_modifier_info(self, modifier_info):
        """
        Formats the modifier information into a readable, structured output.

        Parameters:
        ----------
        modifier_info : dict
            Information dictionary about the modifier, including parameters,
            usage, and example values.

        Returns:
        -------
        str
            A formatted string with readable output.
        """
        if isinstance(modifier_info, str):
            return modifier_info  # Handles the "Modifier not found." case
        
        # Extract components for better readability
        parameters = modifier_info.get('parameters', {})
        usage = modifier_info.get('usage', 'No usage information available')
        example_values = modifier_info.get('example_values', {})

        # Create formatted output
        formatted_output = "### Modifier Information\n"
        formatted_output += "\n**Parameters:**\n"
        for param, dtype in parameters.items():
            example = example_values.get(param, "N/A")
            formatted_output += f" - `{param}` ({dtype}): e.g., `{example}`\n"

        formatted_output += f"\n**Usage Example:**\n```\n{usage}\n```\n"
        
        return formatted_output

    def modify(self, modifier_name, **kwargs):
        """
        Apply a specified modifier to a DataFrame.

        Parameters:
        ----------
        modifier_name : str
            The name of the modifier to apply.
        kwargs : dict
            The parameters required by the modifier.

        Returns:
        -------
        pd.DataFrame
            The modified DataFrame.

        Raises:
        ------
        ValueError
            If the modifier is not found or if parameters are missing.

        Usage:
        -----
        manager = ModificationManager()
        df, message = manager.modify('iso_date', df=df, date_col='Fecha_id')
        print(message)
        """
        if modifier_name not in self.modifiers:
            raise ValueError(f"Modifier '{modifier_name}' not found.")
        
        modifier = self.modifiers[modifier_name]
        return modifier(**kwargs)

    @staticmethod
    def iso_date(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
        """
        Convert a given date column in a DataFrame to ISO 8601 date format (YYYY-MM-DD).
        If the column is already formatted correctly, no changes are made.
        
        Parameters:
        - df (pd.DataFrame): Input DataFrame containing the date column.
        - date_col (str): Name of the date column to be converted.

        Returns:
        - pd.DataFrame: DataFrame with the date column converted to ISO 8601 date format.
        - str: Message indicating if any changes were made or if the column was already formatted.

        Raises:
        - ValueError: If the column does not exist or contains invalid dates.

        Usage:
        -----
        manager = ModificationManager()
        df, message = manager.iso_date(df, 'Fecha_id')
        print(message)
        """
        if date_col not in df.columns:
            raise ValueError(f"Column '{date_col}' does not exist in the DataFrame.")
        
        iso_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        if df[date_col].apply(lambda x: bool(iso_pattern.match(str(x)))).all():
            return df, "Input is already formatted correctly as ISO 8601 (YYYY-MM-DD)."

        def parse_date_safe(date_str):
            try:
                parsed_date = parser.parse(str(date_str), fuzzy=True)
                return parsed_date.strftime('%Y-%m-%d')
            except (ValueError, TypeError):
                return None

        df[date_col] = df[date_col].apply(parse_date_safe)

        if df[date_col].isnull().any():
            invalid_rows = df[df[date_col].isnull()].index.tolist()
            raise ValueError(f"Column '{date_col}' contains invalid date values that could not be converted. "
                             f"Invalid rows: {invalid_rows}")

        return df, "Date column successfully converted to ISO 8601 format."
    
    @staticmethod
    def lower_case(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Convert all string values in a specified column of a DataFrame to lowercase.

        Parameters:
        - df (pd.DataFrame): Input DataFrame containing the column to be modified.
        - column (str): Name of the column to convert to lowercase.

        Returns:
        - pd.DataFrame: DataFrame with the specified column converted to lowercase.

        Raises:
        - ValueError: If the column does not exist or is not of string type.

        Usage:
        -----
        manager = ModificationManager()
        df = manager.lower_case(df, 'column_name')
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
        
        if not pd.api.types.is_string_dtype(df[column]):
            raise ValueError(f"Column '{column}' is not of string type.")
        
        df[column] = df[column].str.lower()
        return df

    @staticmethod
    def drop_na(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove all rows from a DataFrame that contain any missing (NaN) values.

        Parameters:
        - df (pd.DataFrame): Input DataFrame from which to drop rows with missing values.

        Returns:
        - pd.DataFrame: DataFrame with rows containing missing values removed.

        Usage:
        -----
        manager = ModificationManager()
        df = manager.drop_na(df)
        """
        df.dropna(inplace=True)
        return df

    @staticmethod
    def rename_columns(df: pd.DataFrame, column_rename_dict: dict) -> pd.DataFrame:
        """
        Rename columns in a DataFrame according to a given dictionary mapping.

        Parameters:
        - df (pd.DataFrame): Input DataFrame with columns to be renamed.
        - column_rename_dict (dict): Dictionary mapping old column names to new column names.

        Returns:
        - pd.DataFrame: DataFrame with columns renamed according to the provided mapping.

        Raises:
        - ValueError: If any columns to be renamed do not exist in the DataFrame.

        Usage:
        -----
        manager = ModificationManager()
        df = manager.rename_columns(df, {'old_name': 'new_name'})
        """
        missing_cols = [col for col in column_rename_dict.keys() if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} do not exist in the DataFrame.")
        
        df = df.rename(columns=column_rename_dict)
        return df

    @staticmethod
    def convert_dtypes(df: pd.DataFrame, dtype_dict: dict) -> pd.DataFrame:
        """
        Convert the data types of specified columns in a DataFrame.

        Parameters:
        - df (pd.DataFrame): Input DataFrame containing columns to be converted.
        - dtype_dict (dict): Dictionary mapping column names to target data types.

        Returns:
        - pd.DataFrame: DataFrame with specified columns converted to the target data types.

        Raises:
        - ValueError: If any columns do not exist in the DataFrame or if conversion fails.

        Usage:
        -----
        manager = ModificationManager()
        df = manager.convert_dtypes(df, {'column_name': 'int'})
        """
        for col, dtype in dtype_dict.items():
            if col not in df.columns:
                raise ValueError(f"Column '{col}' does not exist in the DataFrame.")
            
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                raise ValueError(f"Error converting column '{col}' to type '{dtype}': {e}")
        return df

    @staticmethod
    def reorder_columns(df: pd.DataFrame, new_column_order: list) -> pd.DataFrame:
        """
        Reorder the columns of a DataFrame according to a specified list of column names.

        Parameters:
        - df (pd.DataFrame): Input DataFrame with columns to be reordered.
        - new_column_order (list): List specifying the new order of columns.

        Returns:
        - pd.DataFrame: DataFrame with columns reordered according to the specified list.

        Raises:
        - ValueError: If any specified columns do not exist in the DataFrame.

        Usage:
        -----
        manager = ModificationManager()
        df = manager.reorder_columns(df, ['col1', 'col2', 'col3'])
        """
        missing_cols = [col for col in new_column_order if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Columns {missing_cols} do not exist in the DataFrame.")
        
        df = df[new_column_order]
        return df