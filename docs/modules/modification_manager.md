# ModificationManager

The `ModificationManager` class provides a flexible framework for applying various modifications to pandas DataFrames. It includes methods for converting date formats, changing data types, manipulating text, and reorganizing DataFrame structures.

## Installation

```python
pip install pandas dateutil
```

## Quick Start

```python
from modification_manager import ModificationManager

# Initialize the manager
manager = ModificationManager()

# Get available modifiers
modifiers = manager.get_modifier_list()

# Apply a modification
df, message = manager.modify('iso_date', df=your_dataframe, date_col='date_column')
```

## Available Modifiers

### 1. ISO Date Conversion (`iso_date`)
Converts date columns to ISO 8601 format (YYYY-MM-DD).

```python
df, message = manager.iso_date(df, date_col='date_column')
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame
- `date_col` (str): Name of the date column to convert

**Returns:**
- Modified DataFrame
- Status message indicating success or current format

### 2. Lowercase Conversion (`lower_case`)
Converts all string values in a specified column to lowercase.

```python
df = manager.lower_case(df, column='text_column')
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame
- `column` (str): Name of the column to convert

**Returns:**
- Modified DataFrame

### 3. Drop NA Values (`drop_na`)
Removes rows containing any missing values.

```python
df = manager.drop_na(df)
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame

**Returns:**
- Cleaned DataFrame

### 4. Rename Columns (`rename_columns`)
Renames DataFrame columns according to a provided mapping.

```python
df = manager.rename_columns(df, {'old_name': 'new_name'})
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame
- `column_rename_dict` (dict): Mapping of old column names to new names

**Returns:**
- DataFrame with renamed columns

### 5. Convert Data Types (`convert_dtypes`)
Converts column data types according to a specified mapping.

```python
df = manager.convert_dtypes(df, {'column_name': 'int64'})
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame
- `dtype_dict` (dict): Mapping of column names to desired data types

**Returns:**
- DataFrame with converted data types

### 6. Reorder Columns (`reorder_columns`)
Reorders DataFrame columns according to a specified list.

```python
df = manager.reorder_columns(df, ['col1', 'col2', 'col3'])
```

**Parameters:**
- `df` (pandas.DataFrame): Input DataFrame
- `new_column_order` (list): List of column names in desired order

**Returns:**
- DataFrame with reordered columns

## Helper Methods

### Get Modifier List
Retrieves all available modifiers.

```python
modifiers = manager.get_modifier_list()
```

### Get Modifier Description
Retrieves the description of a specific modifier.

```python
description = manager.get_modifier_description('iso_date')
```

### Get Modifier Parameters
Retrieves detailed information about a modifier's parameters and usage.

```python
info = manager.get_modifier_parameters('rename_columns')
print(info)  # Displays formatted information about parameters and usage
```

## Error Handling

The ModificationManager includes comprehensive error handling:

- Raises `ValueError` when:
  - Specified columns don't exist in the DataFrame
  - Date conversion fails due to invalid formats
  - Data type conversion fails
  - Invalid modifier names are provided
  - Required parameters are missing

## Examples

### Complete Usage Example

```python
import pandas as pd
from modification_manager import ModificationManager

# Create a sample DataFrame
df = pd.DataFrame({
    'date': ['2023/01/01', '2023/01/02'],
    'text': ['Sample TEXT', 'More TEXT'],
    'value': ['1', '2']
})

# Initialize the manager
manager = ModificationManager()

# Apply multiple modifications
df, _ = manager.modify('iso_date', df=df, date_col='date')
df = manager.modify('lower_case', df=df, column='text')
df = manager.modify('convert_dtypes', df=df, dtype_dict={'value': 'int64'})

# Reorder columns
df = manager.modify('reorder_columns', df=df, new_column_order=['value', 'date', 'text'])
```

## Best Practices

1. **Date Handling**
   - Always validate date formats before conversion
   - Use ISO date modifier for standardization

2. **Data Type Conversion**
   - Verify data consistency before type conversion
   - Handle missing values appropriately

3. **Column Management**
   - Back up DataFrame before applying modifications
   - Verify column existence before operations

4. **Error Handling**
   - Implement try-except blocks for modification chains
   - Validate input parameters before processing

## Contributing

When adding new modifiers:

1. Add the modifier function to the class
2. Update the `modifiers` dictionary in `__init__`
3. Add appropriate documentation
4. Include error handling
5. Update the modifier description and parameters information

## License

[Include appropriate license information here]