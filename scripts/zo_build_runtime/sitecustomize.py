"""Install the official-input guard in Python children of a Quarto build."""
import os
from pathlib import Path
import sys

if os.environ.get('ZO_OFFICIAL_BUILD') == '1':
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from zo_build_boundary import official_inputs
    _official_context = official_inputs()
    _official_context.__enter__()
