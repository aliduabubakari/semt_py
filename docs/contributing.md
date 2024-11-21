# Contributing Guide

## Table of Contents
- [Introduction](#introduction)
- [Adding New Reconciliation Services](#adding-new-reconciliation-services)
  - [Overview](#reconciliator-overview)
  - [Implementation Steps](#reconciliator-implementation)
  - [Integration Guide](#reconciliator-integration)
  - [Testing Requirements](#reconciliator-testing)
  - [Example Implementation](#reconciliation-example)
- [Adding New Extension Services](#adding-new-extension-services)
  - [Overview](#extension-overview)
  - [Implementation Steps](#extension-implementation)
  - [Integration Guide](#extension-integration)
  - [Testing Requirements](#extension-testing)
  - [Example Implementation](#extension-example)
- [Adding New Modification Services](#adding-new-modification-services)
  - [Overview](#modificator-overview)
  - [Implementation Steps](#modificator-implementation)
  - [Integration Guide](#modificator-integration)
  - [Testing Requirements](#modificator-testing)
  - [Example Implementation](#modificator-example)  
- [General Guidelines](#general-guidelines)
  - [Code Style](#code-style)
  - [Documentation Standards](#documentation-standards)
  - [Error Handling](#error-handling)
  - [Testing Best Practices](#testing-best-practices)
- [Submission Process](#submission-process)
  - [Pull Request Guidelines](#pull-request-guidelines)
  - [Code Review Process](#code-review-process)

## Introduction

This guide provides detailed instructions for contributing new reconciliators and extension services to the SemT_py library. Follow these guidelines to ensure your contributions maintain code quality and consistency.

## Adding New Reconciliation Services

### Reconciliator Overview

The ReconciliationManager is designed to be extensible, allowing developers to add new reconciliation services. This guide outlines the process of implementing and integrating new reconciliators while maintaining code quality and consistency.

### Reconciliator Implementation
#### Core Components

Every new reconciliator requires implementation of three main components:

```python
class ReconciliationManager:
    def _prepare_input_data_new_reconciliator(self, table, column_name, options):
        """
        Prepare data for the new reconciliation service.

        Args:
            table (Dict): Input table data
            column_name (str): Target column name
            options (Dict): Additional options

        Returns:
            Dict: Formatted input data for the reconciliation service
        """
        pass

    def _send_reconciliation_request_new(self, input_data, debug=False):
        """
        Handle API communication with the new reconciliation service.

        Args:
            input_data (Dict): Prepared input data
            debug (bool): Enable debug output

        Returns:
            Dict: Response from the reconciliation service
        """
        pass

    def _process_reconciliation_response_new(self, response_data, original_data):
        """
        Process the response from the new reconciliation service.

        Args:
            response_data (Dict): Service response
            original_data (Dict): Original input data

        Returns:
            Dict: Processed reconciliation results
        """
        pass
```

#### Required Methods

Implement these essential methods for your reconciliator:

```python
def _validate_new_reconciliator_input(self, data: Dict) -> bool:
    """
    Validate input data for the new reconciliator.

    Args:
        data (Dict): Input data to validate

    Returns:
        bool: True if valid, False otherwise

    Raises:
        ValueError: If validation fails
    """
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary")
    
    required_fields = ['column_name', 'data']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    return True

def _format_new_reconciliator_output(self, data: Dict) -> Dict:
    """
    Format output data from the new reconciliator.

    Args:
        data (Dict): Raw reconciliation results

    Returns:
        Dict: Formatted results matching expected schema
    """
    return {
        "status": "success",
        "results": data,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "reconciliator": "new_reconciliator"
        }
    }
```

### Reconciliator Integration

#### 1. Register the Reconciliator

Add your reconciliator to the available services:

```python
class ReconciliationManager:
    def __init__(self, base_url, Auth_manager):
        self.reconciliators = {
            'geocodingHere': self._reconcile_geocoding_here,
            'geocodingGeonames': self._reconcile_geocoding_geonames,
            'new_reconciliator': self._reconcile_new_service  # Add your reconciliator
        }
```

#### 2. Define Parameters

Add parameter definitions for your reconciliator:

```python
def get_reconciliator_parameters(self, id_reconciliator: str) -> Dict:
    if id_reconciliator == 'new_reconciliator':
        return {
            'mandatory': [
                {
                    'name': 'column_name',
                    'type': 'string',
                    'description': 'Column to reconcile'
                }
            ],
            'optional': [
                {
                    'name': 'threshold',
                    'type': 'float',
                    'description': 'Matching threshold',
                    'default': 0.8
                }
            ]
        }
```

#### 3. Implement Error Handling

Add comprehensive error handling:

```python
def _handle_new_reconciliator_errors(self, error: Exception) -> Dict:
    """
    Handle errors from the new reconciliator.

    Args:
        error (Exception): The caught exception

    Returns:
        Dict: Error information
    """
    error_mapping = {
        ValueError: "Invalid input data",
        requests.RequestException: "API communication error",
        json.JSONDecodeError: "Invalid response format"
    }

    error_type = type(error)
    error_message = error_mapping.get(error_type, "Unknown error")

    return {
        "status": "error",
        "error_type": error_type.__name__,
        "message": error_message,
        "details": str(error)
    }
```

### Reconciliator Testing

#### 1. Unit Tests

Create comprehensive unit tests:

```python
def test_new_reconciliator():
    """Test the new reconciliator functionality"""
    # Setup
    reconciliation_manager = ReconciliationManager(base_url, auth_manager)
    test_data = {
        "column_name": "test_column",
        "data": [{"id": 1, "value": "test"}]
    }

    # Test validation
    assert reconciliation_manager._validate_new_reconciliator_input(test_data)

    # Test reconciliation
    result = reconciliation_manager.reconcile(
        test_data,
        "test_column",
        "new_reconciliator",
        []
    )
    assert result is not None
```

#### 2. Integration Tests

Test integration with existing systems:

```python
def test_new_reconciliator_integration():
    """Test integration with existing reconciliation workflow"""
    # Setup
    manager = ReconciliationManager(base_url, auth_manager)
    
    # Test workflow
    result = manager.reconcile(
        sample_table,
        "location",
        "new_reconciliator",
        ["city", "country"]
    )
    
    # Verify results
    assert result[0] is not None  # Check final payload
    assert result[1] is not None  # Check backend payload
```

## Reconciliation Example

### Complete Reconciliator Implementation

```python
class ReconciliationManager:
    def _reconcile_new_service(self, table_data: Dict, 
                             column_name: str,
                             options: Dict = None) -> Tuple[Dict, Dict]:
        """
        Complete implementation of a new reconciliation service.
        """
        try:
            # Validate input
            self._validate_new_reconciliator_input({
                "column_name": column_name,
                "data": table_data
            })

            # Prepare data
            input_data = self._prepare_input_data_new_reconciliator(
                table_data, column_name, options
            )

            # Send request
            response = self._send_reconciliation_request_new(input_data)

            # Process response
            results = self._process_reconciliation_response_new(
                response, table_data
            )

            # Format output
            final_payload = self._format_new_reconciliator_output(results)
            backend_payload = self._create_backend_payload(final_payload)

            return final_payload, backend_payload

        except Exception as e:
            error_info = self._handle_new_reconciliator_errors(e)
            self.logger.error(f"Reconciliation failed: {error_info}")
            return None, None
```


## Adding New Extension Services

### Extension Overview

The ExtensionManager is designed to be extensible, allowing developers to add new extension services. This guide provides detailed instructions for implementing and integrating new extension services while maintaining code quality and consistency.

### Extension Implementation
#### Core Components

Every new extension service requires implementation of three main components:

```python
class ExtensionManager:
    def _prepare_extension_data(self, table: Dict, column_name: str, properties: List[str]) -> Dict:
        """
        Prepare data for the new extension service.

        Args:
            table (Dict): Input table data
            column_name (str): Target column name
            properties (List[str]): Properties to extend

        Returns:
            Dict: Formatted input data for the extension service
        """
        return {
            "serviceId": "new_extension_service",
            "items": self._format_items(table, column_name),
            "properties": properties
        }

    def _send_extension_request(self, input_data: Dict, debug: bool = False) -> Dict:
        """
        Handle API communication with the new extension service.

        Args:
            input_data (Dict): Prepared input data
            debug (bool): Enable debug output

        Returns:
            Dict: Response from the extension service
        """
        url = urljoin(self.api_url, 'extensions/new_service')
        response = requests.post(url, json=input_data, headers=self._get_headers())
        return response.json()

    def _process_extension_response(self, response: Dict, original_table: Dict) -> Dict:
        """
        Process the response from the new extension service.

        Args:
            response (Dict): Service response
            original_table (Dict): Original input table

        Returns:
            Dict: Processed extension results
        """
        return self._compose_extension_table(original_table, response)
```

#### Required Methods

Implement these essential methods for your extension service:

```python
def _validate_extension_input(self, data: Dict) -> bool:
    """
    Validate input data for the new extension service.

    Args:
        data (Dict): Input data to validate

    Returns:
        bool: True if valid, False otherwise

    Raises:
        ValueError: If validation fails
    """
    required_fields = ['column_name', 'properties']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
    
    return True

def _format_extension_output(self, data: Dict) -> Dict:
    """
    Format output data from the extension service.

    Args:
        data (Dict): Raw extension results

    Returns:
        Dict: Formatted results matching expected schema
    """
    return {
        "extended_table": data,
        "metadata": {
            "extension_service": "new_service",
            "timestamp": datetime.now().isoformat(),
            "properties": data.get("properties", [])
        }
    }
```

### Extension Integration
#### 1. Register the Extension Service

Add your extension service to the available services:

```python
class ExtensionManager:
    def __init__(self, base_url: str, token: str):
        self.extension_services = {
            'meteoPropertiesOpenMeteo': self._extend_meteo_properties,
            'reconciledColumnExt': self._extend_reconciled_column,
            'new_extension_service': self._extend_new_service  # Add your service
        }
```

#### 2. Define Service Parameters

Add parameter definitions for your extension service:

```python
def get_extender_parameters(self, extender_id: str) -> Dict:
    """Define parameters for the new extension service."""
    if extender_id == 'new_extension_service':
        return {
            'mandatory': [
                {
                    'name': 'column_name',
                    'type': 'string',
                    'description': 'Column to extend'
                },
                {
                    'name': 'properties',
                    'type': 'array',
                    'description': 'Properties to add'
                }
            ],
            'optional': [
                {
                    'name': 'options',
                    'type': 'object',
                    'description': 'Additional options'
                }
            ]
        }
```

#### 3. Implement Error Handling

Add comprehensive error handling:

```python
def _handle_extension_errors(self, error: Exception) -> Dict:
    """
    Handle errors from the extension service.

    Args:
        error (Exception): The caught exception

    Returns:
        Dict: Error information
    """
    error_types = {
        ValueError: "Invalid input data",
        requests.RequestException: "API communication error",
        json.JSONDecodeError: "Invalid response format"
    }

    error_info = {
        "status": "error",
        "error_type": type(error).__name__,
        "message": error_types.get(type(error), "Unknown error"),
        "details": str(error)
    }

    self.logger.error(f"Extension error: {error_info}")
    return error_info
```

### Extension Testing
#### 1. Unit Tests

Create comprehensive unit tests:

```python
def test_new_extension_service():
    """Test the new extension service functionality."""
    # Setup
    extension_manager = ExtensionManager(base_url, token)
    test_data = {
        "column_name": "test_column",
        "properties": ["property1", "property2"]
    }

    # Test validation
    assert extension_manager._validate_extension_input(test_data)

    # Test extension
    result = extension_manager.extend_column(
        table=sample_table,
        column_name="test_column",
        extender_id="new_extension_service",
        properties=["property1", "property2"]
    )
    assert result is not None
```

#### 2. Integration Tests

Test integration with existing systems:

```python
def test_extension_integration():
    """Test integration with existing extension workflow."""
    manager = ExtensionManager(base_url, token)
    
    # Test complete workflow
    extended_table, backend_payload = manager.extend_column(
        table=sample_table,
        column_name="location",
        extender_id="new_extension_service",
        properties=["property1", "property2"],
        other_params={"option1": "value1"}
    )
    
    # Verify results
    assert extended_table is not None
    assert backend_payload is not None
```


### Extension Example
#### Complete Extension Service Implementation

```python
class ExtensionManager:
    def _extend_new_service(
        self,
        table: Dict,
        column_name: str,
        properties: List[str],
        options: Dict = None,
        debug: bool = False
    ) -> Tuple[Dict, Dict]:
        """
        Complete implementation of a new extension service.
        """
        try:
            # Validate input
            self._validate_extension_input({
                "column_name": column_name,
                "properties": properties
            })

            # Prepare data
            input_data = self._prepare_extension_data(
                table, column_name, properties
            )

            # Send request
            response = self._send_extension_request(
                input_data, debug=debug
            )

            # Process response
            extended_table = self._process_extension_response(
                response, table
            )

            # Create backend payload
            backend_payload = self._create_backend_payload(extended_table)

            return extended_table, backend_payload

        except Exception as e:
            error_info = self._handle_extension_errors(e)
            self.logger.error(f"Extension failed: {error_info}")
            return None, None
```

## Adding New Modification Services

### Modificator Overview

The Modification Services system allows developers to extend the data transformation capabilities of the platform by adding new modification techniques. These services are managed through the ModificationManager class and can be used to perform various data transformation operations on DataFrames.

### Modificator Implementation

1. **Create the Modifier Method**
   - Define a new static method in the ModificationManager class
   - Method should accept a pandas DataFrame as its first parameter
   - Include any additional parameters needed for the modification
   - Ensure proper type hints and return types
   - Implement comprehensive error handling

2. **Register the Modifier**
   - Add the new modifier to the ModificationManager's modifiers dictionary
   - Choose a descriptive key that clearly represents the modifier's function
   - Update the initialization method accordingly

3. **Document the Modifier**
   - Add comprehensive docstrings following the established format
   - Include parameter descriptions, return types, and usage examples
   - Document any raised exceptions or special cases

### Modificator Integration

1. **Method Signature**
```python
@staticmethod
def new_modifier(df: pd.DataFrame, param1: str, param2: int) -> pd.DataFrame:
    """
    Brief description of what the modifier does.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.
    - param1 (str): Description of the first parameter.
    - param2 (int): Description of the second parameter.

    Returns:
    - pd.DataFrame: Modified DataFrame.

    Raises:
    - ValueError: If any parameter is invalid.
    """
    pass
```

2. **Registration in ModificationManager**
```python
def __init__(self):
    self.modifiers = {
        'existing_modifier': self.existing_modifier,
        'new_modifier': self.new_modifier  # Add your new modifier here
    }
```

3. **Documentation Updates**
```python
def get_modifier_description(self, modifier_name):
    descriptions = {
        'existing_modifier': "Existing modifier description",
        'new_modifier': "Description of the new modifier"
    }
    return descriptions.get(modifier_name, "Modifier not found.")
```

### Modificator Testing

1. **Unit Tests**
   - Test the modifier with valid inputs
   - Test edge cases and boundary conditions
   - Verify error handling for invalid inputs
   - Ensure DataFrame integrity is maintained
   - Test performance with various data sizes

2. **Integration Tests**
   - Verify compatibility with existing modifiers
   - Test modifier chains and combinations
   - Validate memory usage and performance
   - Check for any side effects on the DataFrame

### Modificator Example

Here's a complete example of adding a new modifier that converts text to uppercase:

```python
class ModificationManager:
    @staticmethod
    def to_uppercase(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Convert text in specified column to uppercase.

        Parameters:
        - df (pd.DataFrame): Input DataFrame
        - column (str): Column name to modify

        Returns:
        - pd.DataFrame: Modified DataFrame

        Raises:
        - ValueError: If column doesn't exist or isn't string type
        """
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        if not pd.api.types.is_string_dtype(df[column]):
            raise ValueError(f"Column '{column}' must be string type")
            
        df = df.copy()
        df[column] = df[column].str.upper()
        return df

    def __init__(self):
        self.modifiers = {
            'to_uppercase': self.to_uppercase
        }

    def get_modifier_description(self, modifier_name):
        descriptions = {
            'to_uppercase': "Converts text in specified column to uppercase"
        }
        return descriptions.get(modifier_name, "Modifier not found.")
```

## General Guidelines

### Code Style

#### Python Style Guidelines
- Follow PEP 8 conventions for Python code
- Use 4 spaces for indentation
- Maximum line length of 88 characters (compatible with black formatter)
- Use snake_case for functions and variables
- Use PascalCase for class names
- Use descriptive variable names that indicate purpose

#### Naming Conventions
```python
# Good examples
def calculate_total_revenue(sales_data):
    monthly_revenue = 0
    
# Avoid
def calc(d):
    x = 0
```

#### Import Organization
```python
# Standard library imports
from datetime import datetime
from typing import Dict, List, Tuple

# Third-party imports
import requests
import pandas as pd

# Local application imports
from semt_py.utils import logger
from semt_py.managers.base import BaseManager
```

### Documentation Standards

#### Method Documentation
All methods must include comprehensive docstrings following this format:

```python
def process_data(
    self,
    input_data: Dict[str, Any],
    options: Optional[Dict] = None,
    debug: bool = False
) -> Tuple[Dict, Dict]:
    """
    Process input data using specified options and return processed results.

    Args:
        input_data (Dict[str, Any]): The input data to process, containing:
            - column_name (str): Name of the target column
            - data (List[Dict]): List of data entries
        options (Optional[Dict], optional): Additional processing options. Defaults to None.
            - threshold (float): Matching threshold (0-1)
            - limit (int): Maximum number of results
        debug (bool, optional): Enable debug output. Defaults to False.

    Returns:
        Tuple[Dict, Dict]: A tuple containing:
            - First Dict: Processed results with the following structure:
                {
                    "status": "success",
                    "results": List[Dict],
                    "metadata": Dict
                }
            - Second Dict: Backend payload for logging/tracking

    Raises:
        ValueError: If input_data is missing required fields
        TypeError: If input types are incorrect
        RequestException: If external API communication fails
    """
    pass
```

#### Class Documentation
All classes must include docstrings describing their purpose and usage:

```python
class DataProcessor:
    """
    Handles data processing operations for the SemT_py library.

    This class provides methods for data validation, transformation,
    and enrichment. It supports both synchronous and asynchronous
    processing modes.

    Attributes:
        base_url (str): Base URL for API endpoints
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum number of retry attempts

    Example:
        >>> processor = DataProcessor(base_url="https://api.example.com")
        >>> result = processor.process_data({"column": "value"})
    """
```

#### Module Documentation
Each module should include a module-level docstring:

```python
"""
semt_py.processors.data_processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains the core data processing functionality for the SemT_py library.
It provides classes and functions for data validation, transformation, and enrichment.

Key Classes:
    - DataProcessor: Main class for data processing operations
    - ValidationHandler: Handles input validation
    - TransformationEngine: Manages data transformations

Example Usage:
    >>> from semt_py.processors import DataProcessor
    >>> processor = DataProcessor()
    >>> result = processor.process_data(input_data)
"""
```

### Error Handling

#### Exception Hierarchy
```python
class SemTPyError(Exception):
    """Base exception class for SemT_py library."""
    pass

class ValidationError(SemTPyError):
    """Raised when input validation fails."""
    pass

class ProcessingError(SemTPyError):
    """Raised when data processing fails."""
    pass

class APIError(SemTPyError):
    """Raised when API communication fails."""
    pass
```

#### Error Handling Pattern
```python
def process_data(self, data: Dict) -> Dict:
    """Process data with proper error handling."""
    try:
        # Validate input
        if not self._validate_input(data):
            raise ValidationError("Invalid input format")

        # Process data
        result = self._process(data)
        
        # Validate output
        if not self._validate_output(result):
            raise ProcessingError("Processing failed")
            
        return result

    except ValidationError as e:
        self.logger.error(f"Validation failed: {str(e)}")
        raise

    except ProcessingError as e:
        self.logger.error(f"Processing failed: {str(e)}")
        raise

    except Exception as e:
        self.logger.error(f"Unexpected error: {str(e)}")
        raise SemTPyError(f"Unexpected error occurred: {str(e)}")
```

### Testing Best Practices

#### Test Organization
```python
# test_data_processor.py

import pytest
from semt_py.processors import DataProcessor

class TestDataProcessor:
    """Test suite for DataProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create a DataProcessor instance for testing."""
        return DataProcessor(base_url="http://test.com")

    def test_valid_input(self, processor):
        """Test processing with valid input."""
        input_data = {"column": "value"}
        result = processor.process_data(input_data)
        assert result["status"] == "success"

    def test_invalid_input(self, processor):
        """Test processing with invalid input."""
        with pytest.raises(ValidationError):
            processor.process_data({})
```

#### Test Coverage Requirements
- Minimum 85% code coverage for new contributions
- 100% coverage for critical paths
- Test both success and failure cases
- Include edge cases and boundary conditions

#### Testing Guidelines
1. **Unit Tests**
   - Test each component in isolation
   - Mock external dependencies
   - Use meaningful test names
   - Include positive and negative test cases

2. **Integration Tests**
   - Test component interactions
   - Use realistic test data
   - Test complete workflows

3. **Performance Tests**
   - Test with large datasets
   - Measure response times
   - Check memory usage

#### Test Documentation
```python
def test_complex_scenario(processor):
    """
    Test complex data processing scenario.
    
    This test verifies that the processor can handle:
    1. Multiple input columns
    2. Nested data structures
    3. Special characters
    4. Edge cases
    
    Test data includes samples from real-world scenarios.
    """
    # Test implementation
```

### Version Control Guidelines

#### Commit Messages
Follow the conventional commits specification:
```
feat: add new reconciliation service
fix: handle null values in processor
docs: update API documentation
test: add integration tests for processor
refactor: simplify error handling logic
```

#### Branch Naming
```
feature/add-new-service
bugfix/handle-null-values
docs/update-api-docs
test/add-integration-tests
```

#### Code Review Checklist
- [ ] Code follows style guidelines
- [ ] Documentation is complete and accurate
- [ ] Tests are comprehensive
- [ ] Error handling is appropriate
- [ ] Performance implications considered
- [ ] Security implications considered

## Submission Process

### Pull Request Guidelines

#### Before Creating a Pull Request
1. **Review Documentation**
   - Read the [Quick Start Guide](getting-started/quickstart.md) to understand basic functionality
   - Review the [API Documentation](api.md) for detailed module information
   - Ensure your contribution aligns with project goals

2. **Prepare Your Development Environment**
   ```bash
   # Fork and clone the repository
   git clone https://github.com/yourusername/semt_py.git
   cd semt_py

   # Create a new branch
   git checkout -b feature/your-feature-name

   # Install development dependencies
   pip install -e ".[dev]"
   ```

3. **Development Checklist**
   - [ ] Write clear, documented code following our [General Guidelines](#general-guidelines)
   - [ ] Add comprehensive tests for new features
   - [ ] Update documentation if needed
   - [ ] Run the test suite locally
   - [ ] Update the CHANGELOG.md

#### Creating the Pull Request
1. **PR Template**
   ```markdown
   ## Description
   Brief description of the changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   - [ ] Code refactoring

   ## Testing
   - [ ] New tests added
   - [ ] Existing tests updated
   - [ ] All tests passing

   ## Documentation
   - [ ] Documentation updated
   - [ ] Examples added/updated

   ## Related Issues
   Fixes #[issue_number]
   ```

2. **Title Format**
   ```
   feat: Add new reconciliation service
   fix: Handle null values in processor
   docs: Update API documentation
   ```

3. **Required Information**
   - Clear description of changes
   - Link to related issues
   - Test coverage report
   - Documentation updates
   - Breaking changes (if any)

### Code Review Process

#### For Contributors

1. **Initial Submission**
   - Ensure PR meets all requirements
   - Respond to reviewer feedback promptly
   - Keep PR focused and concise
   - Update PR based on feedback

2. **Review Response Guidelines**
   ```markdown
   # Good response example:
   Thanks for the review! I've made the following changes:
   - Fixed the validation logic as suggested
   - Added error handling for edge cases
   - Updated tests to cover new scenarios
   
   Please let me know if anything else needs attention.
   ```

3. **Addressing Feedback**
   - Mark addressed comments as resolved
   - Push additional commits with clear messages
   - Request re-review when ready

#### For Reviewers

1. **Review Checklist**
   - [ ] Code follows project style guide
   - [ ] Tests are comprehensive and passing
   - [ ] Documentation is clear and complete
   - [ ] Changes are appropriate in scope
   - [ ] Security considerations addressed
   - [ ] Performance impact evaluated

2. **Review Comment Guidelines**
   ```markdown
   # Good review comment example:
   Consider handling the null case here:
   ```python
   if value is None:
       return default_value
   ```
   This would prevent the ValueError we're seeing in tests.
   ```

3. **Review Timeline**
   - Initial review within 2 business days
   - Follow-up reviews within 1 business day
   - Mark as approved when requirements met

#### After Merge

1. **Clean Up**
   ```bash
   # Update your fork
   git checkout main
   git pull upstream main

   # Delete feature branch
   git branch -d feature/your-feature-name
   ```

2. **Post-Merge Tasks**
   - Verify changes in staging environment
   - Update related documentation
   - Close related issues
   - Update project board

### Getting Help

If you need assistance at any point:

1. **Documentation Resources**
   - [Quick Start Guide](quickstart.md)
   - [API Documentation](./api.md)
   - [GitHub Repository](https://github.com/aliduabubakari/semt_py)

2. **Getting Support**
   - [Open an issue](https://github.com/aliduabubakari/semt_py/issues) for:
     - Bug reports
     - Feature requests
     - Documentation improvements
     - General questions

3. **Issue Template**
   ```markdown
   ## Issue Type
   - [ ] Bug Report
   - [ ] Feature Request
   - [ ] Documentation
   - [ ] Question

   ## Description
   Clear description of the issue or request

   ## Environment (for bugs)
   - Python version:
   - SemT_py version:
   - Operating System:

   ## Steps to Reproduce (for bugs)
   1. Step 1
   2. Step 2
   3. Step 3

   ## Expected Behavior
   What should happen

   ## Actual Behavior
   What actually happens
   ```

