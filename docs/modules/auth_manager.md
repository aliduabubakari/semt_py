# AuthManager Documentation

## Table of Contents
- [Installation](#installation)
- [Class Overview](#class-overview)
- [Constructor](#constructor)
- [Methods](#methods)
  - [get_token](#get_token)
  - [get_headers](#get_headers)
  - [get_auth_list](#get_auth_list)
  - [get_auth_description](#get_auth_description)
  - [get_auth_parameters](#get_auth_parameters)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```python
pip install semt_py
```

## Class Overview

The `AuthManager` class provides a robust interface for managing authentication tokens for API access. It handles token retrieval, refreshing, and maintenance while providing convenient methods for authentication-related operations.

## Constructor

```python
def __init__(self, api_url: str, username: str, password: str)
```

### Parameters:
- `api_url` (str): The base URL of the API for authentication
- `username` (str): The username for API authentication
- `password` (str): The password for API authentication

### Example:
```python
from semt_py import AuthManager

auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)
```

## Methods

### get_token

```python
def get_token(self) -> str
```

Retrieves the current authentication token, refreshing if necessary.

#### Returns:
- str: The current authentication token

#### Example:
```python
token = auth_manager.get_token()
print(token)  # "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
```


### get_headers

```python
def get_headers(self) -> Dict[str, str]
```

Returns headers required for API requests.

#### Returns:
- Dict[str, str]: Headers including authorization token

#### Example:
```python
headers = auth_manager.get_headers()
print(headers)
```

### get_auth_list

```python
def get_auth_list(self) -> List[str]
```

Returns list of available authentication methods.

#### Returns:
- List[str]: Available authentication methods

#### Example:
```python
methods = auth_manager.get_auth_list()
print(methods)  # ['get_headers']
```

### get_auth_description

```python
def get_auth_description(self, auth_name: str) -> str
```

Retrieves description of a specific authentication method.

#### Parameters:
- `auth_name` (str): Name of the authentication method

#### Returns:
- str: Description of the authentication method

#### Example:
```python
desc = auth_manager.get_auth_description('get_headers')
print(desc)
```

### get_auth_parameters

```python
def get_auth_parameters(self, auth_name: str) -> str:
```

Get detailed parameter information for a specific authentication method.

#### Parameters:
- `auth_name` (str): Name of the authentication method

#### Returns:
- str: Formatted string containing parameter information and usage examples.

#### Example:
```python
# Get detailed parameter information
params = token_manager.get_auth_parameters('get_headers')
print(params)
```

## Usage Examples

### Basic Usage
```python
from semt_py import AuthManager

# Initialize manager
auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

# Get authentication headers
headers = auth_manager.get_headers()

# Make authenticated request
import requests
response = requests.get(
    "https://api.example.com/data",
    headers=headers
)
```

### Advanced Usage
```python
# Check available methods
methods = auth_manager.get_auth_list()
print("Available methods:", methods)

# Get method information
for method in methods:
    desc = auth_manager.get_auth_description(method)
    params = auth_manager.get_auth_parameters(method)
    print(f"\nMethod: {method}")
    print(f"Description: {desc}")
    print(f"Parameters: {params}")
```

## Error Handling

```python
try:
    # Get authentication token
    token = auth_manager.get_token()
    
    # Make authenticated request
    headers = auth_manager.get_headers()
    response = requests.get(url, headers=headers)
    
except requests.RequestException as e:
    print(f"API request failed: {e}")
    if hasattr(e, 'response'):
        print(f"Status code: {e.response.status_code}")
        print(f"Response: {e.response.text}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Token Management
- **Let `AuthManager` handle token refresh automatically**
- **Don't store tokens manually**
- **Use environment variables for credentials**

### 2. Security
- **Never expose credentials in code**
- **Use HTTPS for all API communications**
- **Implement proper error handling**

### 3. Performance
- **Reuse `AuthManager` instance**
- **Let token caching work automatically**
- **Avoid unnecessary token refreshes**

### 4. Error Handling
- **Implement proper `try-except` blocks**
- **Log authentication failures**
- **Handle token expiration gracefully**

### 5. Configuration
- **Use configuration files**
- **Implement environment variables**
- **Separate credentials from code**

### 6. Maintenance
- **Monitor token expiration**
- **Implement proper logging**
- **Regular security audits**