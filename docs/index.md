# SemT_py Documentation

Welcome to the documentation for SemT_py, a powerful Python library for Semantic Enrichment of Tables.

## Overview

SemT_py provides a comprehensive suite of tools for enhancing and enriching tabular data with semantic information. This library simplifies the process of working with semantic data while maintaining high performance and ease of use.

## Key Features

- **Semantic Table Processing**: Enhance your tables with semantic information
- **Flexible Authentication**: Secure access to various data sources
- **Extensible Architecture**: Easy to extend and customize for your needs
- **Data Reconciliation**: Advanced matching and reconciliation capabilities
- **Efficient Data Management**: Optimized for handling large datasets

## Quick Example

```python
from semt_py import TableManager
from semt_py import ReconciliationManager

# Initialize the table manager
table_manager = TableManager()
reconciliation_manager = ReconciliationManager(base_url, token_manager)

# Load and process a table
table_data = table_manager.get_table(dataset_id, table_id)

column_name = ""
reconciliator_id = ""
optional_columns = []

try:
    reconciled_table, backend_payload = reconciliation_manager.reconcile(
        table_data,
        column_name,
        reconciliator_id,
        optional_columns
    )
    if reconciled_table and backend_payload:
        print("Column reconciled successfully and backend payload created!")
    else:
        print("Failed to reconcile column or create backend payload.")
except Exception as e:
    print(f"Error during reconciliation process: {e}")
```

## Module Overview

SemT_py consists of several key modules:

- **Auth Manager**: Handles authentication and security
- **Dataset Manager**: Manages data loading and preprocessing
- **Extension Manager**: Handles plugin and extension functionality
- **Modification Manager**: Controls data modification operations
- **Reconciliation Manager**: Manages data matching and reconciliation
- **Table Manager**: Core table processing functionality
- **Utils**: Utility functions and helpers

For detailed information about each module, please visit their respective documentation pages.