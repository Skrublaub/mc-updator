from pathlib import Path

########################## parse_tools ########################################################
RELEASES_PER_PAGE: int = 2

# no page option for later
MC_RELEASES_URL_BASE: str = 'https://api.github.com/repos/mastercomfig/mastercomfig/releases'
PROGRAM_PATH: Path = Path(__name__).parents[0]

######################### log #################################################################
LOG_FORMAT: str = '%(asctime)s-%(name)s-%(levelname)s: %(message)s'
LOG_DIR: Path = PROGRAM_PATH / "./logs"

######################## download tools #######################################################
DEFAULT_PRESET: str = "mastercomfig-medium-low-preset"
CHUNK_SIZE: int = 8192  # chunks to download the zip files with
