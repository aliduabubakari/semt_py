# ExtensionManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [extend_column](#extend_column)
  - [get_extenders](#get_extenders)
  - [get_extender_parameters](#get_extender_parameters)
  - [download_csv](#download_csv)
  - [download_json](#download_json)
  - [parse_json](#parse_json)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```python
pip install semt_py
```

## Class Overview

The `ExtensionManager` class provides functionality to manage and interact with data extension services through API interactions. It handles authentication, request formatting, and response processing while providing methods for extending table columns using various extenders.

## Constructor

```python
def __init__(self, base_url: str, token: str)
```

### Parameters:
- `base_url` (str): The base URL for the API
- `token` (str): The authentication token for accessing the API

### Example:
```python
from semt_py import ExtensionManager

extension_manager = ExtensionManager(
    base_url="https://api.example.com",
    token="your_api_token"
)
```

## Methods

### extend_column

```python
def extend_column(
    self,
    table: Dict,
    column_name: str,
    extender_id: str,
    properties: List[str],
    other_params: Optional[Dict] = None,
    debug: bool = False
) -> Tuple[Dict, Dict]
```

Extends a column using a specified extender service.

#### Parameters:
- `table` (Dict): The input table containing data
- `column_name` (str): The name of the column to extend
- `extender_id` (str): The ID of the extender to use
- `properties` (List[str]): The properties to extend
- `other_params` (Optional[Dict]): Additional parameters specific to the extender
- `debug` (bool): Enable debug mode

#### Returns:
- Tuple[Dict, Dict]: Extended table and backend payload

### get_extenders

```python
def get_extenders(self, debug: bool = False) -> pd.DataFrame
```

Retrieves a list of available extenders.

#### Parameters:
- `debug` (bool): Enable debug mode

#### Returns:
- pd.DataFrame: DataFrame containing extender information

### get_extender_parameters

```python
def get_extender_parameters(
    self,
    extender_id: str,
    print_params: bool = False
) -> Optional[str]
```

Retrieves parameters for a specific extender service.

#### Parameters:
- `extender_id` (str): The ID of the extender service
- `print_params` (bool): Whether to print the parameters

#### Returns:
- Optional[str]: Formatted string containing parameter details

### download_csv

```python
def download_csv(
    self,
    dataset_id: str,
    table_id: str,
    output_file: str = "downloaded_data.csv"
) -> str
```

Downloads table data as CSV.

#### Parameters:
- `dataset_id` (str): The dataset ID
- `table_id` (str): The table ID
- `output_file` (str): Output file name

#### Returns:
- str: Path to the downloaded CSV file

### download_json

```python
def download_json(
    self,
    dataset_id: str,
    table_id: str,
    output_file: str = "downloaded_data.json"
) -> str
```

Downloads table data as W3C JSON format.

#### Parameters:
- `dataset_id` (str): The dataset ID
- `table_id` (str): The table ID
- `output_file` (str): Output file name

#### Returns:
- str: Path to the downloaded JSON file

### parse_json

```python
def parse_json(self, json_data: List[Dict]) -> pd.DataFrame
```

Converts W3C JSON format to pandas DataFrame.

#### Parameters:
- `json_data` (List[Dict]): The W3C JSON data

#### Returns:
- pd.DataFrame: DataFrame containing the parsed data

## Usage Examples

### Basic Usage
```python
from semt_py import ExtensionManager

# Initialize the manager
manager = ExtensionManager(
    base_url="https://api.example.com",
    token="your_api_token"
)

# Get available extenders
extenders = manager.get_extenders(debug=True)
print(extenders)

# Get extender parameters
params = manager.get_extender_parameters("meteoPropertiesOpenMeteo", print_params=True)
```

### Extending Columns
```python
# Extend using meteoPropertiesOpenMeteo
extended_table, payload = manager.extend_column(
    table=table_data,
    column_name="City",
    extender_id="meteoPropertiesOpenMeteo",
    properties=["temperature_max", "precipitation_sum"],
    other_params={
        "date_column_name": "Date",
        "decimal_format": "comma"
    }
)

# Download results
csv_path = manager.download_csv("dataset123", "table456", "weather_data.csv")
```

## Error Handling

```python
try:
    extended_table, payload = manager.extend_column(
        table=table_data,
        column_name="City",
        extender_id="meteoPropertiesOpenMeteo",
        properties=["temperature"],
        other_params={"date_column_name": "Date"},
        debug=True
    )
except ValueError as e:
    print(f"Invalid parameters: {e}")
except requests.RequestException as e:
    print(f"API request failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

#### 1. **Authentication Management**
   - Store API tokens securely
   - Refresh tokens when needed
   - Use environment variables for sensitive data

#### 2. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Enable debug mode during development
   - Log errors appropriately

#### 3. **Performance Optimization**
   - Minimize debug mode usage in production
   - Batch operations when possible
   - Handle large datasets efficiently

#### 4. **Data Validation**
   - Verify input data structure
   - Validate parameters before API calls
   - Check extender compatibility

#### 5. **Resource Management**
   - Clean up downloaded files
   - Close file handles properly
   - Monitor API rate limits
