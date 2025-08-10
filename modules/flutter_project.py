# =============================================================================
# modules/flutter_project.py
# -----------------------------------------------------------------------------
# This module contains functions to create a new Flutter project and to add
# dependencies using the 'flutter pub add' command.
# =============================================================================

import os
import subprocess
import sys
from termcolor import colored


def create_flutter_project(
    project_name: str,
    selected_devices: str,
    target_dir: str
) -> str:
    """
    Creates a new Flutter project in the specified directory.

    Args:
        project_name: The name of the new Flutter project.
        selected_devices: A comma-separated string of target platforms.
        target_dir: The directory where the project will be created.

    Returns:
        The full path to the newly created Flutter project.
    """
    project_path = os.path.join(target_dir, project_name)

    if os.path.exists(project_path):
        print(colored(
            f"Project already exists at {project_path}. Aborting.",
            "red"
        ))
        sys.exit(1)

    print(f"Creating Flutter project '{project_name}'...")
    try:
        command = f"flutter create --platforms {selected_devices.lower()} {project_name}"
        # 'cwd' specifies the working directory for the command
        subprocess.run(command, cwd=target_dir, check=True, shell=True)
        return project_path
    except subprocess.CalledProcessError as e:
        print(colored(
            f"Failed to create Flutter project. Error: {e}",
            "red"
        ))
        sys.exit(1)


def add_dependencies(flutter_project_path: str, dependencies: list[str]):
    """
    Adds a list of dependencies to the Flutter project.

    Args:
        flutter_project_path: The path to the Flutter project.
        dependencies: A list of dependency names to be added.
    """
    if not dependencies:
        print(colored("No dependencies to add.", "yellow"))
        return

    print("Adding dependencies...")
    try:
        # Use 'flutter pub add' with the list of dependencies
        flutter_dependency_str = " ".join(dependencies)
        command = f"flutter pub add {flutter_dependency_str}"
        subprocess.run(command, cwd=flutter_project_path, check=True, shell=True)
        print(colored("Dependencies added successfully.", "green"))
    except subprocess.CalledProcessError as e:
        print(colored(
            f"Failed to add dependencies. Error: {e}",
            "red"
        ))
        sys.exit(1)
