# =============================================================================
# modules/utils.py
# -----------------------------------------------------------------------------
# This module contains utility functions for file system operations, such as
# safely removing directories and replacing strings in files.
# =============================================================================

import os
import shutil
import stat
import errno
from termcolor import colored


def handle_remove_readonly(func, path, exc):
    """
    Error handler for `shutil.rmtree`.
    This function handles cases where a file or directory is read-only
    and cannot be deleted. It sets the write permission and tries again.
    """
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


def safe_rmtree(path: str):
    """
    Recursively removes a directory and its contents.
    It uses an error handler to deal with read-only files, which is
    especially useful on Windows systems.

    Args:
        path: The path of the directory to be removed.
    """
    if not os.path.exists(path):
        return

    print(f"Deleting folder: {path}")
    try:
        shutil.rmtree(path, onerror=handle_remove_readonly)
        print(colored(f"Successfully deleted: {path}", "green"))
    except Exception as e:
        print(colored(f"Error deleting {path}: {e}", "red"))


def replace_package_name_in_lib(
    lib_path: str,
    old_pkg_name: str,
    new_pkg_name: str
):
    """
    Walks through a directory and replaces a specified package name
    in all `.dart` files.

    Args:
        lib_path: The path to the 'lib' directory.
        old_pkg_name: The package name to be replaced (e.g., 'bloc_tdd_arc').
        new_pkg_name: The new package name (e.g., 'my_new_project').
    """
    old_import_string = f"package:{old_pkg_name}"
    new_import_string = f"package:{new_pkg_name}"



    print('This is working...............................................')

    for root, _, files in os.walk(lib_path):
        for file in files:
            if file.endswith('.dart'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Only replace if the old package name is present
                    if old_import_string in content:
                        new_content = content.replace(
                            old_import_string,
                            new_import_string
                        )
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated imports in: {file_path}")
                except Exception as e:
                    print(colored(
                        f"Error processing file {file_path}: {e}",
                        "red"
                    ))
