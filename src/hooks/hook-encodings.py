"""
PyInstaller hook for encodings module

This hook ensures that the idna encoding is properly included in the build,
which is required for proper handling of URLs and internationalized domain names.
"""

# Explicitly include idna encoding to prevent the "unknown encoding: idna" error
hiddenimports = ['encodings.idna', 'encodings.ascii', 'encodings.utf_8', 'encodings.latin_1', 'encodings.cp1252'] 