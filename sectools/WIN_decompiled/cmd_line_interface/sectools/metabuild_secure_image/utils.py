
import sys
from pathlib import Path
from typing import Dict, Optional
from cmd_line_interface.base_defines import AutoCloseFileType
from cmd_line_interface.sectools.metabuild_secure_image.defines import IMAGE_FINDER
from common.logging.logger import log_debug
from common.subprocess.subprocess import get_function_from_script
from core.metabuild_secure_image.defines import IMAGE_FINDER_FUNCTION_SIGNATURE, OEM_IMAGE_FINDER_FUNCTION_NAME, QTI_IMAGE_FINDER_FUNCTION_NAME

def get_image_finder_script(image_finder = None):
    log_debug('Locating image finder script.')
    sectools_path = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__) / '../../../..'
    image_finder_script = image_finder.path if image_finder else str(sectools_path / '../../../../common/build/app/image_finder.py')
    if not Path(image_finder_script).exists():
        raise RuntimeError(f'''Image finder script must be provided via {IMAGE_FINDER}.''')


def merge_image_finder_data(oem_image_finder_data = None, qti_image_finder_data = None):
    '''
    This function returns the union of two nested dictionary structures of the form
    {chipset: {storage: {flavor: { image_id: [] }}}
    where only the union of chipset, storage, and flavor values are of interest to be able to display available
    filters.
    '''
    finder_data = { }
    for key in set(oem_image_finder_data.keys()).union(set(qti_image_finder_data.keys())):
        if key in oem_image_finder_data and key in qti_image_finder_data:
            if isinstance(oem_image_finder_data[key], dict) and isinstance(qti_image_finder_data[key], dict):
                finder_data[key] = merge_image_finder_data(oem_image_finder_data[key], qti_image_finder_data[key])
                continue
            if isinstance(oem_image_finder_data[key], list) and isinstance(qti_image_finder_data[key], list):
                finder_data[key] = oem_image_finder_data[key]
            continue
        if key in oem_image_finder_data:
            finder_data[key] = oem_image_finder_data[key]
            continue
        finder_data[key] = qti_image_finder_data[key]
    return finder_data


def get_image_finder_data(image_finder = None):
    image_finder_script = get_image_finder_script(image_finder)
    oem_image_finder_data = get_function_from_script(image_finder_script, IMAGE_FINDER_FUNCTION_SIGNATURE, OEM_IMAGE_FINDER_FUNCTION_NAME)(None, None, None, None)
    qti_image_finder_data = get_function_from_script(image_finder_script, IMAGE_FINDER_FUNCTION_SIGNATURE, QTI_IMAGE_FINDER_FUNCTION_NAME)(None, None, None, None)
    return merge_image_finder_data(oem_image_finder_data, qti_image_finder_data)

