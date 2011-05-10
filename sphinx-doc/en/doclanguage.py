import sys
import os

# Import from dispass for versionStr
sys.path.insert(0, os.path.abspath('../../'))
import dispass

# language specific settings
language = 'en'
html_title = dispass.versionStr + ' documentation'
