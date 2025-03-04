"""
Functions for more convenient file operations. 
"""

import os
import shutil
from glob import glob
from typing import List


def get_file_paths(path: str) -> List[str]:
    """
    Get full paths for files matching the given pattern.
    
    Args:
        path: A file path pattern (can include wildcards)
        
    Returns:
        A list of matching file paths
    """
    return glob(path)


def remove_files(path: str) -> List[str]:
    """
    Remove all files matching the given path pattern.
    
    Args:
        path: A file path pattern (can include wildcards)
        
    Returns:
        A list of removed file paths
    """
    file_list = get_file_paths(path)
    if not file_list:
        return []
    
    for file_path in file_list:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f'--> {file_path} not found')
    
    return file_list


def move_files(src: str, dst: str) -> List[str]:
    """
    Move all files matching the source pattern to destination.
    
    Args:
        src: Source path pattern (can include wildcards)
        dst: Destination directory
        
    Returns:
        A list of moved file paths
    """
    file_list = get_file_paths(src)
    if not file_list:
        return []
    
    for file_path in file_list:
        try:
            shutil.move(file_path, dst)
        except FileNotFoundError:
            print(f'--> {file_path} not found')
    
    return file_list


def copy_files(src: str, dst: str) -> List[str]:
    """
    Copy all files matching the source pattern to destination.
    
    Args:
        src: Source path pattern (can include wildcards)
        dst: Destination directory
        
    Returns:
        A list of copied file paths
    """
    file_list = get_file_paths(src)
    if not file_list:
        return []
    
    for file_path in file_list:
        try:
            shutil.copy(file_path, dst)
        except FileNotFoundError:
            print(f'--> {file_path} not found')
    
    return file_list
