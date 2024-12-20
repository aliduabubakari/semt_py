import zipfile
import os
import inspect
import tempfile
import pandas as pd
import requests
import json
from urllib.parse import urljoin
from typing import Dict, Tuple, List, Optional
#from .Auth_manager import TokenManager
from .auth_manager import AuthManager
from IPython.core.display import HTML

class Utility:
    """
    A utility class providing various helper functions for API interactions,
    class exploration, and data display.
    """
    def __init__(self, api_url: str, Auth_manager):
        """
        Initialize the Utility class with the API URL and token manager.

        :param api_url: The base URL for the API.
        :param Auth_manager: An instance of TokenManager to handle authentication.
        """
        self.api_url = api_url.rstrip('/') + '/'
        self.Auth_manager = Auth_manager
        self.headers = self._get_headers()

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate the headers required for API requests, including authorization.

        :return: A dictionary containing the headers for the API request.
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.Auth_manager.get_token()}'
        }

    def get_utils_list(self):
        """
        Get a list of all available utility methods.
        """
        return [
            'explore_class_methods',
            'explore_submodules',
            'push_to_backend',
            'download_csv',
            'download_json',
            'parse_json',
            'create_temp_csv',
            'create_zip_file',
            'display_json_table'
        ]

    def get_utils_description(self, util_name: str) -> str:
        """
        Get the description of a specific utility method.
        """
        descriptions = {
            'explore_class_methods': "Explore all methods of a class, filtering for user-defined functions only.",
            'explore_submodules': "Explore all classes in the given submodules and list their functions.",
            'push_to_backend': "Pushes the payload data to the backend API.",
            'download_csv': "Downloads a CSV file from the backend and saves it locally.",
            'download_json': "Downloads a JSON file in W3C format from the backend and saves it locally.",
            'parse_json': "Parses the W3C JSON format into a pandas DataFrame.",
            'create_temp_csv': "Creates a temporary CSV file from a DataFrame.",
            'create_zip_file': "Creates a zip file containing a CSV file from the given DataFrame.",
            'display_json_table': "Displays a formatted HTML table from a JSON-based table structure with optional metadata."
        }
        return descriptions.get(util_name, "Utility not found.")

    def get_utils_parameters(self, util_name: str) -> str:
        """
        Get detailed parameter information for a specific utility method.
        """
        parameter_info = {
            'explore_class_methods': {
                'parameters': {'cls': 'class'},
                'usage': "# Explore methods of a class\nmethods = Utility.explore_class_methods(SomeClass)\nprint(methods)",
                'example_values': {'cls': 'YourClass'}
            },
            'explore_submodules': {
                'parameters': {'submodules': 'List'},
                'usage': "# Explore submodules\nsubmodules = [module1, module2]\nresult = Utility.explore_submodules(submodules)\nprint(result)",
                'example_values': {'submodules': '[your_module1, your_module2]'}
            },
            'push_to_backend': {
                'parameters': {
                    'dataset_id': 'str',
                    'table_id': 'str',
                    'payload': 'Dict',
                    'debug': 'bool'
                },
                'usage': "success_message, payload = utility.push_to_backend('dataset_id', 'table_id', payload, debug=True)\nprint(success_message)",
                'example_values': {
                    'dataset_id': "'my_dataset'",
                    'table_id': "'my_table'",
                    'payload': "{'data': 'your_data'}",
                    'debug': 'True'
                }
            },
            'download_csv': {
                'parameters': {
                    'dataset_id': 'str',
                    'table_id': 'str',
                    'output_file': 'str'
                },
                'usage': "csv_path = utility.download_csv('dataset_id', 'table_id', 'output.csv')",
                'example_values': {
                    'dataset_id': "'my_dataset'",
                    'table_id': "'my_table'",
                    'output_file': "'downloaded_data.csv'"
                }
            },
            'download_json': {
                'parameters': {
                    'dataset_id': 'str',
                    'table_id': 'str',
                    'output_file': 'str'
                },
                'usage': "json_path = utility.download_json('dataset_id', 'table_id', 'output.json')",
                'example_values': {
                    'dataset_id': "'my_dataset'",
                    'table_id': "'my_table'",
                    'output_file': "'downloaded_data.json'"
                }
            },
            'parse_json': {
                'parameters': {'json_data': 'List[Dict]'},
                'usage': "df = utility.parse_json(json_data)",
                'example_values': {'json_data': '[{"th1": {"label": "col1"}, ...}, {"td1": {"label": "val1"}, ...}]'}
            },
            'create_temp_csv': {
                'parameters': {'table_data': 'pd.DataFrame'},
                'usage': "temp_file_path = Utility.create_temp_csv(df)",
                'example_values': {'table_data': 'your_dataframe'}
            },
            'create_zip_file': {
                'parameters': {
                    'df': 'pd.DataFrame',
                    'zip_filename': 'Optional[str]'
                },
                'usage': "zip_path = utility.create_zip_file(df, 'output.zip')",
                'example_values': {
                    'df': 'your_dataframe',
                    'zip_filename': "'output.zip'"
                }
            },
            'display_json_table': {
                'parameters': {
                    'json_table': 'dict',
                    'number_of_rows': 'Optional[int]',
                    'from_row': 'int',
                    'labels': 'Optional[List[str]]'
                },
                'usage': "html_table = Utility.display_json_table(json_table, number_of_rows=10, from_row=0, labels=['col1', 'col2'])",
                'example_values': {
                    'json_table': "{'columns': {...}, 'rows': {...}}",
                    'number_of_rows': '10',
                    'from_row': '0',
                    'labels': "['Name', 'Age']"
                }
            }
        }
        
        util_info = parameter_info.get(util_name, "Utility not found.")
        return self._format_utils_info(util_info)

    def _format_utils_info(self, util_info: dict) -> str:
        """
        Formats the utility information into a readable, structured output.
    
        Parameters:
        ----------
        util_info : dict
            Information dictionary about the utility, including parameters,
            usage, and example values.
    
        Returns:
        -------
        str
            A formatted string with readable output.
        """
        if isinstance(util_info, str):
            return util_info  # Handles the "Utility not found." case
        
        # Extract components for better readability
        parameters = util_info.get('parameters', {})
        usage = util_info.get('usage', 'No usage information available')
        example_values = util_info.get('example_values', {})
    
        # Create formatted output
        formatted_output = "### Utility Information\n"
        formatted_output += "\n**Parameters:**\n"
        for param, dtype in parameters.items():
            example = example_values.get(param, "N/A")
            formatted_output += f" - `{param}` ({dtype}): e.g., `{example}`\n"
    
        formatted_output += f"\n**Usage Example:**\n```python\n{usage}\n```\n"
        
        return formatted_output
    
    @staticmethod
    def explore_class_methods(cls) -> List[str]:
        """
        Explore all methods of a class, filtering for user-defined functions only.
        """
        # List all methods defined in the class
        return [name for name, func in inspect.getmembers(cls, inspect.isfunction)]

    @staticmethod
    def explore_submodules(submodules: List) -> Dict[str, Dict[str, List[str]]]:
        """
        Explore all classes in the given submodules and list their functions.

        """
        result = {}

        for module in submodules:
            print(f"\nExploring module: {module.__name__}")
            print("-" * 60)

            # Get all classes defined in the module
            classes = [name for name, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__]
            
            module_dict = {}
            for cls_name in classes:
                cls = getattr(module, cls_name)
                methods = Utility.explore_class_methods(cls)
                module_dict[cls_name] = methods

                # Print results for the user
                print(f"Class: {cls_name}")
                print(f"  Methods: {methods}")
            
            result[module.__name__] = module_dict

        return result

    def push_to_backend(self, dataset_id: str, table_id: str, payload: Dict, debug: bool = False) -> Tuple[str, Dict]:
        """
        Pushes the payload data to the backend API.

        """
        def send_request(data: Dict, url: str) -> requests.Response:
            try:
                response = requests.put(url, json=data, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                if debug:
                    print(f"Request failed: {str(e)}")
                return None
    
        # Log payload if enabled
        if debug:
            print("Payload being sent:")
            print(json.dumps(payload, indent=2))
    
        # Push to backend
        backend_url = urljoin(self.api_url, f"api/dataset/{dataset_id}/table/{table_id}")
        response = send_request(payload, backend_url)
    
        # Prepare output
        if response and response.status_code == 200:
            success_message = f"Updated Table successfully pushed to backend for table {table_id} in dataset {dataset_id}"
        else:
            status_code = response.status_code if response else "N/A"
            success_message = f"Failed to push to backend. Status code: {status_code}"
    
        # Log response if enabled
        if debug:
            if response:
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
            else:
                print("No response received from the server.")
    
        return success_message, payload
    
    def download_csv(self, dataset_id: str, table_id: str, output_file: str = "downloaded_data.csv") -> str:
        """
        Downloads a CSV file from the backend and saves it locally.
        """
        endpoint = f"/api/dataset/{dataset_id}/table/{table_id}/export"
        params = {"format": "csv"}
        url = urljoin(self.api_url, endpoint)

        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response.text)
            print(f"CSV file has been downloaded successfully and saved as {output_file}")
            return output_file
        else:
            raise Exception(f"Failed to download CSV. Status code: {response.status_code}")

    def download_json(self, dataset_id: str, table_id: str, output_file: str = "downloaded_data.json") -> str:
        """
        Downloads a JSON file in W3C format from the backend and saves it locally.
        """
        endpoint = f"/api/dataset/{dataset_id}/table/{table_id}/export"
        params = {"format": "w3c"}
        url = urljoin(self.api_url, endpoint)

        response = requests.get(url, params=params, headers=self.headers)

        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()
            
            # Save the JSON data to a file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"W3C JSON file has been downloaded successfully and saved as {output_file}")
            return output_file
        else:
            raise Exception(f"Failed to download W3C JSON. Status code: {response.status_code}")

    def parse_json(self, json_data: List[Dict]) -> pd.DataFrame:
        """
        Parses the W3C JSON format into a pandas DataFrame.
        """
        # Extract column names from the first item (metadata)
        columns = [key for key in json_data[0].keys() if key.startswith('th')]
        column_names = [json_data[0][col]['label'] for col in columns]

        # Extract data rows
        data_rows = []
        for item in json_data[1:]:  # Skip the first item (metadata)
            row = [item[col]['label'] for col in column_names]
            data_rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=column_names)
        return df
    
    @staticmethod
    def create_temp_csv(table_data: pd.DataFrame) -> str:
        """
        Creates a temporary CSV file from a DataFrame.
        
        Args:
            table_data (DataFrame): The table data to be written to the CSV file.
            
        Returns:
            str: The path of the temporary CSV file.
        """
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.csv') as temp_file:
            table_data.to_csv(temp_file, index=False)
            temp_file_path = temp_file.name
        
        return temp_file_path
    
    def create_zip_file(self, df: pd.DataFrame, zip_filename: Optional[str] = None) -> str:
        """
        Creates a zip file containing a CSV file from the given DataFrame.
        The zip file is created as a temporary file unless a filename is specified.

        Args:
            df (pandas.DataFrame): The DataFrame to be saved as a CSV file.
            zip_filename (str, optional): The path to the zip file to be created.

        Returns:
            str: The path to the created zip file.
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
    
    @staticmethod
    def display_json_table(json_table, number_of_rows=None, from_row=0, labels=None):
        """
        Displays a formatted HTML table from a JSON-based table structure with optional metadata.
    """
        # Set default number_of_rows if not provided
        if number_of_rows is None:
            number_of_rows = len(json_table['rows'])  # Show all rows by default

        # Set default labels if not provided (use all column labels)
        if labels is None:
            labels = list(json_table['columns'].keys())

        # Extracting rows and creating a DataFrame
        data = []
        columns_with_metadata = set()  # To keep track of columns that have metadata

        for i in range(from_row, from_row + number_of_rows):
            row_key = f'r{i}'
            if row_key not in json_table['rows']:
                continue

            row_value = json_table['rows'][row_key]
            row_data = {}
            
            # Iterate over the selected labels (columns)
            for label in labels:
                cell_data = row_value['cells'].get(label, {})
                cell_label = cell_data.get('label', 'N/A')
                cell_metadata = cell_data.get('metadata', [])

                row_data[label] = cell_label

                if cell_metadata:
                    columns_with_metadata.add(label)
                    # Structuring metadata as a formatted string for display using HTML
                    formatted_metadata = []
                    for meta in cell_metadata:
                        metadata_lines = [
                            f"<strong>ID:</strong> {meta.get('id', 'N/A')}<br>"
                        ]
                        if 'name' in meta:
                            if isinstance(meta['name'], dict):
                                metadata_lines.extend([
                                    f"<strong>Name:</strong> {meta['name'].get('value', 'N/A')}<br>",
                                    f"<strong>URI:</strong> <a href='{meta['name'].get('uri', '#')}'>{meta['name'].get('uri', 'N/A')}</a><br>"
                                ])
                            else:
                                metadata_lines.append(f"<strong>Name:</strong> {meta['name']}<br>")
                        
                        metadata_lines.extend([
                            f"<strong>Score:</strong> {meta.get('score', 'N/A')}<br>",
                            f"<strong>Match:</strong> {meta.get('match', 'N/A')}<br>"
                        ])
                        
                        if 'type' in meta and isinstance(meta['type'], list):
                            types = ', '.join(t.get('name', 'N/A') for t in meta['type'])
                            metadata_lines.append(f"<strong>Types:</strong> {types}")
                        
                        formatted_metadata.append("".join(metadata_lines))

                    # Combine all metadata entries into one string with double line breaks between them
                    formatted_metadata_str = "<br><br>".join(formatted_metadata)
                    row_data[f'{label}_metadata'] = formatted_metadata_str

            data.append(row_data)

        # Creating DataFrame
        df = pd.DataFrame(data)

        # Remove metadata columns for labels that don't have metadata
        columns_to_keep = labels + [f'{label}_metadata' for label in columns_with_metadata]
        df = df[columns_to_keep]

        # Displaying the DataFrame as a table with structured metadata using HTML rendering
        pd.set_option('display.max_colwidth', None)  # Allow full display of cell contents

        # Define CSS styles for better formatting
        html_output = df.to_html(escape=False, index=False)
        styled_output = f"""
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                vertical-align: top;
            }}
            td {{
                max-width: 300px;
                word-wrap: break-word;
                white-space: pre-wrap;
            }}
        </style>
        {html_output}
        """

        # Render the styled HTML output
        return HTML(styled_output)