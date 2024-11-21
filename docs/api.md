# API Reference

Welcome to the API reference for the SemT_py library. This section provides detailed documentation for all modules, classes, and functions available in the library.

## Auth Manager

The `AuthManager` class is responsible for managing authentication tokens for API access. It handles token retrieval, refreshing, and provides necessary headers for authenticated requests.

### Class Methods

::: semt_py.auth_manager.AuthManager
    options:
      members:
        - get_token
        - get_auth_list
        - get_auth_description
        - get_auth_parameters
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true

## Dataset Manager
The `DatasetManager` module provides functionality for managing datasets.

### Class Methods

::: semt_py.dataset_manager.DatasetManager
    options:
      members:
        - get_dataset_list
        - get_dataset_description
        - get_dataset_parameters
        - get_datasets
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true

## Table Manager
This class provides methods to interact with a table API, allowing users to retrieve lists of tables and perform other table-related operations.

### Class Methods

::: semt_py.table_manager.TableManager
    options:
      members:
        - get_table_description
        - get_table_parameters
        - get_tables
        - add_table
        - get_table
        - delete_tables
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true


## Modification Manager
The ModificationManager module provides functionality for managing and applying various modifications to DataFrames. It includes methods to modify date formats, change data types, reorder columns, and more.

### Class Methods
::: semt_py.modification_manager.ModificationManager
    options:
      members:
        - get_modifier_list
        - get_modifier_description
        - get_modifier_parameters
        - modify
        - lower_case
        - drop_na
        - rename_columns
        - convert_dtypes
        - reorder_columns
    show_source: true
    show_docstring: true
    show_signature: true
    heading_level: 3
    members_order: source
    docstring_style: numpy
    docstring_section_style: table
    separate_signature: true


## Extension Manager
The `ExtensionManager` module provides functionality for managing extensions through API interactions.

### Class Methods

::: semt_py.extension_manager.ExtensionManager
    options:
      members:
        - extend_column
        - get_extenders
        - get_extender_parameters
        - download_csv
        - download_json
        - parse_json
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true

## Reconciliation Manager
This class provides methods to interact with a reconciliation API, allowing users to retrieve lists of reconciliators and their parameters.

### Class Methods

::: semt_py.reconciliation_manager.ReconciliationManager
    options:
      members:
        - get_reconciliators
        - get_reconciliator_parameters
        - get_extender_parameters
        - reconcile
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true

## Utility 
A utility class providing various helper functions for API interactions.

### Class Methods

::: semt_py.utils.Utility
    options:
      members:
        - get_utils_list
        - get_utils_description
        - get_utils_parameters
        - explore_class_methods
        - explore_submodules
        - push_to_backend
        - download_csv
        - download_json
        - parse_json
        - display_json_table
      show_source: true
      show_docstring: true
      show_signature: true
      heading_level: 3
      members_order: source
      docstring_style: numpy
      docstring_section_style: table
      separate_signature: true
