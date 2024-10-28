# Dataset Manager Tutorial

This guide explains how to use the Dataset Manager to work with datasets through API interactions. The Dataset Manager provides functions to list, add, and delete datasets while handling all the API communication details for you.

## Setting Up Dataset Manager

First, you'll need to set up the Dataset Manager with your API credentials:

```python
from semt_py import DatasetManager, AuthManager

# First set up authentication
auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

# Then initialize Dataset Manager
dataset_manager = DatasetManager(
    base_url="https://api.example.com",
    Auth_manager=auth_manager
)
```

## Core Functions

### 1. Listing Available Dataset Functions (`get_dataset_list`)

Want to see what operations you can perform with datasets? Use `get_dataset_list`:

```python
# Get list of available functions
available_functions = dataset_manager.get_dataset_list()
print(available_functions)

# Output will be:
# ['get_datasets', 'add_dataset', 'delete_dataset']
```

**When to use this:**
- When exploring the Dataset Manager's capabilities
- When you need to check available dataset operations
- For documentation purposes

### 2. Understanding Dataset Functions (`get_dataset_description`)

Need details about what each function does? Use `get_dataset_description`:

```python
# Get descriptions of all functions
descriptions = dataset_manager.get_dataset_description()

# Print descriptions in a readable format
for func_name, details in descriptions.items():
    print(f"\nFunction: {func_name}")
    for key, value in details.items():
        print(f"{key}: {value}")

# Output will include details like:
# Function: get_datasets
# description: Retrieves the list of datasets from the server
# returns: pandas DataFrame containing dataset information
# raises: RequestException if API call fails, ValueError if JSON decoding fails
```

### 3. Getting Detailed Function Information (`get_dataset_parameters`)

Want to know exactly how to use a specific function? Use `get_dataset_parameters`:

```python
# Get detailed information about the get_datasets function
info = dataset_manager.get_dataset_parameters('get_datasets')
print(info)

# This will show:
# - Required parameters
# - Usage examples
# - Example values
```

### 4. Working with Datasets (`get_datasets`)

The main function you'll use to retrieve datasets:

```python
# Get list of all datasets
datasets_df = dataset_manager.get_datasets(debug=False)

# With debug information
datasets_df = dataset_manager.get_datasets(debug=True)

# The result is a pandas DataFrame containing your datasets
print(datasets_df)
```

**Debug Mode Features:**
- Shows API response status codes
- Displays metadata information
- Helps troubleshoot any issues

## Complete Working Example

Here's a full example showing how to use the Dataset Manager:

```python
from semt_py import DatasetManager, AuthManager
import pandas as pd

# 1. Set up authentication
auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

# 2. Initialize Dataset Manager
dataset_manager = DatasetManager(
    base_url="https://api.example.com",
    Auth_manager=auth_manager
)

# 3. List available functions
functions = dataset_manager.get_dataset_list()
print("Available functions:", functions)

# 4. Get descriptions
descriptions = dataset_manager.get_dataset_description()
print("\nFunction descriptions:")
for func, desc in descriptions.items():
    print(f"\n{func}:", desc['description'])

# 5. Get detailed parameters for get_datasets
params = dataset_manager.get_dataset_parameters('get_datasets')
print("\nParameters for get_datasets:", params)

# 6. Retrieve datasets
try:
    # Get datasets with debug info
    datasets = dataset_manager.get_datasets(debug=True)
    
    # Display the results
    if not datasets.empty:
        print("\nAvailable datasets:")
        print(datasets)
    else:
        print("\nNo datasets found or error occurred")
        
except Exception as e:
    print(f"Error: {e}")
```

## Common Questions and Tips

1. **Error Handling**
   - Always wrap API calls in try-except blocks
   - Use debug=True when troubleshooting
   - Check the response status codes and messages

2. **Best Practices:**
   - Keep track of your dataset IDs
   - Use meaningful dataset names
   - Regular list and clean up unused datasets

3. **Performance Tips:**
   - Minimize debug mode usage in production
   - Cache dataset lists when appropriate
   - Reuse the Dataset Manager instance

4. **Common Issues:**
   - Connection errors: Check your internet and API URL
   - Authentication errors: Verify your credentials
   - Empty results: Use debug mode to investigate

## Need Help?

- Use `get_dataset_description()` to understand available functions
- Check function parameters with `get_dataset_parameters()`
- Enable debug mode to get more detailed error information
- Make sure your authentication is properly set up

Remember to handle your API credentials securely and never share them in your code or version control system!
```