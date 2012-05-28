import sys
import os

# Import from DisPass for versionStr
sys.path.insert(0, os.path.abspath('../../'))
from dispass import dispass

# language specific settings
language = 'nl'
html_title = dispass.versionStr + ' documentatie'
