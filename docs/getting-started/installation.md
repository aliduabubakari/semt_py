# Installation Guide

SemT_py can be installed either in user mode (from GitHub) or developer mode (local installation). This guide covers both installation methods and provides verification steps for each.

## User Installation

For users who want to use SemT_py in their projects, we recommend installing directly from GitHub:

```bash
pip install --upgrade --no-cache-dir git+https://github.com/aliduabubakari/semt_py.git
```

### Verify User Installation

After installation, you can verify that all components are properly installed by running this import test:

```python
# Import necessary classes and functions from the SemT_py package
from semt_py.Auth_manager import AuthManager
from semt_py.extension_manager import ExtensionManager
from semt_py.reconciliation_manager import ReconciliationManager
from semt_py.utils import Utility
from semt_py.dataset_manager import DatasetManager
from semt_py.table_manager import TableManager
from semt_py.modification_manager import ModificationManager

print("All modules successfully imported!")
```

## Developer Installation

For developers who want to contribute to SemT_py or modify the source code, follow these steps for a local installation:

### 1. Create Virtual Environment

First, create and activate a new virtual environment:

```bash
# Create new virtual environment
python -m venv test_semt_env

# Activate the virtual environment
# On Windows:
test_semt_env\Scripts\activate
# On Unix or MacOS:
source test_semt_env/bin/activate
```

### 2. Verify Clean Environment

Ensure you're starting with a clean environment:

```bash
# Should show minimal packages
pip list
```

### 3. Install in Development Mode

Navigate to the project directory and install the package:

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/aliduabubakari/semt_py.git
cd semt_py

# Install in development mode
pip install -e .
```

Alternatively, if you have the distribution files:

```bash
pip install dist/semt_py-0.1-py2.py3-none-any.whl
```

### 4. Verify Developer Installation

```bash
# Check if it's installed
pip list | grep SemT_py

# Try importing it in Python
python -c "import semt_py; print('Package successfully imported!')"
```

## Testing the Installation

Here's a quick test to ensure everything is working correctly:

```python
# Start Python interpreter
python

# Import and test basic functionality
>>> import semt_py
>>> # Example: Initialize a table manager
>>> from semt_py.table_manager import TableManager
>>> table_mgr = TableManager()
```

## Deactivating the Virtual Environment

When you're done working with SemT_py, you can deactivate the virtual environment:

```bash
deactivate
```

## Troubleshooting

If you encounter any issues during installation:

1. **Import Errors**: Ensure you're using the correct Python version (Python 3.6+)
2. **Permission Issues**: Try using `pip install --user` for user-space installation
3. **Virtual Environment Issues**: Make sure the virtual environment is activated
4. **Package Not Found**: Verify you're using the correct package name and repository URL

## Dependencies

SemT_py requires the following main dependencies:
- pandas
- numpy
- chardet
- PyJWT
- fake-useragent
- requests
- python-dateutil

These will be automatically installed during the package installation.

## Next Steps

- Check out the [Quick Start Guide](quickstart.md) for basic usage examples
- Explore the [API Documentation](../api.md) for detailed information about all modules
- Visit our [GitHub repository](https://github.com/aliduabubakari/semt_py) for the latest updates

If you encounter any issues or need help, please [open an issue](https://github.com/aliduabubakari/semt_py/issues) on our GitHub repository.