import sys, os

# Import from DisPass for versionStr
sys.path.insert(0, os.path.abspath('../../dispass/'))
import dispass

# language specific settings
language = 'nl'
html_title = dispass.DisPass.versionStr + ' documentatie'
