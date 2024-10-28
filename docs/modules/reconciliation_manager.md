# ReconciliationManager

## Overview

The `ReconciliationManager` class provides a robust interface for managing reconciliation operations through API interactions. It enables users to retrieve lists of reconciliators, their parameters, and perform data reconciliation operations with various services like geocoding.

## Installation

The ReconciliationManager is part of the core library and can be imported directly:

```python
from semt_py.reconciliation_manager import ReconciliationManager
```

## Prerequisites

The following dependencies are required:

- requests
- pandas
- json
- datetime
- urllib

## Class Initialization

```python
reconciliation_manager = ReconciliationManager(base_url, auth_manager)
```

### Parameters

- `base_url` (str): The base URL for the API endpoint
- `auth_manager` (AuthManager): An instance of AuthManager for handling authentication

## Main Features

### 1. Retrieving Reconciliators

```python
reconciliators_df = reconciliation_manager.get_reconciliators(debug=False)
```

Returns a DataFrame containing available reconciliators with their IDs, relative URLs, and names.

#### Parameters

- `debug` (bool, optional): If True, prints additional debugging information. Defaults to False.

#### Returns

- pandas.DataFrame: Contains columns for "id", "relativeUrl", and "name"

### 2. Getting Reconciliator Parameters

```python
parameters = reconciliation_manager.get_reconciliator_parameters(id_reconciliator, debug=False)
```

Retrieves and displays parameters required for a specific reconciliator service.

#### Parameters

- `id_reconciliator` (str): The ID of the reconciliator to get parameters for
- `debug` (bool, optional): If True, displays debug information. Defaults to False.

#### Returns

- Dict[str, Any] | None: Dictionary containing mandatory and optional parameters if found, None otherwise

### 3. Performing Reconciliation

```python
final_payload, backend_payload = reconciliation_manager.reconcile(
    table_data,
    column_name,
    reconciliator_id,
    optional_columns
)
```

Performs reconciliation on specified column data using the chosen reconciliation service.

#### Parameters

- `table_data` (Dict): Input table data containing rows and columns
- `column_name` (str): Name of the column to reconcile
- `reconciliator_id` (str): ID of the reconciliation service ('geocodingHere', 'geocodingGeonames', or 'geonames')
- `optional_columns` (List[str]): Additional columns to include in reconciliation

#### Returns

- Tuple[Dict, Dict]: Contains:
  - final_payload: Reconciled table data with updated values
  - backend_payload: Data prepared for backend use with metadata

## Usage Examples

### Basic Usage

```python
# Initialize the ReconciliationManager
base_url = "https://api.example.com"
auth_manager = AuthManager(api_url="https://api.example.com/token", username="user", password="pass")
reconciliation_manager = ReconciliationManager(base_url, auth_manager)

# Get available reconciliators
reconciliators = reconciliation_manager.get_reconciliators()
print(reconciliators)

# Get parameters for a specific reconciliator
params = reconciliation_manager.get_reconciliator_parameters('geocodingHere')
print(params)
```

### Performing Reconciliation

```python
# Example table data
table_data = {
    "table": {
        "id": "table1",
        "idDataset": "dataset1",
        "name": "Addresses",
        "nCols": 2,
        "nRows": 2,
        "nCells": 4
    },
    "columns": {
        "address": {"status": "pending"},
        "city": {"status": "pending"}
    },
    "rows": {
        "1": {
            "cells": {
                "address": {"label": "123 Main St"},
                "city": {"label": "Anytown"}
            }
        },
        "2": {
            "cells": {
                "address": {"label": "456 Oak St"},
                "city": {"label": "Othertown"}
            }
        }
    }
}

# Perform reconciliation
final_payload, backend_payload = reconciliation_manager.reconcile(
    table_data,
    "address",
    "geocodingHere",
    ["city"]
)
```

## Error Handling

The ReconciliationManager includes comprehensive error handling:

- Network errors are caught and logged
- Invalid reconciliator IDs raise ValueError
- Failed reconciliation attempts return (None, None)
- JSON parsing errors are handled gracefully

## Debug Mode

Most methods accept a `debug` parameter that enables additional logging:

```python
# Enable debug mode for more detailed output
reconciliators = reconciliation_manager.get_reconciliators(debug=True)
```

## Internal Methods

The class includes several internal methods for data processing:

- `_get_headers()`: Generates API request headers
- `_prepare_input_data()`: Formats data for reconciliation
- `_send_reconciliation_request()`: Handles API communication
- `_compose_reconciled_table()`: Processes reconciliation results
- `_restructure_payload()`: Updates metadata and annotations
- `_create_backend_payload()`: Prepares data for backend systems

These methods are not intended for direct use but may be useful for understanding the reconciliation process.

## Notes

1. The reconciliation process is synchronous and may take time for large datasets
2. Valid reconciliator IDs are: 'geocodingHere', 'geocodingGeonames', and 'geonames'
3. The API requires proper authentication via the AuthManager
4. All dates are handled in UTC

## See Also

- AuthManager documentation for authentication details
- API documentation for endpoint specifications