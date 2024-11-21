# TableManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [get_tables](#get_tables)
  - [add_table](#add_table)
  - [get_table](#get_table)
  - [delete_tables](#delete_tables)
  - [get_table_description](#get_table_description)
  - [get_table_parameters](#get_table_parameters)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```python
pip install semt_py
```

## Class Overview

The `TableManager` class provides a comprehensive interface for managing tables through API interactions. It handles table operations such as retrieval, addition, and deletion while managing authentication and maintaining consistent API communication.

## Constructor

```python
def __init__(self, base_url: str, Auth_manager: AuthManager)
```

### Parameters:
- `base_url` (str): The base URL for the API endpoint
- `Auth_manager` (AuthManager): An instance of AuthManager for handling authentication

### Example:
```python
from semt_py import TableManager, AuthManager

auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

table_manager = TableManager(
    base_url="https://api.example.com",
    Auth_manager=auth_manager
)
```

## Methods

### get_tables

```python
def get_tables(
    self,
    dataset_id: str,
    debug: bool = False
) -> pd.DataFrame
```

Retrieves all tables in a specified dataset.

#### Parameters:
- `dataset_id` (str): The ID of the dataset to query
- `debug` (bool): Enable debug output

#### Returns:
- pd.DataFrame: Contains table information

#### Example:
```python
tables_df = table_manager.get_tables(
    dataset_id='dataset_123',
    debug=True
)
print(tables_df)
```

### add_table

```python
def add_table(
    self,
    dataset_id: str,
    table_data: pd.DataFrame,
    table_name: str
) -> Tuple[Optional[str], str, Optional[Dict]]
```

Adds a new table to a dataset.

#### Parameters:
- `dataset_id` (str): Target dataset ID
- `table_data` (pd.DataFrame): Data to be added
- `table_name` (str): Name for the new table

#### Returns:
- Tuple containing:
  - table_id (Optional[str]): ID of created table
  - message (str): Status message
  - response_data (Optional[Dict]): API response

### get_table

```python
def get_table(
    self,
    dataset_id: str,
    table_id: str
) -> Optional[Dict[str, Any]]
```

Retrieves a specific table by ID.

#### Parameters:
- `dataset_id` (str): Dataset ID
- `table_id` (str): Table ID to retrieve

#### Returns:
- Optional[Dict[str, Any]]: Table data or None

### delete_tables

```python
def delete_tables(
    self,
    dataset_id: str,
    table_ids: List[str]
) -> Dict[str, Tuple[bool, str]]
```

Deletes multiple tables from a dataset.

#### Parameters:
- `dataset_id` (str): Dataset ID
- `table_ids` (List[str]): Table IDs to delete

#### Returns:
- Dict[str, Tuple[bool, str]]: Results for each table

### get_table_description

```python
def get_table_description(self) -> Dict[str, str]
```

Provides descriptions of all functions in the TableManager class.

#### Parameters:
- **None**

#### Returns:
Dict[str, str] A dictionary where keys are function names and values are descriptions.

### get_table_parameters

```python
def get_table_parameters(self, function_name: str) -> List[str]
```

Provides the parameters required for a specific function in the TableManager class.

#### Parameters:
- `function_name` : The name of the function to get parameters for.

#### Returns:
List[str]: A list of parameter names required by the function.

## Usage Examples

### Basic Usage
```python
# Initialize manager
table_manager = TableManager(base_url, auth_manager)

# List tables
tables_df = table_manager.get_tables('dataset_123')

# Add new table
data = pd.DataFrame({'column1': [1, 2, 3]})
table_id, msg, response = table_manager.add_table(
    dataset_id='dataset_123',
    table_data=data,
    table_name='new_table'
)
```

### Advanced Usage
```python
# Delete multiple tables
results = table_manager.delete_tables(
    dataset_id='dataset_123',
    table_ids=['table_456', 'table_789']
)

# Process results
for table_id, (success, message) in results.items():
    if success:
        print(f"Table {table_id} deleted successfully")
    else:
        print(f"Failed to delete table {table_id}: {message}")
```

## Error Handling

```python
try:
    # Get tables
    tables_df = table_manager.get_tables(
        dataset_id='dataset_123',
        debug=True
    )
    
    if tables_df.empty:
        print("No tables found")
    else:
        print(f"Found {len(tables_df)} tables")
        
except requests.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Invalid data: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. **Authentication Management**
   - Securely store credentials
   - Implement token refresh
   - Use environment variables

### 2. **Error Handling**
   - Implement try-except blocks
   - Enable debug mode during development
   - Log errors appropriately

### 3. **Data Management**
   - Validate data before upload
   - Handle large datasets in chunks
   - Clean up temporary files

### 4. **Performance Optimization**
   - Cache results when appropriate
   - Minimize API calls
   - Use batch operations

### 5. **Security**
   - Validate input data
   - Sanitize file names
   - Handle sensitive data appropriately

### 6. **Resource Management**
   - Close file handles
   - Delete temporary files
   - Monitor memory usage