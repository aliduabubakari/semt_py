# TableManager Module Documentation

The `TableManager` class provides a comprehensive interface for managing tables through API interactions. It handles table operations such as retrieval, addition, and deletion while managing authentication and maintaining consistent API communication.

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Authentication](#authentication)
- [Methods](#methods)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)

## Installation

The TableManager module requires the following dependencies:
```python
requests
pandas
fake_useragent
```

## Class Overview

```python
from .Auth_manager import AuthManager

class TableManager:
    def __init__(self, base_url: str, Auth_manager: AuthManager):
        # Initialize TableManager with base URL and authentication manager
```

The TableManager class is initialized with:
- `base_url`: The base URL for the API endpoint
- `Auth_manager`: An instance of AuthManager for handling authentication

## Authentication

The TableManager uses token-based authentication handled through the AuthManager class. Each request includes:
- Bearer token authentication
- Random User-Agent headers
- Origin and Referer headers matching the base URL

## Methods

### get_tables(dataset_id: str, debug: bool = False) → pd.DataFrame

Retrieves all tables in a specified dataset.

**Parameters:**
- `dataset_id` (str): The ID of the dataset to query
- `debug` (bool, optional): Enable debug output. Defaults to False

**Returns:**
- pandas DataFrame containing table information

**Example:**
```python
tables_df = table_manager.get_tables(dataset_id='dataset_123', debug=True)
```

### add_table(dataset_id: str, table_data: pd.DataFrame, table_name: str) → Tuple[Optional[str], str, Optional[Dict]]

Adds a new table to a dataset.

**Parameters:**
- `dataset_id` (str): Target dataset ID
- `table_data` (pd.DataFrame): Data to be added as a table
- `table_name` (str): Name for the new table

**Returns:**
- Tuple containing:
  - table_id (Optional[str]): ID of the created table
  - message (str): Operation status message
  - response_data (Optional[Dict]): Complete API response

**Example:**
```python
table_id, message, response = table_manager.add_table(
    dataset_id='dataset_123',
    table_data=df,
    table_name='new_table'
)
```

### get_table(dataset_id: str, table_id: str) → Optional[Dict[str, Any]]

Retrieves a specific table by ID.

**Parameters:**
- `dataset_id` (str): Dataset ID containing the table
- `table_id` (str): ID of the table to retrieve

**Returns:**
- Dictionary containing table data or None if not found

**Example:**
```python
table_data = table_manager.get_table(
    dataset_id='dataset_123',
    table_id='table_456'
)
```

### delete_tables(dataset_id: str, table_ids: List[str]) → Dict[str, Tuple[bool, str]]

Deletes multiple tables from a dataset.

**Parameters:**
- `dataset_id` (str): Dataset ID containing the tables
- `table_ids` (List[str]): List of table IDs to delete

**Returns:**
- Dictionary mapping table IDs to tuples of (success_status, message)

**Example:**
```python
results = table_manager.delete_tables(
    dataset_id='dataset_123',
    table_ids=['table_456', 'table_789']
)
```

## Usage Examples

### Basic Table Management

```python
# Initialize TableManager
base_url = "https://api.example.com"
auth_manager = AuthManager(api_credentials)
table_manager = TableManager(base_url, auth_manager)

# List all tables in a dataset
tables_df = table_manager.get_tables('dataset_123')

# Add a new table
new_data = pd.DataFrame({'column1': [1, 2, 3]})
table_id, msg, response = table_manager.add_table('dataset_123', new_data, 'new_table')

# Retrieve specific table
table_data = table_manager.get_table('dataset_123', table_id)

# Delete tables
results = table_manager.delete_tables('dataset_123', [table_id])
```

### Error Handling Example

```python
try:
    tables_df = table_manager.get_tables(dataset_id='dataset_123')
    if tables_df.empty:
        print("No tables found or error occurred")
    else:
        print(f"Found {len(tables_df)} tables")
except Exception as e:
    print(f"Error accessing tables: {str(e)}")
```

## Error Handling

The TableManager implements comprehensive error handling:

- Network errors: Caught and logged through RequestException
- JSON parsing errors: Handled via JSONDecodeError
- Authentication errors: Managed through the AuthManager
- File operations: Protected with try/except blocks for IOError

All errors are logged using the built-in logging system, with appropriate error messages returned to the caller.

## Logging

The TableManager uses Python's built-in logging system:

```python
import logging
logger = logging.getLogger(__name__)
```

Log messages include:
- INFO: Successful operations
- WARNING: Non-critical issues
- ERROR: Operation failures and exceptions

## Best Practices

1. Always check return values for None or empty DataFrames
2. Use debug mode when troubleshooting API interactions
3. Implement appropriate error handling in your code
4. Monitor logging output for operation status
5. Clean up resources after file operations

## Security Considerations

- Credentials are managed through the AuthManager
- Temporary files are properly cleaned up
- API tokens are never logged
- HTTPS is required for API communication