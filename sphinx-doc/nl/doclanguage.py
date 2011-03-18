import sys, os

# Import from DisPass for versionStr
sys.path.insert(0, os.path.abspath('../../'))
import DisPass
dp = DisPass.DisPass

# language specific settings
language = 'nl'
html_title = dp.versionStr + ' documentatie'
