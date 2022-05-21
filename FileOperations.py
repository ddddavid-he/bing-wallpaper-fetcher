import os
import shutil as sh
from glob import glob



def full_path(path):
    return glob(path)


def rm(path):
    file_list = full_path(path)
    if len(file_list)==0:
        ...
    else:
        for f in file_list:
            try:
                os.remove(f)
            except FileNotFoundError:
                print(f'--> {f} not found')
    return file_list


def mv(src, dst):
    file_list = full_path(src)
    if len(file_list)==0:
        ...
    else:
        for f in file_list:
            try:
                sh.move(f, dst)
            except FileNotFoundError:
                print(f'--> {f} no found')
    return file_list


def cp(src, dst):
    file_list = full_path(src)
    if len(file_list)==0:
        ...
    else:
        for f in file_list:
            try:
                sh.copy(f, dst)
            except FileNotFoundError:
                print(f'--> {f} no found')
    return file_list


