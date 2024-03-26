'''
config.py

Set basic configurations to be used by the rest of the package.

Contains
--------
`grids_path` (str): directory to install stellar model grids. Defaults to a
    hidden cache directory created in the home directory: ~/.kiauhoku/grids

`grids_url` (str): Zenodo URL from which to download model grids. This URL
    is the generic one for the repository; it defaults to the latest version.
'''

import os
from socket import gethostname


grids_url = "https://zenodo.org/api/records/4287717"


if "ufhpc" in gethostname():
    grids_path = "/blue/jtayar/shared/kiauhoku_grids"
else:
    grids_path = os.path.join(os.path.expanduser('~/'), '.kiauhoku/grids')
