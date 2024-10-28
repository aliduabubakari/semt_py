# Auth Manager Tutorial

This guide will walk you through using the main functions of the Auth Manager with practical examples. The Auth Manager helps you handle authentication when accessing APIs, making it easier to manage tokens and access secure data.

## Setting Up Auth Manager

First, let's set up the Auth Manager with your API credentials:

```python
from semt_py import AuthManager

# Initialize Auth Manager with your credentials
auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)
```

## 1. Getting Authentication Tokens (`get_token`)

The `get_token` function helps you get an authentication token that you'll need to access secure API endpoints. Think of it like getting a visitor's badge at a secure building.

```python
# Example 1: Basic token retrieval
token = auth_manager.get_token()

# The token will look something like this:
# "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**What's happening behind the scenes?**
- Checks if you already have a valid token
- If the token is expired or missing, gets a new one automatically
- Returns the token as a text string

**Pro tip:** You don't usually need to call this directly - other Auth Manager functions will use it automatically when needed!

## 2. Viewing Available Authentication Methods (`get_auth_list`)

Want to know what authentication methods are available? The `get_auth_list` function shows you all the options:

```python
# Example 2: List available authentication methods
available_methods = auth_manager.get_auth_list()
print(available_methods)

# Output will be something like:
# ['get_headers']
```

**When to use this:**
- When exploring the Auth Manager's capabilities
- When you need to check what authentication options are available
- For documentation purposes

## 3. Understanding Authentication Methods (`get_auth_description`)

Need to know what a specific authentication method does? The `get_auth_description` function gives you a plain-English explanation:

```python
# Example 3: Get description of the get_headers method
description = auth_manager.get_auth_description('get_headers')
print(description)

# Output will be something like:
# "Returns the headers required for API requests, including the authorization token. 
#  The headers include Accept and Content-Type specifications, along with a Bearer 
#  token for authentication. The token is automatically refreshed if expired."
```

**Use cases:**
- Learning about a specific authentication method
- Understanding what each method does
- Deciding which method to use for your needs

## 4. Detailed Method Information (`get_auth_parameters`)

Want to dive deeper into how to use a specific method? The `get_auth_parameters` function provides detailed information and examples:

```python
# Example 4: Get detailed information about get_headers
detailed_info = auth_manager.get_auth_parameters('get_headers')
print(detailed_info)

# Output will include:
# - Required parameters (if any)
# - What the method returns
# - Example usage
# - Sample return values
```

## Putting It All Together

Here's a complete example showing how you might use these functions in a real project:

```python
from semt_py import AuthManager
import pandas as pd

# 1. Set up Auth Manager
auth_manager = AuthManager(
    api_url="https://api.example.com",
    username="your_username",
    password="your_password"
)

# 2. Check available methods
methods = auth_manager.get_auth_list()
print("Available authentication methods:", methods)

# 3. Learn about a specific method
method_name = 'get_headers'
description = auth_manager.get_auth_description(method_name)
print(f"\nDescription of {method_name}:", description)

# 4. Get detailed information
details = auth_manager.get_auth_parameters(method_name)
print(f"\nDetailed information about {method_name}:", details)

# 5. Use the authentication in a real request
headers = auth_manager.get_headers()  # This automatically handles the token for you
print("\nGenerated headers ready for API use!")

# Example: Using the headers to fetch some data
import requests

try:
    response = requests.get(
        "https://api.example.com/data", 
        headers=headers
    )
    data = response.json()
    df = pd.DataFrame(data)
    print("\nSuccessfully fetched data!")
    display(df.head())  # If you're in a Jupyter notebook
except Exception as e:
    print(f"Error fetching data: {e}")
```

## Common Questions and Tips

1. **How often should I get a new token?**
   - Don't worry about this! The Auth Manager automatically handles token renewal.

2. **What if I get an error?**
   - Check your API URL, username, and password
   - Make sure you have internet connectivity
   - Verify that your API service is running

3. **Best Practices:**
   - Store your credentials securely (use environment variables)
   - Don't share your tokens
   - Let Auth Manager handle token management automatically

4. **Performance Tips:**
   - The Auth Manager caches tokens until they expire
   - You don't need to create multiple Auth Manager instances
   - Reuse the same Auth Manager instance throughout your application

Need more help? The `get_auth_parameters` function provides detailed examples for each method!