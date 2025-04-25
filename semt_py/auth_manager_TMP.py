import requests
import json
import time
import jwt
from typing import Dict, List

class AuthManager:
    """Manages authentication tokens for API access."""

    def __init__(self, api_url: str, username: str, password: str):
        """Initialize AuthManager with API credentials."""
        self.api_url = api_url.rstrip('/')
        self.signin_url = f"{self.api_url}/auth/signin"
        self.username = username
        self.password = password
        self.token = None
        self.expiry = 0

    def get_token(self) -> str:
        """
        Retrieve the current authentication token.

        If the token is expired or not yet retrieved, this method will refresh
        the token by calling the `refresh_token` method.

        Returns
        -------
        str
            The current authentication token.
        """
        if self.token is None or time.time() >= self.expiry:
            self.refresh_token()
        return self.token

    def refresh_token(self) -> None:
        """Refresh authentication token via sign-in request."""
        signin_data = {"username": self.username, "password": self.password}
        signin_headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
        }

        try:
            response = requests.post(self.signin_url, headers=signin_headers, data=json.dumps(signin_data))
            response.raise_for_status()
            token_info = response.json()
            self.token = token_info.get("token")
            
            if self.token:
                decoded = jwt.decode(self.token, options={"verify_signature": False})
                self.expiry = decoded.get('exp', time.time() + 3600)
            else:
                self.expiry = time.time() + 3600
                
        except requests.RequestException as e:
            print(f"Sign-in request failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text}")
            self.token = None
            self.expiry = 0

    def get_auth_list(self) -> List[str]:
        """Get available authentication methods."""
        return ['get_headers']

    def get_auth_description(self, auth_name: str) -> str:
        """Get authentication method description."""
        descriptions = {
            'get_headers': "Returns the headers required for API requests, including the authorization token. "
                          "The headers include Accept and Content-Type specifications, along with a Bearer token "
                          "for authentication. The token is automatically refreshed if expired."
        }
        return descriptions.get(auth_name, "Authentication method not found.")

    def get_auth_parameters(self, auth_name: str) -> str:
        """Get authentication method parameter details."""
        parameter_info = {
            'get_headers': {
                'parameters': {},
                'returns': {
                    'type': 'dict',
                    'description': 'Headers dictionary containing Accept, Content-Type, and Authorization',
                    'structure': {
                        'Accept': 'application/json, text/plain, */*',
                        'Content-Type': 'application/json;charset=UTF-8',
                        'Authorization': 'Bearer <token>'
                    }
                },
                'usage': """# Initialize AuthManager
    auth_manager = AuthManager(api_url='https://api.example.com', 
                             username='your_username', 
                             password='your_password')
    
    # Get headers for API request
    headers = auth_manager.get_headers()
    
    # Use headers in API request
    response = requests.get('https://api.example.com/endpoint', headers=headers)""",
                'example_values': {
                    'return_value': """{
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
    }"""
                }
            }
        }
        
        auth_info = parameter_info.get(auth_name, "Authentication method not found.")
        return self._format_auth_info(auth_info)

    def _format_auth_info(self, auth_info: dict) -> str:
        """Format authentication information for display."""
        if isinstance(auth_info, str):
            return auth_info
        
        formatted_output = "### Authentication Method Information\n\n"
        
        if auth_info.get('parameters'):
            formatted_output += "**Parameters:**\n"
            for param, dtype in auth_info['parameters'].items():
                formatted_output += f" - `{param}` ({dtype})\n"
        else:
            formatted_output += "**Parameters:** None required\n"
        
        if auth_info.get('returns'):
            formatted_output += "\n**Returns:**\n"
            returns_info = auth_info['returns']
            formatted_output += f" - Type: `{returns_info['type']}`\n"
            formatted_output += f" - Description: {returns_info['description']}\n"
            
            if returns_info.get('structure'):
                formatted_output += " - Structure:\n```python\n"
                formatted_output += json.dumps(returns_info['structure'], indent=4)
                formatted_output += "\n```\n"
        
        if auth_info.get('usage'):
            formatted_output += "\n**Usage Example:**\n```python\n"
            formatted_output += auth_info['usage']
            formatted_output += "\n```\n"
        
        return formatted_output
    
    def get_headers(self) -> Dict[str, str]:
        """Get headers for authenticated API requests."""
        return {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.get_token()}"
        }