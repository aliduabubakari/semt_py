# ExtensionManager

The `ExtensionManager` class provides functionality to manage and interact with data extension services through API interactions. It allows users to extend table columns using various extenders while handling authentication and API communication.

## Table of Contents
- [Installation](#installation)
- [Basic Usage](#basic-usage)


## Installation

This module is part of the core library and requires the following dependencies:
- requests
- pandas
- json
- urllib

## Basic Usage

```python
from extension_manager import ExtensionManager

# Initialize the manager
base_url = "https://api.example.com"
token = "your_api_token"
manager = ExtensionManager(base_url, token)

# Extend a column using a specific extender
extended_table, backend_payload = manager.extend_column(
    table=your_table,
    column_name="City",
    extender_id="meteoPropertiesOpenMeteo",
    properties=["temperature", "precipitation"],
    other_params={
        "date_column_name": "Date",
        "decimal_format": "comma"
    }
)
```

## Class: ExtensionManager

### Constructor

```python
ExtensionManager(base_url: str, token: str)
```

#### Parameters:
- `base_url` (str): The base URL for the API
- `token` (str): The authentication token for accessing the API

### Methods

#### extend_column

```python
extend_column(
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
- `debug` (bool): Enable/disable debug information

#### Returns:
- Tuple containing:
  - Extended table (Dict)
  - Backend payload (Dict)

#### Example:
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
```

#### get_extenders

```python
get_extenders(debug: bool = False) -> pd.DataFrame
```

Retrieves a list of available extenders.

#### Parameters:
- `debug` (bool): Enable/disable debug information

#### Returns:
- DataFrame containing extender information with columns:
  - id
  - relativeUrl
  - name

#### Example:
```python
extenders_list = manager.get_extenders()
print(extenders_list)
```

#### get_extender_parameters

```python
get_extender_parameters(extender_id: str, print_params: bool = False) -> Optional[str]
```

Retrieves detailed parameters for a specific extender service.

#### Parameters:
- `extender_id` (str): The ID of the extender service
- `print_params` (bool): Whether to print the parameters

#### Returns:
- Formatted string containing parameter details or None if extender not found

#### Example:
```python
params = manager.get_extender_parameters("meteoPropertiesOpenMeteo", print_params=True)
```

#### download_csv

```python
download_csv(
    dataset_id: str,
    table_id: str,
    output_file: str = "downloaded_data.csv"
) -> str
```

Downloads table data as CSV.

#### Parameters:
- `dataset_id` (str): The dataset ID
- `table_id` (str): The table ID
- `output_file` (str): Output file name (default: "downloaded_data.csv")

#### Returns:
- Path to the downloaded CSV file

#### Example:
```python
csv_path = manager.download_csv("dataset123", "table456", "my_data.csv")
```

#### download_json

```python
download_json(
    dataset_id: str,
    table_id: str,
    output_file: str = "downloaded_data.json"
) -> str
```

Downloads table data as W3C JSON format.

#### Parameters:
- `dataset_id` (str): The dataset ID
- `table_id` (str): The table ID
- `output_file` (str): Output file name (default: "downloaded_data.json")

#### Returns:
- Path to the downloaded JSON file

#### Example:
```python
json_path = manager.download_json("dataset123", "table456", "my_data.json")
```

#### parse_json

```python
parse_json(json_data: List[Dict]) -> pd.DataFrame
```

Converts W3C JSON format to pandas DataFrame.

#### Parameters:
- `json_data` (List[Dict]): The W3C JSON data

#### Returns:
- DataFrame containing the parsed data

#### Example:
```python
with open("data.json", "r") as f:
    json_data = json.load(f)
df = manager.parse_json(json_data)
```

## Supported Extenders

The ExtensionManager currently supports two types of extenders:

1. `reconciledColumnExt`: Extends reconciled columns with additional properties
2. `meteoPropertiesOpenMeteo`: Extends location data with meteorological information

### meteoPropertiesOpenMeteo Requirements:
- Requires a date column
- Requires decimal format specification
- Properties should be valid weather parameters

### reconciledColumnExt Requirements:
- Column must be previously reconciled
- Properties must be valid for the reconciled entities

## Error Handling

The ExtensionManager includes comprehensive error handling:
- HTTP errors are raised with detailed error messages
- Invalid extender IDs raise ValueError
- Missing required parameters raise ValueError
- Failed API requests include debug information when debug=True

## Debug Mode

Enable debug mode to get detailed information about:
- API requests and responses
- Payload construction
- Error messages
- Extended table composition

Example with debug mode:
```python
extended_table, payload = manager.extend_column(
    table=table_data,
    column_name="City",
    extender_id="meteoPropertiesOpenMeteo",
    properties=["temperature"],
    other_params={"date_column_name": "Date", "decimal_format": "comma"},
    debug=True
)
```