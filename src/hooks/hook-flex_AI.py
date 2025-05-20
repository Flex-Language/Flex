"""
PyInstaller hook for flex_AI module

This hook ensures that the data directories for flex_AI are properly included in the build,
and that all necessary dependencies are imported.
"""

from PyInstaller.utils.hooks import collect_data_files

# Include all data files from the flex_AI module
datas = collect_data_files('flex_AI')

# Ensure these modules are included
hiddenimports = [
    'encodings.idna',
    'ipaddress',
    'requests',
    'json',
    'urllib3',
    'chardet',
    'certifi'
] 