import requests
import json
import copy
import datetime
import pandas as pd
from urllib.parse import urljoin
from .auth_manager import AuthManager
from typing import Dict, Any, Optional
import logging

class ReconciliationManager:
    """
    A class to manage reconciliation operations through API interactions.
    """

    def __init__(self, base_url, Auth_manager):
        """
        Initialize the ReconciliationManager with the base URL and token manager.
        """
        self.base_url = base_url.rstrip('/') + '/'
        self.api_url = urljoin(self.base_url, 'api/')
        self.Auth_manager = Auth_manager
        self.logger = logging.getLogger(__name__)

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate the headers required for API requests, including authorization.

        """
        return {
            'Authorization': f'Bearer {self.Auth_manager.get_token()}',
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept': 'application/json, text/plain, */*'
        }

    def _get_reconciliator_data(self, debug: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieves the list of available reconciliators from the server.

        Args:
        ----
        debug : bool
            If True, prints additional information like response status and headers.

        Returns:
        -------
        Optional[Dict[str, Any]]
            JSON response if successful, None otherwise.
        """
        try:
            url = urljoin(self.api_url, 'reconciliators/list')
            headers = self._get_headers()
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            if debug:
                print(f"Response status code: {response.status_code}")
                print(f"Response headers: {response.headers}")
                print(f"Response content (first 200 chars): {response.text[:200]}...")

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
                print(f"Request error occurred while retrieving reconciliator data: {e}")
                if hasattr(e, 'response') and e.response is not None:
                    print(f"Response status code: {e.response.status_code}")
                    print(f"Response content: {e.response.text[:200]}...")
            return None
        except json.JSONDecodeError as e:
            if debug:
                print(f"JSON decoding error: {e}")
                print(f"Raw response content: {response.text}")
            return None

    def get_reconciliators(self, debug: bool = False) -> pd.DataFrame:
        """
        Retrieves and cleans the list of reconciliators.

        """
        response = self._get_reconciliator_data(debug=debug)
        if response is not None:
            try:
                return self._clean_service_list(response)
            except Exception as e:
                if debug:
                    print(f"Error in clean_service_list: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    def _clean_service_list(self, service_list: Any) -> pd.DataFrame:
        """
        Cleans the raw service list and extracts necessary columns.

        Args:
        ----
        service_list : Any
            Raw list of reconciliator services.

        Returns:
        -------
        pd.DataFrame
            Cleaned DataFrame with selected columns.
        """
        if not isinstance(service_list, list):
            print(f"Expected a list, but got {type(service_list)}: {service_list}")
            return pd.DataFrame()

        reconciliators = []
        for reconciliator in service_list:
            if isinstance(reconciliator, dict) and all(key in reconciliator for key in ["id", "relativeUrl", "name"]):
                reconciliators.append({
                    "id": reconciliator["id"],
                    "relativeUrl": reconciliator["relativeUrl"],
                    "name": reconciliator["name"]
                })
            else:
                print(f"Skipping invalid reconciliator data: {reconciliator}")
        
        return pd.DataFrame(reconciliators)

    def _display_formatted_parameters(self, param_dict: Dict[str, Any], id_reconciliator: str):
        """
        Helper method to display formatted parameters.
    
        Args:
        ----
        param_dict : Dict[str, Any]
            The dictionary containing mandatory and optional parameters.
        id_reconciliator : str
            The ID of the reconciliator for reference in the print statement.
        """
        def print_param_details(param):
            print(f"\n  Parameter Name: {param['name']}")
            print(f"    - Type: {param['type']}")
            print(f"    - Mandatory: {'Yes' if param['mandatory'] else 'No'}")
            print(f"    - Description: {param['description']}")
            if 'label' in param and param['label']:
                print(f"    - Label: {param['label']}")
            if 'infoText' in param and param['infoText']:
                print(f"    - Info: {param['infoText']}")
    
        # Print header
        print(f"\n{'=' * 3} Reconciliator Parameters: {id_reconciliator} {'=' * 3}")
    
        # Print mandatory parameters
        if param_dict.get('mandatory'):
            print("\nMandatory Parameters:")
            for param in param_dict['mandatory']:
                print_param_details(param)
    
        # Print optional parameters
        if param_dict.get('optional'):
            print("\nOptional Parameters:")
            for param in param_dict['optional']:
                print_param_details(param)
    
        print("\n" + "=" * 50)

    def get_reconciliator_parameters(self, id_reconciliator: str, debug: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get reconciliator parameters and display them in a formatted way.
        """
        reconciliator_data = self._get_reconciliator_data(debug=debug)
        if not reconciliator_data:
            if debug:
                print(f"No reconciliator data retrieved for ID '{id_reconciliator}'.")
            return None
    
        mandatory_params = [
            {'name': 'table', 'type': 'json', 'mandatory': True, 'description': 'The table data in JSON format'},
            {'name': 'columnName', 'type': 'string', 'mandatory': True, 'description': 'The name of the column to reconcile'},
            {'name': 'idReconciliator', 'type': 'string', 'mandatory': True, 'description': 'The ID of the reconciliator to use'}
        ]
    
        for reconciliator in reconciliator_data:
            if reconciliator['id'] == id_reconciliator:
                parameters = reconciliator.get('formParams', [])
                
                optional_params = [
                    {
                        'name': param['id'],
                        'type': param['inputType'],
                        'mandatory': 'required' in param.get('rules', []),
                        'description': param.get('description', ''),
                        'label': param.get('label', ''),
                        'infoText': param.get('infoText', '')
                    } for param in parameters
                ]
    
                param_dict = {
                    'mandatory': mandatory_params,
                    'optional': optional_params
                }
    
                # Always display formatted parameters
                self._display_formatted_parameters(param_dict, id_reconciliator)
                return param_dict
    
        if debug:
            print(f"No parameters found for reconciliator with ID '{id_reconciliator}'.")
        return None

    def _prepare_input_data(self, original_input, column_name, reconciliator_id, optional_columns):
        """
        Prepare the input data for the reconciliation process.

        :param original_input: The original input data containing rows and columns.
        :param column_name: The name of the column to be reconciled.
        :param reconciliator_id: The ID of the reconciliator service to use.
        :param optional_columns: A list of optional columns to include in the reconciliation.
        :return: A dictionary representing the prepared input data for reconciliation.
        """
        input_data = {
            "serviceId": reconciliator_id,
            "items": [{"id": column_name, "label": column_name}],
            "secondPart": {},
            "thirdPart": {}
        }

        for row_id, row_data in original_input['rows'].items():
            main_column_value = row_data['cells'][column_name]['label']
            input_data['items'].append({"id": f"{row_id}${column_name}", "label": main_column_value})

            if reconciliator_id in ['geocodingHere', 'geocodingGeonames']:
                second_part_value = row_data['cells'].get(optional_columns[0], {}).get('label', '')
                third_part_value = row_data['cells'].get(optional_columns[1], {}).get('label', '')
                input_data['secondPart'][row_id] = [second_part_value, [], optional_columns[0]]
                input_data['thirdPart'][row_id] = [third_part_value, [], optional_columns[1]]

        return input_data

    def _send_reconciliation_request(self, input_data, reconciliator_id):
        """
        Send a reconciliation request to the specified reconciliator service.

        :param input_data: The input data prepared for reconciliation.
        :param reconciliator_id: The ID of the reconciliator service to use.
        :return: The JSON response from the reconciliator service, or None if an error occurs.
        """
        url = urljoin(self.api_url, f'reconciliators/{reconciliator_id}')
        headers = self._get_headers()
        
        try:
            response = requests.post(url, json=input_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error: {e}")
            return None

    def _compose_reconciled_table(self, original_input, reconciliation_output, column_name):
        """
        Compose a reconciled table from the original input and reconciliation output.

        :param original_input: The original input data containing rows and columns.
        :param reconciliation_output: The output data from the reconciliation process.
        :param column_name: The name of the column that was reconciled.
        :return: A dictionary representing the final reconciled table payload.
        """
        final_payload = copy.deepcopy(original_input)

        final_payload['table']['lastModifiedDate'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        final_payload['columns'][column_name]['status'] = 'reconciliated'
        final_payload['columns'][column_name]['context'] = {
            'georss': {
                'uri': 'http://www.google.com/maps/place/',
                'total': len(reconciliation_output) - 1,
                'reconciliated': len(reconciliation_output) - 1
            }
        }
        final_payload['columns'][column_name]['kind'] = 'entity'
        final_payload['columns'][column_name]['annotationMeta'] = {
            'annotated': True,
            'match': {'value': True},
            'lowestScore': 1,
            'highestScore': 1
        }

        column_metadata = next(item for item in reconciliation_output if item['id'] == column_name)
        final_payload['columns'][column_name]['metadata'] = column_metadata['metadata']

        nCellsReconciliated = 0
        for item in reconciliation_output:
            if item['id'] != column_name:
                row_id, cell_id = item['id'].split('$')
                cell = final_payload['rows'][row_id]['cells'][cell_id]

                metadata = item['metadata'][0]
                cell['metadata'] = [metadata]

                cell['annotationMeta'] = {
                    'annotated': True,
                    'match': {'value': metadata['match']},
                    'lowestScore': metadata['score'],
                    'highestScore': metadata['score']
                }
                nCellsReconciliated += 1

        final_payload['table']['nCellsReconciliated'] = nCellsReconciliated

        return final_payload

    def _restructure_payload(self, payload):
        """
        Restructure the payload to update metadata and annotation information.

        :param payload: The payload containing the reconciled data.
        :return: The restructured payload with updated metadata and annotations.
        """
        def create_google_maps_url(id_string):
            if id_string.startswith('georss:'):
                coords = id_string.split('georss:')[-1]
                return f"https://www.google.com/maps/place/{coords}"
            return ""  # Return empty string if id doesn't contain coordinates

        reconciliated_columns = [col_key for col_key, col in payload['columns'].items() if col.get('status') == 'reconciliated']

        for column_key in reconciliated_columns:
            column = payload['columns'][column_key]

            new_metadata = [{
                'id': 'None:',
                'match': True,
                'score': 0,
                'name': {'value': '', 'uri': ''},
                'entity': []
            }]

            for item in column.get('metadata', []):
                new_entity = {
                    'id': item['id'],
                    'name': {
                        'value': item['name'],
                        'uri': create_google_maps_url(item['id'])
                    },
                    'score': item.get('score', 0),
                    'match': item.get('match', True),
                    'type': item.get('type', [])
                }
                new_metadata[0]['entity'].append(new_entity)

            column['metadata'] = new_metadata

            scores = []
            for row in payload['rows'].values():
                cell = row['cells'].get(column_key)
                if cell and 'metadata' in cell and len(cell['metadata']) > 0:
                    score = cell['metadata'][0].get('score', 0)
                    scores.append(score)

            column['annotationMeta'] = {
                'annotated': True,
                'match': {'value': True, 'reason': 'reconciliator'},
                'lowestScore': min(scores) if scores else 0,
                'highestScore': max(scores) if scores else 0
            }

            if 'kind' in column:
                del column['kind']
        
        for row in payload['rows'].values():
            for cell_key, cell in row['cells'].items():
                if cell_key in reconciliated_columns:
                    if 'metadata' in cell:
                        for idx, item in enumerate(cell['metadata']):
                            new_item = {
                                'id': item['id'],
                                'name': {
                                    'value': item['name'],
                                    'uri': create_google_maps_url(item['id'])
                                },
                                'feature': item.get('feature', []),
                                'score': item.get('score', 0),
                                'match': item.get('match', True),
                                'type': item.get('type', [])
                            }
                            cell['metadata'][idx] = new_item

                    if 'annotationMeta' in cell:
                        cell['annotationMeta']['match'] = {'value': True, 'reason': 'reconciliator'}
                        if 'metadata' in cell and len(cell['metadata']) > 0:
                            score = cell['metadata'][0].get('score', 0)
                            cell['annotationMeta']['lowestScore'] = score
                            cell['annotationMeta']['highestScore'] = score

        return payload
    
    def _create_backend_payload(self, final_payload):
        """
        Create a backend payload from the final reconciled payload.

        :param final_payload: The final reconciled payload containing table data.
        :return: A dictionary representing the backend payload.
        """
        nCellsReconciliated = sum(
            1 for row in final_payload['rows'].values()
            for cell in row['cells'].values()
            if cell.get('annotationMeta', {}).get('annotated', False)
        )
        all_scores = [
            cell.get('annotationMeta', {}).get('lowestScore', float('inf'))
            for row in final_payload['rows'].values()
            for cell in row['cells'].values()
            if cell.get('annotationMeta', {}).get('annotated', False)
        ]
        minMetaScore = min(all_scores) if all_scores else 0
        maxMetaScore = max(all_scores) if all_scores else 1
    
        table_data = final_payload['table']
        columns = final_payload.get('columns', {})
        rows = final_payload.get('rows', {})
    
        backend_payload = {
            "tableInstance": {
                "id": table_data.get("id"),
                "idDataset": table_data.get("idDataset"),
                "name": table_data.get("name"),
                "nCols": table_data.get("nCols", 0),
                "nRows": table_data.get("nRows", 0),
                "nCells": table_data.get("nCells", 0),
                "nCellsReconciliated": nCellsReconciliated,
                "lastModifiedDate": table_data.get("lastModifiedDate", ""),
                "minMetaScore": minMetaScore,
                "maxMetaScore": maxMetaScore
            },
            "columns": {
                "byId": columns,
                "allIds": list(columns.keys())
            },
            "rows": {
                "byId": rows,
                "allIds": list(rows.keys())
            }
        }
    
        return backend_payload

    def reconcile(self, table_data, column_name, reconciliator_id, optional_columns):
        """
        Perform the reconciliation process on a specified column in the provided table data.
        """
        # Check if the provided reconciliator_id is valid
        if reconciliator_id not in ['geocodingHere', 'geocodingGeonames', 'geonames']:
            raise ValueError("Invalid reconciliator ID. Please use 'geocodingHere', 'geocodingGeonames', or 'geonames'.")
        
        # Prepare the input data required for reconciliation. This step may involve extracting the 
        # specified column and optional columns and formatting the data for the service's API.
        input_data = self._prepare_input_data(table_data, column_name, reconciliator_id, optional_columns)
        
        # Send the formatted data to the reconciliation service and get the response data.
        response_data = self._send_reconciliation_request(input_data, reconciliator_id)
        
        # Check if the reconciliation service responded with data
        if response_data:
            # Compose a reconciled table by merging the original input with the reconciliation results.
            final_payload = self._compose_reconciled_table(table_data, response_data, column_name)
            
            # Optionally restructure the final payload. This could involve updating metadata or 
            # reformatting the structure of the data.
            final_payload = self._restructure_payload(final_payload)
            
            # Create a backend-compatible payload which may include additional information required by backend systems.
            backend_payload = self._create_backend_payload(final_payload)
            
            # Return both the final payload (for internal use) and the backend payload.
            return final_payload, backend_payload
        else:
            # If no data was returned from the reconciliation service, return None values to indicate failure.
            return None, None
