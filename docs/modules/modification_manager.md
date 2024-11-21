# ModificationManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [get_modifier_list](#get_modifier_list)
  - [get_modifier_description](#get_modifier_description)
  - [get_modifier_parameters](#get_modifier_parameters)
  - [modify](#modify)
  - [iso_date](#iso_date)
  - [lower_case](#lower_case)
  - [drop_na](#drop_na)
  - [rename_columns](#rename_columns)
  - [convert_dtypes](#convert_dtypes)
  - [reorder_columns](#reorder_columns)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [How to Add a New Modification Technique](#how-to-add-a-new-modification-technique)
  - [Step 1: Define the Modifier Method](#step-1-define-the-modifier-method)
  - [Step 2: Register the Modifier](#step-2-register-the-modifier)
  - [Step 3: Update Documentation](#step-3-update-documentation)
  - [Step 4: Test Your Modifier](#step-4-test-your-modifier)

## Installation

```python
pip install semt_py
```

## Class Overview

The `ModificationManager` class provides a comprehensive framework for applying various modifications to pandas DataFrames. It includes methods for converting date formats, changing data types, manipulating text, and reorganizing DataFrame structures.

## Constructor

```python
def __init__(self)
```

Initializes the ModificationManager with available modifiers.

### Example:
```python
from semt_py import ModificationManager

modification_manager = ModificationManager()
```

## Methods

### get_modifier_list

```python
def get_modifier_list(self) -> List[str]
```

Returns a list of available modifier names.

#### Returns:
- List[str]: Available modifier names

#### Example:
```python
modifiers = modification_manager.get_modifier_list()
print(modifiers)  # ['iso_date', 'lower_case', 'drop_na', ...]
```

### get_modifier_description

```python
def get_modifier_description(self, modifier_name: str) -> str
```

Returns the description of a specific modifier.

#### Parameters:
- `modifier_name` (str): Name of the modifier

#### Returns:
- str: Description of the modifier

#### Example:
```python
description = modification_manager.get_modifier_description('iso_date')
print(description)
```

### get_modifier_parameters

Retrieves the parameters required for a specific modifier along with usage example.

```python
manager = ModificationManager()
modifier_list = manager.get_modifier_parameters('iso_date')
print(modifier_list)
```

### modify

```python
def modify(self, modifier_name: str, **kwargs) -> Union[pd.DataFrame, Tuple[pd.DataFrame, str]]
```

Applies a specified modifier to a DataFrame.

#### Parameters:
- `modifier_name` (str): Name of the modifier to apply
- `**kwargs`: Arguments required by the specific modifier

#### Returns:
- Modified DataFrame or tuple of (DataFrame, message)

#### Example:
```python
df, message = modification_manager.modify('iso_date', df=df, date_col='date')
```

### iso_date

```python
@staticmethod
def iso_date(df: pd.DataFrame, date_col: str) -> Tuple[pd.DataFrame, str]
```

Converts date column to ISO 8601 format.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame
- `date_col` (str): Name of date column

#### Returns:
- Tuple[pd.DataFrame, str]: Modified DataFrame and status message

### lower_case

```python
@staticmethod
def lower_case(df: pd.DataFrame, column: str) -> pd.DataFrame
```

Converts string values to lowercase.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame
- `column` (str): Column to convert

#### Returns:
- pd.DataFrame: Modified DataFrame

### drop_na
```python
@staticmethod
def drop_na(df: pd.DataFrame) -> pd.DataFrame
```

Remove all rows from a DataFrame that contain any missing (NaN) values.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame from which to drop rows with missing values.

#### Returns:
- pd.DataFrame: DataFrame with rows containing missing values removed.

### rename_columns
```python
@staticmethod
def rename_columns(df: pd.DataFrame, column_rename_dict: dict) -> pd.DataFrame
```

Rename columns in a DataFrame according to a given dictionary mapping.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame with columns to be renamed.
- `column_rename_dict` (dict): Dictionary mapping old column names to new column names.

#### Returns:
- pd.DataFrame: DataFrame with columns renamed according to the provided mapping.

#### Raises:
- ValueError: If any columns to be renamed do not exist in the DataFrame.

### convert_dtypes
```python
@staticmethod
def convert_dtypes(df: pd.DataFrame, dtype_dict: dict) -> pd.DataFrame
```

Convert the data types of specified columns in a DataFrame.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame containing columns to be converted.

#### Returns:
- pd.DataFrame: DataFrame with specified columns converted to the target data types.

### reorder_columns
```python
@staticmethod
def reorder_columns(df: pd.DataFrame, new_column_order: list) -> pd.DataFrame
```

Reorder the columns of a DataFrame according to a specified list of column names.

#### Parameters:
- `df` (pd.DataFrame): Input DataFrame with columns to be reordered.
- `new_column_order` (list): List of column names in the desired order.

#### Returns:
- pd.DataFrame: DataFrame with columns reordered according to the specified list.

## Usage Examples

### Basic Usage
```python
from semt_py import ModificationManager
# Initialize manager
manager = ModificationManager()

# Convert dates to ISO format
df, message = manager.modify('iso_date', 
                           df=df, 
                           date_col='date_column')

# Convert text to lowercase
df = manager.modify('lower_case', 
                   df=df, 
                   column='text_column')
```

### Advanced Usage
```python
# Chain multiple modifications
df, _ = manager.modify('iso_date', df=df, date_col='date')
df = manager.modify('lower_case', df=df, column='text')
df = manager.modify('convert_dtypes', 
                   df=df, 
                   dtype_dict={'value': 'int64'})
df = manager.modify('reorder_columns', 
                   df=df, 
                   new_column_order=['id', 'date', 'text'])
```

## Error Handling

```python
try:
    df, message = manager.modify('iso_date', 
                               df=df, 
                               date_col='date')
except ValueError as e:
    print(f"Date conversion error: {e}")
except KeyError as e:
    print(f"Column not found: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

#### 1. **Data Validation**
   - Always validate input data types
   - Check column existence before modifications
   - Verify date formats before conversion

#### 2. **Error Handling**
   - Implement try-except blocks for each modification
   - Validate parameters before processing
   - Handle missing or invalid data appropriately

#### 3. **Performance Optimization**
   - Chain modifications efficiently
   - Use appropriate data types
   - Handle large datasets in chunks

#### 4. **Data Integrity**
   - Create backups before modifications
   - Verify results after each modification
   - Maintain data consistency

#### 5. **Code Organization**
   - Use meaningful variable names
   - Document modifications clearly
   - Follow consistent coding patterns