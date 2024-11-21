# Installation Guide

SemT_py can be installed either in user mode (from GitHub) or developer mode (local installation). This guide provides detailed instructions for both installation methods, including setting up a virtual environment and working with sample notebooks.

## Prerequisites

Before installing SemT_py, ensure you have:

- **Python 3.6 or higher installed**
- **pip (Python package installer)**
- **Git (for cloning the repository)**

## Detailed Installation Process

### 1. Create and Set Up Virtual Environment

First, create a dedicated virtual environment for SemT_py:

```bash
# Create a new virtual environment
python3 -m venv myenv

# Activate the virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS and Linux:
source myenv/bin/activate
```

### 2. Install SemT_py

Choose one of the following installation methods:

#### A. User Installation (Recommended)
```bash
pip install --upgrade --no-cache-dir git+https://github.com/aliduabubakari/semt_py.git
```

#### B. Developer Installation
```bash
# Clone the repository
git clone https://github.com/aliduabubakari/semt_py.git
cd semt_py

# Install in development mode
pip install -e .
```

### 3. Set Up Jupyter Environment

To use SemT_py with Jupyter notebooks:

```bash
# Install ipykernel
pip install ipykernel

# Add your virtual environment to Jupyter
python -m ipykernel install --user --name=myenv --display-name "Python (myenv)"
```

### 4. Get Sample Notebooks

#### Option 1: Direct Download
1. Visit the [Sample Notebooks Folder](https://github.com/unimib-datAI/Semtui-python/tree/main/sample%20Notebooks)
2. Download the following files:
   - `sample_notebook.ipynb`
   - `SEMTUI_test_Notebook.ipynb`

#### Option 2: Using Terminal
If you've downloaded the notebooks to your Downloads folder:

```bash
# Create Sample Notebooks directory
mkdir -p myenv/Sample\ Notebooks/

# Move notebooks to the directory
mv ~/Downloads/sample_notebook.ipynb myenv/Sample\ Notebooks/
mv ~/Downloads/SEMTUI_test_Notebook.ipynb myenv/Sample\ Notebooks/
```

## Verification Steps

### 1. Verify Package Installation

```python
# Import all major components
from semt_py.auth_manager import AuthManager
from semt_py.extension_manager import ExtensionManager
from semt_py.reconciliation_manager import ReconciliationManager
from semt_py.utils import Utility
from semt_py.dataset_manager import DatasetManager
from semt_py.table_manager import TableManager
from semt_py.modification_manager import ModificationManager

print("All modules successfully imported!")
```

### 2. Verify Jupyter Setup

1. Launch Jupyter Notebook:
```bash
jupyter notebook
```

2. Create a new notebook using the "Python (myenv)" kernel

3. Try importing SemT_py:
```python
import semt_py
print("SemT_py successfully imported!")
```

## Dependencies

SemT_py relies on the following key dependencies (automatically installed):

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical operations
- **chardet**: Character encoding detection
- **PyJWT**: JWT token handling
- **fake-useragent**: User-Agent header generation
- **requests**: HTTP requests
- **python-dateutil**: Date manipulation
- **ipykernel**: Jupyter notebook support

## Directory Structure

After installation, your environment should look like this:
    
    ````
    project-folder/
    │
    ├── myenv/                # Virtual environment folder
    │   ├── Sample Notebooks/  # Folder to store notebooks and data files
    │   │   ├── sample_notebook.ipynb
    │   │   ├── SEMTUI_test_Notebook.ipynb
    │   │   ├── sample_data.csv    # Newly added sample data file
    │   │  
    └── your_script.py         # Any Python scripts you create

## Troubleshooting

### Common Issues and Solutions

1. **Virtual Environment Not Activating**
   ```bash
   # On Windows, try:
   .\myenv\Scripts\activate.bat
   # On Unix, try:
   source myenv/bin/activate
   ```

2. **Jupyter Kernel Not Found**
   ```bash
   # Reinstall and register kernel
   pip install --force-reinstall ipykernel
   python -m ipykernel install --user --name=myenv
   ```

3. **Package Import Errors**
   ```bash
   # Verify installation
   pip list | grep semt_py
   # Reinstall if necessary
   pip install --upgrade --force-reinstall git+https://github.com/aliduabubakari/semt_py.git
   ```
4. **Jupyter Notebook Not Installed**

In some cases, you may need to install Jupyter Notebook if it’s not already available. Use;

```bash
pip install notebook
```

## Deactivation

When finished, deactivate the virtual environment:

```bash
deactivate
```

## Next Steps

- Follow the [Quick Start Guide](quickstart.md) for basic usage
- Explore the [API Documentation](../api.md)
- Try the sample notebooks in `myenv/Sample Notebooks/`
- Visit our [GitHub repository](https://github.com/aliduabubakari/semt_py) for updates

For issues or help, please [open an issue](https://github.com/aliduabubakari/semt_py/issues) on GitHub.