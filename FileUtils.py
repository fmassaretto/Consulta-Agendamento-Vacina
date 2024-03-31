import os
from pathlib import Path, PureWindowsPath


def get_dir_path():
    # I've explicitly declared my path as being in Windows format, so I can use forward slashes in it.
    full_file_path = PureWindowsPath(".\\data\\")

    # Convert path to the right format for the current operating system
    return Path(full_file_path)


def get_file_path(file_name):
    return get_dir_path() / file_name


def create_files(file_name):
    file_exists = os.path.isfile(str(get_file_path(file_name)))

    if not file_exists:
        with open(str(get_file_path(file_name)), 'w+') as writer:
            writer.write('')


def create_data_dir():
    dir_path = get_dir_path()
    if not dir_path.exists():
        os.makedirs(str(dir_path))


def build_dir_file(file_name):
    create_files(file_name)
    return get_file_path(file_name)


def initializer():
    create_data_dir()


initializer()
