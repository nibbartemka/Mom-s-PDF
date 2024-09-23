from pathlib import Path
import os


BASE_DIR = os.path.dirname(__file__)

STATIC_DIRECTORY_PATH: Path = Path(os.path.join(BASE_DIR, 'static'))

DEFAULT_OUTPUT_PATH: Path = Path(BASE_DIR)
