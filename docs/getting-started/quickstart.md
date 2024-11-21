# Quick Start Guide

This guide will walk you through the basic usage of SemT_py, demonstrating how to perform common operations with tables, reconciliation, and extensions.

## Initial Setup

First, import the necessary modules and set up your credentials:

```python
from semt_py.auth_manager import AuthManager
from semt_py.dataset_manager import DatasetManager
from semt_py.table_manager import TableManager
from semt_py.reconciliation_manager import ReconciliationManager
from semt_py.extension_manager import ExtensionManager
from semt_py.utils import Utility

# Configure your environment
base_url = "YOUR_BASE_URL"
api_url = "YOUR_API_URL"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

# Initialize authentication
auth_manager = AuthManager(base_url)
token = auth_manager.authenticate(username, password)
```

## Working with Datasets

### List Available Datasets

```python
# Initialize dataset manager
dataset_manager = DatasetManager(base_url, auth_manager)

# Get list of available datasets
datasets_df = dataset_manager.get_datasets(debug=False)
print("Available datasets:", datasets_df)
```

## Managing Tables

### Add a New Table

```python
# Initialize table manager
table_manager = TableManager(base_url, auth_manager)

# Add a new table to a dataset
dataset_id = "YOUR_DATASET_ID"
table_name = "example_table"

# Assuming you have a pandas DataFrame 'df'
table_id, message, response_data = table_manager.add_table(
    dataset_id, 
    df, 
    table_name
)
print(f"Table added with ID: {table_id}")
```

### Retrieve Table Data

```python
# Get table data
table_data = table_manager.get_table(dataset_id, table_id)
```

## Reconciliation Process

The reconciliation process helps match your data with external sources. Here's how to reconcile a column:

```python
# Initialize reconciliation manager
reconciliation_manager = ReconciliationManager(base_url, auth_manager)

# Define reconciliation parameters
column_name = "city_column"  # Replace with your column name
reconciliator_id = "geocodingHere"  # Example reconciliator
optional_columns = []  # Add any optional columns needed

# Perform reconciliation
try:
    reconciled_table, backend_payload = reconciliation_manager.reconcile(
        table_data,
        column_name,
        reconciliator_id,
        optional_columns
    )
    if reconciled_table is not None:
        print("Reconciliation successful!")
except Exception as e:
    print(f"Reconciliation error: {e}")
```

## Extending Data

After reconciliation, you can extend your data with additional properties:

```python
# Initialize extension manager
extension_manager = ExtensionManager(base_url, auth_manager)

# Extend table with meteorological data
meteo_extended_table, meteo_extension_payload = extension_manager.extend_column(
    table=reconciled_table,
    column_name='City',
    extender_id="meteoPropertiesOpenMeteo",
    properties=[
        'apparent_temperature_max',
        'apparent_temperature_min',
        'precipitation_sum',
        'precipitation_hours'
    ],
    other_params={
        'date_column_name': "date_column",
        'decimal_format': "comma"
    }
)
```

## Pushing Changes to Backend

After processing your data, you can push the changes back to the backend:

```python
# Initialize utility
utility = Utility(base_url, auth_manager)

# Push changes to backend
success_message, sent_payload = utility.push_to_backend(
    dataset_id,
    table_id,
    payload,  # Your processed data payload
    debug=False
)
print(success_message)
```

## Downloading Results

To save your processed data:

```python
# Download as CSV
output_file = "processed_data.csv"
downloaded_file = extension_manager.download_csv(
    dataset_id, 
    table_id, 
    output_file=output_file
)
print(f"Data saved to: {downloaded_file}")
```

## Complete Example

Here's a complete workflow putting all the pieces together:

```python
# Setup
base_url = "YOUR_BASE_URL"
api_url = "YOUR_API_URL"
username = "YOUR_USERNAME"
password = "YOUR_PASSWORD"

# Initialize managers
auth_manager = AuthManager(base_url)
token = auth_manager.authenticate(username, password)
dataset_manager = DatasetManager(base_url, auth_manager)
table_manager = TableManager(base_url, auth_manager)
reconciliation_manager = ReconciliationManager(base_url, auth_manager)
extension_manager = ExtensionManager(base_url, auth_manager)
utility = Utility(base_url, auth_manager)

# Work with data
datasets_df = dataset_manager.get_datasets()
dataset_id = "YOUR_DATASET_ID"

# Add table
table_id, message, response = table_manager.add_table(dataset_id, your_dataframe, "example_table")

# Reconcile data
reconciled_table, backend_payload = reconciliation_manager.reconcile(
    table_data,
    "city_column",
    "geocodingHere",
    []
)

# Extend data
extended_table, extension_payload = extension_manager.extend_column(
    table=reconciled_table,
    column_name='City',
    extender_id="meteoPropertiesOpenMeteo",
    properties=['apparent_temperature_max'],
    other_params={'date_column_name': "date_column"}
)

# Save results
extension_manager.download_csv(dataset_id, table_id, "final_results.csv")
```

## Next Steps

- Explore the [API Reference](../api.md) for detailed information about all available methods
- Check out the specific module documentation for advanced features:
  - [Auth Manager](../modules/auth_manager.md)
  - [Dataset Manager](../modules/dataset_manager.md)
  - [Table Manager](../modules/table_manager.md)
  - [Reconciliation Manager](../modules/reconciliation_manager.md)
  - [Extension Manager](../modules/extension_manager.md)

## Error Handling

You can enhance the use of the library with comprehensive error handling. Here's an example:

```python
try:
    # Your SemT_py operations here
    result = some_operation()
except Exception as e:
    print(f"Error: {str(e)}")
    # Handle the error appropriately
```

Remember to always check the return values and handle exceptions appropriately in your production code.