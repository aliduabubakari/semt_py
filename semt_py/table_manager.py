import requests
import json
import pandas as pd
import os
from urllib.parse import urljoin
from fake_useragent import UserAgent
from .auth_manager import AuthManager
from typing import TYPE_CHECKING, List, Optional, Tuple, Dict, Any
import logging
import tempfile
import zipfile
from requests.exceptions import RequestException, JSONDecodeError

class TableManager:
    """
    A class to manage tables through API interactions.
    """

    def __init__(self, base_url, Auth_manager):
        """
        Initialize the TableManager with the base URL and token manager.

        :param base_url: The base URL for the API.
        :param Auth_manager: An instance of TokenManager to handle authentication.
        """
        self.base_url = base_url.rstrip('/') + '/'
        self.api_url = urljoin(self.base_url, 'api/')
        self.Auth_manager = Auth_manager
        self.user_agent = UserAgent()
        self.logger = logging.getLogger(__name__)

    def _get_headers(self):
        """
        Generate the headers required for API requests, including authorization.

        :return: A dictionary containing the headers for the API request.
        """
        token = self.Auth_manager.get_token()
        return {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': f'Bearer {token}',
            'User-Agent': self.user_agent.random,
            'Origin': self.base_url.rstrip('/'),
            'Referer': self.base_url
        }

    def get_table_description(self) -> Dict[str, str]:
        """
        Provides descriptions of all functions in the TableManager class.

        """
        return {
            "get_tables": "Retrieves and lists all tables in a specific dataset.",
            "add_table": "Adds a table to a specific dataset and processes the result.",
            "get_table": "Retrieves a table by its ID from a specific dataset.",
            "delete_tables": "Deletes multiple tables from a specific dataset."
        }

    def get_table_parameters(self, function_name: str) -> str:
        """
        Provides detailed parameter information for a specific function in the TableManager class.
        """
        parameter_info = {
            'get_tables': {
                'parameters': {'dataset_id': 'str', 'debug': 'bool'},
                'usage': """
table_manager = TableManager(base_url, Auth_manager)
tables_df = table_manager.get_tables(dataset_id='dataset_123', debug=True)
print(tables_df)""",
                'example_values': {'dataset_id': "'dataset_123'", 'debug': 'True'}
            },
            'add_table': {
                'parameters': {
                    'dataset_id': 'str',
                    'table_data': 'pd.DataFrame',
                    'table_name': 'str'
                },
                'usage': """
table_manager = TableManager(base_url, Auth_manager)
data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
table_id, message, response_data = table_manager.add_table(dataset_id='dataset_123', table_data=data, table_name='new_table')
print(message)""",
                'example_values': {
                    'dataset_id': "'dataset_123'",
                    'table_data': "pd.DataFrame({'column1': [1, 2, 3]})",
                    'table_name': "'new_table'"
                }
            },
            'get_table': {
                'parameters': {'dataset_id': 'str', 'table_id': 'str'},
                'usage': """
table_manager = TableManager(base_url, Auth_manager)
table_data = table_manager.get_table(dataset_id='dataset_123', table_id='table_456')
print(table_data)""",
                'example_values': {'dataset_id': "'dataset_123'", 'table_id': "'table_456'"}
            },
            'delete_tables': {
                'parameters': {'dataset_id': 'str', 'table_ids': 'List[str]'},
                'usage': """
table_manager = TableManager(base_url, Auth_manager)
results = table_manager.delete_tables(dataset_id='dataset_123', table_ids=['table_456', 'table_789'])
for table_id, (success, message) in results.items():
    print(f"Table {table_id}: {message}")""",
                'example_values': {'dataset_id': "'dataset_123'", 'table_ids': "['table_456', 'table_789']"}
            }
        }
        
        table_info = parameter_info.get(function_name, "Function not found.")
        return self._format_table_info(table_info)

    def _format_table_info(self, table_info: Dict[str, Any]) -> str:
        """
        Formats the Table function information into a readable, structured output.

        Parameters:
        ----------
        table_info : dict
            Information dictionary about the table function, including parameters,
            usage, and example values.

        Returns:
        -------
        str
            A formatted string with readable output.
        """
        if isinstance(table_info, str):
            return table_info  # Handles the "Function not found." case
        
        parameters = table_info.get('parameters', {})
        usage = table_info.get('usage', 'No usage information available')
        example_values = table_info.get('example_values', {})

        formatted_output = "### Table Function Information\n\n"
        
        formatted_output += "**Parameters:**\n"
        for param, dtype in parameters.items():
            example = example_values.get(param, "N/A")
            formatted_output += f"- `{param}` ({dtype})\n"
            formatted_output += f"  - Example: `{example}`\n"

        formatted_output += f"\n**Usage Example:**\n```python\n{usage}\n```\n"
        
        return formatted_output
        
    def get_tables(self, dataset_id: str, debug: bool = False) -> pd.DataFrame:
        """
        Retrieve and list all tables in a specific dataset.

        """
        url = f"{self.api_url}dataset/{dataset_id}/table"
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
                tables = data['collection']
                if not tables:
                    print(f"No tables found in dataset with ID: {dataset_id}")
                    return pd.DataFrame()

                print(f"Tables in dataset {dataset_id}:")
                for table in tables:
                    table_id = table.get('id')
                    table_name = table.get('name')
                    if table_id and table_name:
                        print(f"ID: {table_id}, Name: {table_name}")
                    else:
                        print("A table with missing ID or name was found.")

                return pd.DataFrame(tables)
            else:
                print("Unexpected response structure. 'collection' key not found.")
                return pd.DataFrame()

        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
            print(f"Error getting dataset tables: {e}")
            return pd.DataFrame()
    
    def add_table(self, dataset_id: str, table_data: pd.DataFrame, table_name: str) -> Tuple[Optional[str], str, Optional[Dict[str, Any]]]:
        """
        Add a table to a specific dataset and process the result.

        This method uploads a DataFrame as a CSV file to the specified dataset
        and processes the API response to extract the table ID and other details.

        """
        url = f"{self.api_url}dataset/{dataset_id}/table/"
        headers = self._get_headers()
        headers.pop('Content-Type', None)  # Remove Content-Type for file upload
        
        temp_file_path = self._create_temp_csv(table_data)
        
        try:
            with open(temp_file_path, 'rb') as file:
                files = {'file': (file.name, file, 'text/csv')}
                data = {'name': table_name}
                
                response = requests.post(url, headers=headers, data=data, files=files, timeout=30)
                response.raise_for_status()
                response_data = response.json()
                
                # Extract the table ID from the response data
                if 'tables' in response_data and len(response_data['tables']) > 0:
                    table_id = response_data['tables'][0].get('id')
                    message = f"Table added successfully with ID: {table_id}"
                    self.logger.info(message)
                    return table_id, message, response_data
                else:
                    message = "Failed to add table. No table ID returned."
                    self.logger.warning(message)
                    return None, message, response_data

        except requests.RequestException as e:
            error_message = f"Request error occurred: {str(e)}"
            if hasattr(e, 'response'):
                error_message += f"\nResponse status code: {e.response.status_code}"
                error_message += f"\nResponse content: {e.response.text[:200]}..."
            self.logger.error(error_message)
            return None, error_message, None

        except IOError as e:
            error_message = f"File I/O error occurred: {str(e)}"
            self.logger.error(error_message)
            return None, error_message, None

        except Exception as e:
            error_message = f"An unexpected error occurred: {str(e)}"
            self.logger.error(error_message)
            return None, error_message, None

        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    def _create_temp_csv(self, table_data: pd.DataFrame) -> str:
        """
        Create a temporary CSV file from a DataFrame.

        Args:
        ----
        table_data : pd.DataFrame
            The table data to be written to the CSV file.

        Returns:
        -------
        str
            The path of the temporary CSV file.
        """
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
            table_data.to_csv(temp_file, index=False)
            temp_file_path = temp_file.name
        
        return temp_file_path

    def _process_add_table_result(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the result of adding a table to a dataset.

        Args:
        ----
        response_data : dict
            The response data from the API after adding a table.

        Returns:
        -------
        dict
            A dictionary containing the message and response data.
        """
        if 'tables' in response_data and len(response_data['tables']) > 0:
            table_id = response_data['tables'][0].get('id')
            message = f"Table added successfully with ID: {table_id}"
            return {'message': message, 'response_data': response_data, 'table_id': table_id}
        else:
            message = "Failed to add table. No table ID returned."
            return {'message': message, 'response_data': response_data}

    
    def get_table(self, dataset_id: str, table_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a table by its ID from a specific dataset.

        This method sends a GET request to the dataset API endpoint to retrieve
        a table by its ID. The response is returned in JSON format, including
        the table ID.
        """
        url = f"{self.api_url}dataset/{dataset_id}/table/{table_id}"
        headers = self._get_headers()

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            table_data = response.json()
            table_data["id"] = table_id
            return table_data
        except requests.RequestException as e:
            self.logger.error(f"Error occurred while retrieving the table data: {e}")
            return None
    


    def _create_zip_file(self, df: pd.DataFrame, zip_filename: Optional[str] = None) -> str:
        """
        Create a zip file containing a CSV file from the given DataFrame.

        The zip file is created as a temporary file unless a filename is specified.

        Args:
        ----
        df : pd.DataFrame
            The DataFrame to be saved as a CSV file.
        zip_filename : str, optional
            The path to the zip file to be created.

        Returns:
        -------
        str
            The path to the created zip file.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the DataFrame to a CSV file in the temporary directory
            csv_file = os.path.join(temp_dir, 'data.csv')
            df.to_csv(csv_file, index=False)

            # Determine the path for the zip file
            if zip_filename:
                zip_path = zip_filename
            else:
                # Create a temporary file for the zip
                temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
                temp_zip.close()
                zip_path = temp_zip.name

            # Create a zip file containing the CSV
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
                z.write(csv_file, os.path.basename(csv_file))

            # Return the path to the zip file
            return zip_path
    
    def delete_tables(self, dataset_id: str, table_ids: List[str]) -> Dict[str, Tuple[bool, str]]:
        """
        Delete multiple tables from a specific dataset.

        This method sends DELETE requests to the dataset API endpoint to remove
        tables by their IDs. It processes the API responses to confirm the deletions.

        """
        results = {}
        headers = self._get_headers()

        for table_id in table_ids:
            url = f"{self.api_url}dataset/{dataset_id}/table/{table_id}"
            try:
                response = requests.delete(url, headers=headers)
                response.raise_for_status()

                if response.status_code in [200, 204]:
                    message = f"Table with ID '{table_id}' deleted successfully."
                    self.logger.info(message)
                    results[table_id] = (True, message)
                else:
                    message = f"Unexpected response status: {response.status_code}"
                    self.logger.warning(message)
                    results[table_id] = (False, message)

            except requests.RequestException as e:
                error_message = f"Request error occurred: {str(e)}"
                if hasattr(e, 'response'):
                    error_message += f"\nResponse status code: {e.response.status_code}"
                    error_message += f"\nResponse content: {e.response.text[:200]}..."
                self.logger.error(error_message)
                results[table_id] = (False, error_message)

        return results
