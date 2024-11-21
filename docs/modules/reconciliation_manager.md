# ReconciliationManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [get_reconciliators](#get_reconciliators)
  - [get_reconciliator_parameters](#get_reconciliator_parameters)
  - [reconcile](#reconcile)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```python
pip install semt_py
```

## Class Overview

The `ReconciliationManager` class provides a robust interface for managing reconciliation operations through API interactions. It enables users to retrieve lists of reconciliators, their parameters, and perform data reconciliation operations with various services like geocoding.

## Constructor

```python
def __init__(self, base_url: str, Auth_manager: AuthManager)
```

### Parameters:
- `base_url` (str): The base URL for the API endpoint
- `Auth_manager` (AuthManager): An instance of AuthManager for handling authentication

### Example:
```python
from semt_py import ReconciliationManager, AuthManager

auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

reconciliation_manager = ReconciliationManager(
    base_url="https://api.example.com",
    Auth_manager=auth_manager
)
```

## Methods

### get_reconciliators

```python
def get_reconciliators(self, debug: bool = False) -> pd.DataFrame
```

Retrieves and returns a list of available reconciliators.

#### Parameters:
- `debug` (bool): Enable debug mode for detailed information

#### Returns:
- pd.DataFrame: Contains columns for "id", "relativeUrl", and "name"

#### Example:
```python
reconciliators = reconciliation_manager.get_reconciliators(debug=True)
print(reconciliators)
```

### get_reconciliator_parameters

```python
def get_reconciliator_parameters(
    self,
    id_reconciliator: str,
    debug: bool = False
) -> Optional[Dict[str, Any]]
```

Retrieves parameters for a specific reconciliator service.

#### Parameters:
- `id_reconciliator` (str): The ID of the reconciliator
- `debug` (bool): Enable debug mode

#### Returns:
- Optional[Dict[str, Any]]: Dictionary containing mandatory and optional parameters

#### Example:
```python
params = reconciliation_manager.get_reconciliator_parameters(
    'geocodingHere',
    debug=True
)
print(params)
```

### reconcile

```python
def reconcile(
    self,
    table_data: Dict,
    column_name: str,
    reconciliator_id: str,
    optional_columns: List[str]
) -> Tuple[Optional[Dict], Optional[Dict]]
```

Performs reconciliation on specified column data.

#### Parameters:
- `table_data` (Dict): Input table data
- `column_name` (str): Name of column to reconcile
- `reconciliator_id` (str): ID of reconciliation service
- `optional_columns` (List[str]): Additional columns to include

#### Returns:
- Tuple[Optional[Dict], Optional[Dict]]: Final payload and backend payload

## Usage Examples

### Basic Usage
```python
# Initialize manager
reconciliation_manager = ReconciliationManager(base_url, auth_manager)

# Get available reconciliators
reconciliators = reconciliation_manager.get_reconciliators(debug=True)

# Get reconciliator parameters
params = reconciliation_manager.get_reconciliator_parameters('geocodingHere')
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
        }
    }
}

# Perform reconciliation
final_payload, backend_payload = reconciliation_manager.reconcile(
    table_data=table_data,
    column_name="address",
    reconciliator_id="geocodingHere",
    optional_columns=["city"]
)
```

## Error Handling

```python
try:
    # Get reconciliators
    reconciliators = reconciliation_manager.get_reconciliators(debug=True)
    
    # Perform reconciliation
    final_payload, backend_payload = reconciliation_manager.reconcile(
        table_data=table_data,
        column_name="address",
        reconciliator_id="geocodingHere",
        optional_columns=["city"]
    )
except ValueError as e:
    print(f"Invalid parameters: {e}")
except requests.RequestException as e:
    print(f"API request failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Data Preparation**
   - Validate input data structure
   - Ensure required columns exist
   - Clean data before reconciliation

2. **Error Handling**
   - Implement comprehensive error handling
   - Enable debug mode during development
   - Log errors appropriately

3. **Performance Optimization**
   - Process data in manageable chunks
   - Monitor API rate limits
   - Cache reconciliator information

4. **Security**
   - Secure API credentials
   - Validate input data
   - Handle sensitive information appropriately

5. **Maintenance**
   - Regular token refresh
   - Monitor API changes
   - Update reconciliator parameters

6. **Data Validation**
   - Verify reconciliation results
   - Check data consistency
   - Validate geographic coordinates
