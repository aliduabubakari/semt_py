# DatasetManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [get_dataset_list](#get_dataset_list)
  - [get_dataset_description](#get_dataset_description)
  - [get_dataset_parameters](#get_dataset_parameters)
  - [get_datasets](#get_datasets)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```python
pip install semt_py
```

## Class Overview

The `DatasetManager` class provides a comprehensive interface for managing datasets through API interactions. It handles authentication, request formatting, and response processing while providing convenient methods for dataset operations.

## Constructor

```python
def __init__(self, base_url: str, Auth_manager: AuthManager)
```

### Parameters:
- `base_url` (str): The base URL of the API endpoint
- `Auth_manager` (AuthManager): An instance of AuthManager for handling authentication

### Example:
```python
from semt_py import DatasetManager, AuthManager

auth_manager = AuthManager(api_url="https://api.example.com", 
                         username="your_username", 
                         password="your_password")

dataset_manager = DatasetManager(base_url="https://api.example.com", 
                               Auth_manager=auth_manager)
```

## Methods

### get_dataset_list

```python
def get_dataset_list(self) -> List[str]
```

Returns a list of available dataset function names.

#### Returns:
- List[str]: Available function names

#### Example:
```python
functions = dataset_manager.get_dataset_list()
print(functions)  # ['get_datasets', 'add_dataset', 'delete_dataset']
```

### get_dataset_description

```python
def get_dataset_description(self) -> Dict[str, Dict[str, str]]
```

Provides detailed descriptions of all dataset functions.

#### Returns:
- Dict[str, Dict[str, str]]: Dictionary containing function descriptions

#### Example:
```python
descriptions = dataset_manager.get_dataset_description()
for func, info in descriptions.items():
    print(f"\nFunction: {func}")
    for key, value in info.items():
        print(f"{key}: {value}")
```

### get_dataset_parameters

```python
def get_dataset_parameters(self, function_name: str) -> Dict[str, Any]
```

Provides detailed parameter information for a specific dataset function.

#### Parameters:
- `function_name` (str): Name of the function to get parameters for

#### Returns:
- Dict[str, Any]: Dictionary containing parameter information

#### Example:
```python
info = dataset_manager.get_dataset_parameters('get_datasets')
print(info)
```

### get_datasets

```python
def get_datasets(self, debug: bool = False) -> pd.DataFrame
```

Retrieves the list of datasets from the server.

#### Parameters:
- `debug` (bool, optional): Enable debug mode. Defaults to False.

#### Returns:
- pd.DataFrame: DataFrame containing dataset information

#### Example:
```python
datasets_df = dataset_manager.get_datasets(debug=True)
print(datasets_df)
```

## Usage Examples

### Basic Usage
```python
from semt_py import DatasetManager, AuthManager

# Setup
auth_manager = AuthManager("https://api.example.com", "username", "password")
dataset_manager = DatasetManager("https://api.example.com", auth_manager)

# Get available datasets
datasets = dataset_manager.get_datasets()
print(datasets)

# Get function information
info = dataset_manager.get_dataset_parameters('get_datasets')
print(info)
```

### Advanced Usage
```python
# Enable debug mode for detailed information
datasets = dataset_manager.get_datasets(debug=True)

# Get comprehensive function descriptions
descriptions = dataset_manager.get_dataset_description()
for func, desc in descriptions.items():
    print(f"\n{func}:", desc['description'])
```

## Error Handling

The DatasetManager implements comprehensive error handling:

```python
try:
    datasets = dataset_manager.get_datasets()
except requests.RequestException as e:
    print(f"API request failed: {e}")
except ValueError as e:
    print(f"Data processing error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

#### 1. **Authentication Management**
   - Always securely store credentials
   - Implement token refresh mechanisms
   - Use environment variables for sensitive data

#### 2. **Error Handling**
   - Implement try-catch blocks for API calls
   - Enable debug mode during development
   - Log errors appropriately

#### 3. **Performance Optimization**
   - Cache results when appropriate
   - Minimize debug mode usage in production
   - Implement request timeouts

#### 4. **Data Management**
   - Validate data before sending to API
   - Handle large datasets in chunks
   - Implement proper cleanup procedures
```
