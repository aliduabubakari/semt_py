import requests
import json
import copy
import pandas as pd
from urllib.parse import urljoin
from copy import deepcopy
from .Auth_manager import AuthManager
from typing import Dict, Any, Optional, Tuple, List

class ExtensionManager:
    """
    A class to manage extensions through API interactions.

    This class provides methods to interact with an extension API, allowing users
    to extend columns in a table using various extenders. It handles authentication
    via an API token.

    Attributes:
    ----------
    base_url : str
        The base URL for the API.
    token : str
        The authentication token for accessing the API.
    headers : dict
        The headers for API requests, including authorization.

    Methods:
    -------
    extend_column(table, column_name, extender_id, properties, other_params=None, debug=False)
        Standardized method to extend a column using a specified extender.
    """

    def __init__(self, base_url, token):
        """
        Initialize the ExtensionManager with the base URL and authentication token.

        :param base_url: The base URL for the API.
        :param token: The authentication token for accessing the API.
        """
        self.base_url = base_url.rstrip('/') + '/'
        self.api_url = urljoin(self.base_url, 'api/extenders')
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def _create_backend_payload(self, reconciled_json):
        """
        Create a payload for the backend from the reconciled JSON data.

        :param reconciled_json: The JSON data containing reconciled table information.
        :return: A dictionary representing the backend payload.
        """
        nCellsReconciliated = sum(
            1 for row in reconciled_json['rows'].values()
            for cell in row['cells'].values()
            if cell.get('annotationMeta', {}).get('annotated', False)
        )
        all_scores = [
            cell.get('annotationMeta', {}).get('lowestScore', float('inf'))
            for row in reconciled_json['rows'].values()
            for cell in row['cells'].values()
            if cell.get('annotationMeta', {}).get('annotated', False)
        ]
        minMetaScore = min(all_scores) if all_scores else 0
        maxMetaScore = max(all_scores) if all_scores else 1
        payload = {
            "tableInstance": {
                "id": reconciled_json['table']['id'],
                "idDataset": reconciled_json['table']['idDataset'],
                "name": reconciled_json['table']['name'],
                "nCols": reconciled_json["table"]["nCols"],
                "nRows": reconciled_json["table"]["nRows"],
                "nCells": reconciled_json["table"]["nCells"],
                "nCellsReconciliated": nCellsReconciliated,
                "lastModifiedDate": reconciled_json["table"]["lastModifiedDate"],
                "minMetaScore": minMetaScore,
                "maxMetaScore": maxMetaScore
            },
            "columns": {
                "byId": reconciled_json['columns'],
                "allIds": list(reconciled_json['columns'].keys())
            },
            "rows": {
                "byId": reconciled_json['rows'],
                "allIds": list(reconciled_json['rows'].keys())
            }
        }
        return payload

    def _prepare_input_data_meteo(self, table, reconciliated_column_name, id_extender, properties, date_column_name, decimal_format):
        """
        Prepare input data for the meteoPropertiesOpenMeteo extender.

        :param table: The input table containing data.
        :param reconciliated_column_name: The name of the reconciliated column.
        :param id_extender: The ID of the extender to use.
        :param properties: The properties to extend.
        :param date_column_name: The name of the date column.
        :param decimal_format: The format for decimal values.
        :return: A dictionary representing the payload for the extender.
        """
        dates = {row_id: [row['cells'][date_column_name]['label'], [], date_column_name] for row_id, row in table['rows'].items()} if date_column_name else {}
        items = {reconciliated_column_name: {row_id: row['cells'][reconciliated_column_name]['metadata'][0]['id'] for row_id, row in table['rows'].items()}}
        weather_params = properties if date_column_name else []
        decimal_format = [decimal_format] if decimal_format else []

        payload = {
            "serviceId": id_extender,
            "dates": dates,
            "decimalFormat": decimal_format,
            "items": items,
            "weatherParams": weather_params
        }
        return payload

    def _prepare_input_data_reconciled(self, table, reconciliated_column_name, properties, id_extender):
        """
        Prepare input data for a reconciled column extender.

        :param table: The input table containing data.
        :param reconciliated_column_name: The name of the reconciliated column.
        :param properties: The properties to extend.
        :param id_extender: The ID of the extender to use.
        :return: A dictionary representing the payload for the extender.
        """
        column_data = {
            row_id: [
                row['cells'][reconciliated_column_name]['label'],
                row['cells'][reconciliated_column_name].get('metadata', []),
                reconciliated_column_name
            ] for row_id, row in table['rows'].items()
        }
        items = {
            reconciliated_column_name: {
                row_id: row['cells'][reconciliated_column_name]['metadata'][0]['id']
                for row_id, row in table['rows'].items()
                if 'metadata' in row['cells'][reconciliated_column_name] and row['cells'][reconciliated_column_name]['metadata']
            }
        }

        payload = {
            "serviceId": id_extender,
            "column": column_data,
            "property": properties,
            "items": items
        }
        return payload

    def _send_extension_request(self, payload, debug=False):
        """
        Send a request to the extender service with the given payload.

        :param payload: The payload to send to the extender service.
        :param debug: Boolean flag to enable/disable debug information.
        :return: The JSON response from the extender service.
        :raises: HTTPError if the request fails.
        """
        try:
            if debug:
                print("Sending payload to extender service:")
                print(json.dumps(payload, indent=2))
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            if debug:
                print("Received response from extender service:")
                print(f"Status Code: {response.status_code}")
                print(f"Response Content: {response.text}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if debug:
                print(f"HTTP error occurred: {http_err}")
                if response is not None:
                    print(f"Response Content: {response.text}")
            raise
        except Exception as err:
            if debug:
                print(f"An error occurred: {err}")
            raise

    def _compose_extension_table(self, table, extension_response):
        """
        Compose an extended table from the extension response.

        :param table: The original table to extend.
        :param extension_response: The response from the extender service.
        :return: The extended table with new columns added.
        """
        for column_name, column_data in extension_response['columns'].items():
            table['columns'][column_name] = {
                'id': column_name,
                'label': column_data['label'],
                'status': 'extended',
                'context': {},
                'metadata': [],
                'kind': 'extended',
                'annotationMeta': {}
            }
            for row_id, cell_data in column_data['cells'].items():
                table['rows'][row_id]['cells'][column_name] = {
                    'id': f"{row_id}${column_name}",
                    'label': cell_data['label'],
                    'metadata': cell_data['metadata']
                }
        return table

    def extend_column(self, table, column_name, extender_id, properties, other_params=None, debug=False):
        """
        Standardized method to extend a column using a specified extender.

        This method prepares the input data, sends a request to the extender service,
        and composes the extended table from the response.

        :param table: The input table containing data.
        :param column_name: The name of the column to extend.
        :param extender_id: The ID of the extender to use.
        :param properties: The properties to extend.
        :param other_params: A dictionary of additional parameters (optional).
        :param debug: Boolean flag to enable/disable debug information.

        Returns:
        -------
        Tuple[Dict, Dict]
            A tuple containing the extended table and the backend payload.

        Usage:
        -----
        # Initialize the ExtensionManager with API credentials
        base_url = "https://api.example.com"
        token = "your_api_token"
        extension_manager = ExtensionManager(base_url, token)

        # Call for meteoPropertiesOpenMeteo
        meteo_extended_table, meteo_extension_payload = extension_manager.extend_column(
            table=reconciled_table,
            column_name='City',
            extender_id="meteoPropertiesOpenMeteo",
            properties=['apparent_temperature_max', 'apparent_temperature_min', 'precipitation_sum', 'precipitation_hours'],
            other_params={
                'date_column_name': "Fecha_id",
                'decimal_format': "comma"
            })

        # Call for reconciledColumnExt
        reconciled_extended_table, reconciled_backend_payload = extension_manager.extend_column(
            table=meteo_extended_table,
            column_name='City',
            extender_id='reconciledColumnExt',
            properties=['id', 'name'],
            other_params={}  # Empty dictionary for reconciledColumnExt
        )
        """
        other_params = other_params or {}

        if extender_id == 'reconciledColumnExt':
            input_data = self._prepare_input_data_reconciled(table, column_name, properties, extender_id)
        elif extender_id == 'meteoPropertiesOpenMeteo':
            date_column_name = other_params.get('date_column_name')
            decimal_format = other_params.get('decimal_format')
            if not date_column_name or not decimal_format:
                raise ValueError("date_column_name and decimal_format are required for meteoPropertiesOpenMeteo extender")
            input_data = self._prepare_input_data_meteo(table, column_name, extender_id, properties, date_column_name, decimal_format)
        else:
            raise ValueError(f"Unsupported extender: {extender_id}")

        extension_response = self._send_extension_request(input_data, debug)
        extended_table = self._compose_extension_table(table, extension_response)
        backend_payload = self._create_backend_payload(extended_table)

        if debug:
            print("Extended table:", json.dumps(extended_table, indent=2))
            print("Backend payload:", json.dumps(backend_payload, indent=2))
        else:
            print("Column extended successfully!")

        return extended_table, backend_payload

    def _get_extender_data(self, debug=False):
        """
        Retrieves extender data from the backend with optional debug output.

        :param debug: If True, print detailed debug information.
        :return: JSON data from the API if successful, None otherwise.
        """
        try:
            # Correctly construct the URL
            url = urljoin(self.api_url, 'extenders/list')
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Debugging output
            if debug:
                print(f"Response status code: {response.status_code}")
                print(f"Response headers: {response.headers}")
                print(f"Response content: {response.text[:500]}...")  # Print first 500 characters for clarity
            
            # Check if the response is JSON
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' not in content_type:
                if debug:
                    print(f"Unexpected content type: {content_type}")
                    print("Full response content:")
                    print(response.text)
                return None

            return response.json()
        except requests.RequestException as e:
            if debug:
                print(f"Error occurred while retrieving extender data: {e}")
                if e.response is not None:
                    print(f"Response status code: {e.response.status_code}")
                    print(f"Response content: {e.response.text[:500]}...")  # Show first 500 characters of error content
            return None
        except json.JSONDecodeError as e:
            if debug:
                print(f"JSON decoding error: {e}")
                print(f"Raw response content: {response.text}")
            return None
    
    def _clean_service_list(self, service_list):
        """
        Cleans and formats the service list into a DataFrame.

        :param service_list: Data regarding available services.
        :return: DataFrame containing extenders' information.
        """
        # Initialize a DataFrame with the specified columns
        reconciliators = pd.DataFrame(columns=["id", "relativeUrl", "name"])
        
        # Populate the DataFrame with the extenders' information
        for reconciliator in service_list:
            reconciliators.loc[len(reconciliators)] = [
                reconciliator["id"], reconciliator.get("relativeUrl", ""), reconciliator["name"]
            ]
        
        return reconciliators
    
    def get_extenders(self, debug=False):
        """
        Provides a list of available extenders with their main information.

        :param debug: If True, prints detailed debug information.
        :return: DataFrame containing extenders and their information.
        """
        response = self._get_extender_data(debug=debug)
        if response:
            df = self._clean_service_list(response)
            if debug:
                print("Retrieved Extenders List:")
                print(df)
            return df
        else:
            if debug:
                print("Failed to retrieve extenders data.")
            return None

    def get_extender_parameters(self, extender_id, print_params=False):
        """
        Retrieves and formats the parameters needed for a specific extender service in a readable vertical structure.
    
        :param extender_id: The ID of the extender service.
        :param print_params: (optional) Whether to print the retrieved parameters or not.
        :return: A formatted string of the extender parameters, or None if the extender is not found.
        """
        
        def format_extender_params(param_dict):
            """
            Formats the extender parameters dictionary into a well-structured vertical format for readability.
    
            :param param_dict: The dictionary containing extender parameters.
            :return: Formatted string with mandatory and optional parameters.
            """
            output = []
            output.append("=== Extender Parameters ===\n")
            
            # Process mandatory parameters
            output.append("Mandatory Parameters:\n")
            if param_dict['mandatory']:
                for param in param_dict['mandatory']:
                    output.append(f"  Parameter Name: {param['name']}")
                    output.append(f"    - Type: {param['type']}")
                    output.append(f"    - Mandatory: Yes")
                    output.append(f"    - Description: {param['description']}")
                    output.append(f"    - Label: {param['label']}")
                    if param['infoText']:
                        output.append(f"    - Info: {param['infoText']}")
                    if param['options']:
                        options_str = ', '.join([opt['label'] for opt in param['options']])
                        output.append(f"    - Options: {options_str}")
                    output.append("")  # Add a blank line between parameters
            else:
                output.append("  No mandatory parameters available.\n")
    
            # Process optional parameters
            output.append("Optional Parameters:\n")
            if param_dict['optional']:
                for param in param_dict['optional']:
                    output.append(f"  Parameter Name: {param['name']}")
                    output.append(f"    - Type: {param['type']}")
                    output.append(f"    - Mandatory: No")
                    output.append(f"    - Description: {param['description']}")
                    output.append(f"    - Label: {param['label']}")
                    if param['infoText']:
                        output.append(f"    - Info: {param['infoText']}")
                    if param['options']:
                        options_str = ', '.join([opt['label'] for opt in param['options']])
                        output.append(f"    - Options: {options_str}")
                    output.append("")  # Add a blank line between parameters
            else:
                output.append("  No optional parameters available.\n")
    
            return "\n".join(output)
        
        # Retrieve extender data
        extender_data = self._get_extender_data()
        if not extender_data:
            print(f"No data found for extender ID '{extender_id}'.")
            return None
        
        # Find the specific extender by ID
        for extender in extender_data:
            if extender['id'] == extender_id:
                parameters = extender.get('formParams', [])
                # Organize parameters into mandatory and optional
                mandatory_params = [
                    {
                        'name': param['id'],
                        'type': param['inputType'],
                        'mandatory': 'required' in param.get('rules', []),
                        'description': param.get('description', ''),
                        'label': param.get('label', ''),
                        'infoText': param.get('infoText', ''),
                        'options': param.get('options', [])
                    } for param in parameters if 'required' in param.get('rules', [])
                ]
                optional_params = [
                    {
                        'name': param['id'],
                        'type': param['inputType'],
                        'mandatory': 'required' in param.get('rules', []),
                        'description': param.get('description', ''),
                        'label': param.get('label', ''),
                        'infoText': param.get('infoText', ''),
                        'options': param.get('options', [])
                    } for param in parameters if 'required' not in param.get('rules', [])
                ]
                
                # Combine into parameter dictionary
                param_dict = {
                    'mandatory': mandatory_params,
                    'optional': optional_params
                }
    
                # Format the output
                formatted_output = format_extender_params(param_dict)
                
                # Print the formatted parameters if requested
                if print_params:
                    print(formatted_output)
    
                return formatted_output
    
        # If the extender was not found
        print(f"Extender with ID '{extender_id}' not found.")
        return None
    
    def download_csv(self, dataset_id: str, table_id: str, output_file: str = "downloaded_data.csv") -> str:
        """
        Downloads a CSV file from the backend and saves it locally.
        Args:
            dataset_id (str): The ID of the dataset as a string.
            table_id (str): The ID of the table as a string.
            output_file (str): The name of the file to save the CSV data to. Defaults to "downloaded_data.csv".
        Returns:
            str: The path to the downloaded CSV file.
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

        Args:
            dataset_id (str): The ID of the dataset as a string.
            table_id (str): The ID of the table as a string.
            output_file (str): The name of the file to save the JSON data to. Defaults to "downloaded_data.json".

        Returns:
            str: The path to the downloaded JSON file.
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

        Args:
            json_data (List[Dict]): The W3C JSON data.

        Returns:
            pd.DataFrame: A DataFrame containing the parsed data.
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
    