# Utility Class Documentation

The `Utility` class provides a comprehensive set of helper functions for API interactions, class exploration, and data display. This class is designed to facilitate various common tasks when working with APIs and data manipulation.

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [Utility Information Methods](#utility-information-methods)
  - [Class and Module Exploration](#class-and-module-exploration)
  - [API Interaction Methods](#api-interaction-methods)
  - [Data Export and File Handling](#data-export-and-file-handling)
  - [Data Display Methods](#data-display-methods)

## Installation

The Utility class requires the following dependencies:
```python
import zipfile
import os
import inspect
import tempfile
import pandas as pd
import requests
import json
from urllib.parse import urljoin
from typing import Dict, Tuple, List, Optional
from IPython.core.display import HTML
```

## Class Overview

The Utility class serves as a central hub for various utility functions, primarily focused on:
- API interaction and data management
- Class and module introspection
- Data export and file handling
- Data visualization and display

## Constructor

```python
def __init__(self, api_url: str, Auth_manager)
```

### Parameters
- `api_url` (str): The base URL for the API
- `Auth_manager`: An instance of AuthManager to handle authentication

### Example
```python
utility = Utility("https://api.example.com", auth_manager)
```

## Methods

### Utility Information Methods

#### `get_utils_list()`
Returns a list of all available utility methods.

#### `get_utils_description(util_name: str) -> str`
Returns the description of a specific utility method.

#### `get_utils_parameters(util_name: str) -> str`
Returns detailed parameter information and usage examples for a specific utility method.

### Class and Module Exploration

#### `explore_class_methods(cls) -> List[str]`
Static method that explores all methods of a class, filtering for user-defined functions only.

```python
# Example usage
methods = Utility.explore_class_methods(SomeClass)
print(methods)
```

#### `explore_submodules(submodules: List) -> Dict[str, Dict[str, List[str]]]`
Static method that explores all classes in the given submodules and lists their functions.

```python
# Example usage
submodules = [module1, module2]
result = Utility.explore_submodules(submodules)
print(result)
```

### API Interaction Methods

#### `push_to_backend(dataset_id: str, table_id: str, payload: Dict, debug: bool = False) -> Tuple[str, Dict]`
Pushes payload data to the backend API.

```python
# Example usage
success_message, payload = utility.push_to_backend('dataset_id', 'table_id', payload, debug=True)
print(success_message)
```

### Data Export and File Handling

#### `download_csv(dataset_id: str, table_id: str, output_file: str = "downloaded_data.csv") -> str`
Downloads a CSV file from the backend and saves it locally.

```python
# Example usage
csv_path = utility.download_csv('dataset_id', 'table_id', 'output.csv')
```

#### `download_json(dataset_id: str, table_id: str, output_file: str = "downloaded_data.json") -> str`
Downloads a JSON file in W3C format from the backend and saves it locally.

```python
# Example usage
json_path = utility.download_json('dataset_id', 'table_id', 'output.json')
```

#### `parse_json(json_data: List[Dict]) -> pd.DataFrame`
Parses W3C JSON format into a pandas DataFrame.

```python
# Example usage
df = utility.parse_json(json_data)
```

#### `create_temp_csv(table_data: pd.DataFrame) -> str`
Static method that creates a temporary CSV file from a DataFrame.

```python
# Example usage
temp_file_path = Utility.create_temp_csv(df)
```

#### `create_zip_file(df: pd.DataFrame, zip_filename: Optional[str] = None) -> str`
Creates a zip file containing a CSV file from the given DataFrame.

```python
# Example usage
zip_path = utility.create_zip_file(df, 'output.zip')
```

### Data Display Methods

#### `display_json_table(json_table, number_of_rows=None, from_row=0, labels=None)`
Displays a formatted HTML table from a JSON-based table structure with optional metadata.

```python
# Example usage
json_table = {
    'columns': {
        'Name': {}, 'Age': {}, 'Occupation': {}
    },
    'rows': {
        'r0': {'cells': {'Name': {'label': 'Alice'}, 'Age': {'label': '29'}, 'Occupation': {'label': 'Engineer'}}},
        'r1': {'cells': {'Name': {'label': 'Bob'}, 'Age': {'label': '35'}, 'Occupation': {'label': 'Doctor'}}}
    }
}
html_table = Utility.display_json_table(json_table, number_of_rows=2, labels=['Name', 'Occupation'])
```

## Error Handling

The class includes error handling for:
- Failed API requests
- File download issues
- JSON parsing errors
- Invalid data formats

## Notes

- All API requests include authentication headers automatically
- Temporary files are cleaned up automatically when no longer needed
- The class supports both synchronous and debug operations
- HTML display functions are optimized for Jupyter notebook environments