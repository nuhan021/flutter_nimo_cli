# =============================================================================
# modules/git_operations.py
# -----------------------------------------------------------------------------
# This module handles git operations, specifically cloning a repository and
# copying its 'lib' directory to a new project.
# =============================================================================

import os
import subprocess
import shutil
import sys
from termcolor import colored
from modules.utils import safe_rmtree

def clone_template_and_copy_lib(
    repo_url: str,
    flutter_project_path: str,
    template_name: str
):
    """
    Clones a git repository, copies its 'lib' folder, and cleans up.

    Args:
        repo_url: The URL of the git repository to clone.
        flutter_project_path: The path to the new Flutter project.
        template_name: The name of the template repository. Used for temp directory naming.
    """
    # Create a temporary directory inside the project path for the cloned repo
    temp_dir = os.path.join(flutter_project_path, "temp_template")

    try:
        # Clone the git repository into the temporary directory
        print(f"Cloning template repo from {repo_url}...")
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, temp_dir],
            check=True
        )
        print("Template repo cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(colored(
            f"Failed to clone template repository. Error: {e}",
            "red"
        ))
        safe_rmtree(temp_dir) # Clean up even if cloning fails
        sys.exit(1)

    # Define source and destination paths for the 'lib' folder
    src_lib = os.path.join(temp_dir, "lib")
    dest_lib = os.path.join(flutter_project_path, "lib")

    # Check if the 'lib' folder exists in the cloned repo
    if not os.path.exists(src_lib):
        print(colored(
            f"Error: 'lib' folder not found in the cloned template.",
            "red"
        ))
        safe_rmtree(temp_dir)
        sys.exit(1)

    try:
        # Delete the existing 'lib' folder from the new project
        if os.path.exists(dest_lib):
            safe_rmtree(dest_lib)
        
        # Copy the 'lib' folder from the template to the new project
        shutil.copytree(src_lib, dest_lib)
        print(colored(
            f"Copied 'lib' folder from template to project.",
            "green"
        ))
    except (shutil.Error, OSError) as e:
        print(colored(
            f"Failed to copy 'lib' folder. Error: {e}",
            "red"
        ))
        safe_rmtree(temp_dir)
        sys.exit(1)
    finally:
        # Clean up by removing the temporary directory
        safe_rmtree(temp_dir)
