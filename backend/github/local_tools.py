import platform
import logging

from pathlib import Path

from backend.log import log_enter_exit


@log_enter_exit
def get_custom_path() -> Path | None:
    """
    Gets the path to the custom folder inside of a tf2 directory.
    If none is returned, outside of this function, the tf2 directory should be asked for

    Returns:
        The Path to the directory
    """

    custom_path: Path | None
    user_platform: str = platform.system()

    match user_platform:
        case 'Windows':
            custom_path = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Team Fortress 2\tf\custom')
            if not custom_path.exists():
                logging.info(f"Custom path found: {custom_path}")
                custom_path = None
        case 'Darwin':  # MacOS
            custom_path = Path.home() / 'Downloads'  # I don't own a mac nor want to mess with the tf2 file path on that
            logging.warning("MacOS isn't supported. Everything will be downloaded to your downloads folder")
            logging.warning("If you would like to fix this, go to backend/github/local_tools.py to correct the path")
        case 'Linux':
            custom_path = Path.home() / '.steam/steam/steamapps/common/Team Fortress 2/tf/custom/'  # please don't use the flatpak version

            # this chain of ifs could be nicer
            if not custom_path.exists():
                custom_path = Path.home() / '.var/app/com.valvesoftware.Steam/data/Steam/steamapps/common/Team Fortress 2/tf/custom/'  # check for flatpak version
                if not custom_path.exists():
                    custom_path = None
                else:
                    logging.info(f"flatpak custom path found: {custom_path}")
            else:
                logging.info(f"Non snap/flatpak custom path found: {custom_path}")
        case _:
            custom_path = None

    return custom_path
