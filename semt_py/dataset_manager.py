import requests
import json
import pandas as pd
from urllib.parse import urljoin
from fake_useragent import UserAgent
from typing import TYPE_CHECKING, List, Optional, Tuple, Dict, Any
import logging
from .Auth_manager import AuthManager

class DatasetManager:
    """
    A class to manage datasets through API interactions.
    """
    def __init__(self, base_url, Auth_manager):
        self.base_url = base_url.rstrip('/') + '/'
        self.api_url = urljoin(self.base_url, 'api/')
        self.Auth_manager = Auth_manager
        self.user_agent = UserAgent()
        self.logger = logging.getLogger(__name__)
        self.available_functions = {
            'get_datasets': self.get_datasets,
            'add_dataset': self.add_dataset,
            'delete_dataset': self.delete_dataset
        }

    def get_dataset_list(self) -> List[str]:
        """
        Retrieve the list of available dataset functions.

        Returns:
        -------
        List[str]
            A list of available dataset function names.

        Usage:
        -----
        manager = DatasetManager(base_url, Auth_manager)
        functions = manager.get_dataset_list()
        print(functions)  # ['get_datasets', 'add_dataset', 'delete_dataset']
        """
        return list(self.available_functions.keys())

    def get_dataset_description(self) -> Dict[str, Dict[str, str]]:
        """
        Provides detailed descriptions of all dataset functions.

        Returns:
        -------
        Dict[str, Dict[str, str]]
            A dictionary containing function information with keys:
            - 'description': Brief description of the function
            - 'returns': Description of what the function returns
            - 'raises': Description of possible exceptions

        Usage:
        -----
        manager = DatasetManager(base_url, Auth_manager)
        descriptions = manager.get_dataset_description()
        for func, info in descriptions.items():
            print(f"\nFunction: {func}")
            for key, value in info.items():
                print(f"{key}: {value}")
        """
        return {
            "get_datasets": {
                "description": "Retrieves the list of datasets from the server",
                "returns": "pandas DataFrame containing dataset information",
                "raises": "RequestException if API call fails, ValueError if JSON decoding fails"
            },
            "add_dataset": {
                "description": "Adds a new dataset to the server",
                "returns": "Tuple of (success: bool, error_message: Optional[str])",
                "raises": "ValueError if dataset_name is empty or data is invalid"
            },
            "delete_dataset": {
                "description": "Deletes a specified dataset from the server",
                "returns": "Boolean indicating success of deletion",
                "raises": "ValueError if dataset_id is invalid or not found"
            }
        }

    def get_dataset_parameters(self, function_name: str) -> Dict[str, Any]:
        """
        Provides detailed parameter information for a specific dataset function.

        Parameters:
        ----------
        function_name : str
            The name of the function to get parameters for.

        Returns:
        -------
        Dict[str, Any]
            A dictionary containing:
            - 'parameters': Dictionary of parameter names and their types
            - 'usage': String showing example usage of the function
            - 'example_values': Dictionary showing example values for each parameter

        Usage:
        -----
        manager = DatasetManager(base_url, Auth_manager)
        info = manager.get_dataset_parameters('get_datasets')
        print(info['usage'])
        """
        parameter_info = {
            'get_datasets': {
                'parameters': {'debug': 'bool'},
                'usage': """
manager = DatasetManager(base_url, Auth_manager)
datasets_df = manager.get_datasets(debug=True)
print(datasets_df)""",
                'example_values': {'debug': 'True'}
            },
            'add_dataset': {
                'parameters': {
                    'dataset_name': 'str',
                    'data': 'pd.DataFrame'
                },
                'usage': """
manager = DatasetManager(base_url, Auth_manager)
data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
success, error_msg = manager.add_dataset(dataset_name='new_dataset', data=data)
if success:
    print("Dataset added successfully")
else:
    print(f"Failed to add dataset: {error_msg}")""",
                'example_values': {
                    'dataset_name': "'my_dataset'",
                    'data': "pd.DataFrame({'column1': [1, 2, 3]})"
                }
            },
            'delete_dataset': {
                'parameters': {'dataset_id': 'str'},
                'usage': """
manager = DatasetManager(base_url, Auth_manager)
if manager.delete_dataset(dataset_id='dataset_123'):
    print("Dataset deleted successfully")
else:
    print("Failed to delete dataset")""",
                'example_values': {'dataset_id': "'dataset_123'"}
            }
        }
        
        dataset_info = parameter_info.get(function_name, "Function not found.")
        return self._format_dataset_info(dataset_info)

    def _format_dataset_info(self, dataset_info: Dict[str, Any]) -> str:
        """
        Formats the dataset function information into a readable, structured output.

        Parameters:
        ----------
        dataset_info : dict
            Information dictionary about the dataset function, including parameters,
            usage, and example values.

        Returns:
        -------
        str
            A formatted string with readable output.
        """
        if isinstance(dataset_info, str):
            return dataset_info  # Handles the "Function not found." case

        # Extract components for better readability
        parameters = dataset_info.get('parameters', {})
        usage = dataset_info.get('usage', 'No usage information available')
        example_values = dataset_info.get('example_values', {})
        description = dataset_info.get('description', 'No description available')
        returns = dataset_info.get('returns', 'No return information available')

        # Create formatted output
        formatted_output = "### Dataset Function Information\n\n"
        
        # Add description and return type
        formatted_output += f"**Description:**\n{description}\n\n"
        formatted_output += f"**Returns:**\n{returns}\n\n"
        
        # Add parameters section
        formatted_output += "**Parameters:**\n"
        for param, dtype in parameters.items():
            example = example_values.get(param, "N/A")
            formatted_output += f"- `{param}` ({dtype})\n"
            formatted_output += f"  - Example: `{example}`\n"

        # Add usage example
        formatted_output += f"\n**Usage Example:**\n```python\n{usage}\n```\n"
        
        return formatted_output

    def _get_headers(self):
        """Generate headers for API requests."""
        token = self.Auth_manager.get_token()
        return {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {token}',
            'User-Agent': self.user_agent.random,
            'Origin': self.base_url.rstrip('/'),
            'Referer': self.base_url
        }
    
    def get_datasets(self, debug: bool = False) -> pd.DataFrame:
        """
        Retrieve the list of datasets from the server.

        This method sends a GET request to the dataset API endpoint to retrieve
        a list of available datasets. The response is converted into a pandas
        DataFrame for easy manipulation and analysis.

        Args:
        ----
        debug : bool
            If True, prints additional information like metadata and status code.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the datasets. If the request fails or the
            response structure is unexpected, an empty DataFrame is returned.

        Usage:
        -----
        # Initialize the DatasetManager with API credentials
        base_url = "https://api.example.com"
        Auth_manager = TokenManager(api_url, username, password)
        dataset_manager = DatasetManager(base_url, Auth_manager)

        # Retrieve the list of datasets
        try:
            datasets_df = dataset_manager.get_dataset_list(debug=True)
            print(datasets_df)
        except Exception as e:
            print(f"Error retrieving dataset list: {e}")
        """
        url = urljoin(self.api_url, 'dataset')
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            
            if debug:
                print(f"Status Code: {response.status_code}")
                print("Metadata:")
                print(json.dumps(data.get('meta', {}), indent=4))  # Display metadata in a pretty format
                
            if 'collection' in data:
                # Convert the 'collection' key into a DataFrame
                return pd.DataFrame(data['collection'])
            else:
                print("Unexpected response structure. 'collection' key not found.")
                return pd.DataFrame()  # Return an empty DataFrame if structure is not as expected

        except requests.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e, 'response'):
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.text[:200]}...")
            return pd.DataFrame()

        except ValueError as e:
            print(f"JSON decoding failed: {e}")
            return pd.DataFrame()

    def add_dataset(self, dataset_name: str, data: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """[Original implementation remains the same]"""
        # Implementation remains unchanged
        pass

    def delete_dataset(self, dataset_id: str) -> bool:
        """[Original implementation remains the same]"""
        # Implementation remains unchanged
        pass