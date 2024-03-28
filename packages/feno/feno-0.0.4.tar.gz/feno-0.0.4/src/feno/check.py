from typing import Tuple
import os
import glob
from os.path import getmtime


class Check:
    # return the last update for the most recent file in the directory
    @staticmethod
    def last_update(path) -> Tuple[str, float]:
        value = 0
        if os.path.isfile(path):
            value = (path, getmtime(path))
        else:
            file_list = list(glob.iglob(path + '/**', recursive=True))
            file_list = [f for f in file_list if os.path.isfile(f)]
            # juntos = [(f, getmtime(f)) for f in file_list]
            # print(juntos)
            if len(file_list) == 0:
                value = (path, getmtime(path))
            else:
                juntos = [(f, getmtime(f)) for f in file_list]
                value = max(juntos, key=lambda x: x[1])
        # print (value)
        return value

    # retorna se tem atualização e o arquivo mais recente
    @staticmethod
    def check_rebuild(source: str, target: str) -> Tuple[str, bool]:
        if not os.path.exists(target):
            return [source, True]
        [source_path, source_time] = Check.last_update(source)
        [target_path, target_time] = Check.last_update(target)
        # source tem novas alterações
        return (source_path, source_time > target_time)


