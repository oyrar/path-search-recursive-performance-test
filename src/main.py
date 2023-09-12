import os
import time
import glob
from logging import getLogger, basicConfig, DEBUG
from sys import stderr
from pathlib import Path

import line_profiler

basicConfig(stream=stderr, level=DEBUG, format='%(asctime)s %(levelname)s: %(filename)s:%(lineno)s %(funcName)s() %(message)s')
logger = getLogger(__name__)

@profile
def make_directory_list_by_pathobject(targets) -> list:
    if len(targets) == 0:
        return []

    if isinstance(targets, str):
        targets = [Path(targets).resolve()]

    logger.debug('start')
    #logger.debug(targets)

    target_dirs = [d for d in targets if d.is_dir()]
    logger.debug('create under list')
    under_dirs = [d for f in target_dirs for d in f.iterdir() if d.is_dir()]
    logger.debug('recursive under list')
    result = make_directory_list_by_pathobject(under_dirs)
    logger.debug('fin recursive')
    result += target_dirs

    logger.debug('fin')
    logger.debug(len(result))
    return result

@profile
def make_directory_list_by_ospath(targets) -> list:
    if len(targets) == 0:
        return []
    
    logger.debug('start')
    #logger.debug(targets)
    
    result = []

    target_directories = targets
    while len(target_directories) != 0:
        d = target_directories.pop(0)

        if not os.path.isdir(d):
            continue

        result.append(os.path.abspath(d))

        for under_file in os.listdir(d):
            if not os.path.isdir(d):
                continue
            joined_under_file = os.path.join(d, under_file)
            target_directories.append(os.path.abspath(joined_under_file))

    logger.debug('fin')
    logger.debug(len(result))
    return result

@profile
def make_directory_list_by_ospath_recursive(targets) -> list:
    if len(targets) == 0:
        return []
    
    logger.debug('start')
    #logger.debug(targets)
    
    result_in_result = [os.path.abspath(d) for d in targets if os.path.isdir(d) ]    
    under_dir = [os.path.join(d, under_path) for d in result_in_result for under_path in os.listdir(d)]
    result = make_directory_list_by_ospath_recursive(under_dir)
    result += result_in_result

    logger.debug('fin')
    logger.debug(len(result))
    return result

@profile
def make_directory_list_by_glob(targets : list) -> list:
    if len(targets) == 0:
        return []
    
    if isinstance(targets, str):
        targets = [targets]

    logger.debug('start')

    path_pattern = [os.path.join(pat, '**', '') for pat in targets]
    result = glob.glob(*path_pattern, recursive=True)

    logger.debug('fin')
    logger.debug(len(result))
    
    return result


if __name__ == '__main__':

    for i in range(200):
        result = make_directory_list_by_pathobject('path')
        result = make_directory_list_by_ospath(['path'])
        reulst = make_directory_list_by_ospath_recursive(['path'])
        reulst = make_directory_list_by_glob(['path'])
        reulst = make_directory_list_by_glob(['path'])
        reulst = make_directory_list_by_ospath_recursive(['path'])
        result = make_directory_list_by_ospath(['path'])
        result = make_directory_list_by_pathobject('path')

    time.sleep(1)
