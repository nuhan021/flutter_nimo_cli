# =============================================================================
# main.py
# -----------------------------------------------------------------------------
# This is the main entry point for the Flutter project automation script.
# It orchestrates the entire process of creating a new Flutter project,
# applying a selected architectural template, and adding necessary dependencies.
# =============================================================================

import os
import sys
import inquirer
import re
from termcolor import colored

# Import all necessary modules from the 'modules' directory
from modules.check_dependencies import check_dependencies
from modules.flutter_project import create_flutter_project, add_dependencies
from modules.git_operations import clone_template_and_copy_lib
from modules.utils import replace_package_name_in_lib

# --- Configuration Constants -------------------------------------------------

# GitHub repository URLs for the architectural templates
TDD_GIT_REPO_URL = "https://github.com/nuhan021/bloc_tdd_clean_arc.git"
MVC_GIT_REPO_URL = "https://github.com/nuhan021/getX_project_structure.git"

# Dependencies to be added for the TDD architecture
TDD_DEPENDENCIES = [
    "flutter_bloc",
    "equatable",
    "provider",
    "uuid",
    "dartz",
    "google_fonts",
    "http",
    "get_it",
    "flutter_screenutil",
    "shared_preferences",
    "url_launcher",
    "intl",
    "logger"
]

# Dependencies to be added for the MVC architecture
MVC_DEPENDENCIES = [
    "get",
    "http",
    "logger"
]


def get_user_input():
    """
    Prompts the user for project details and validates the input.

    Returns:
        A tuple containing the validated project name, selected devices, and
        the chosen architecture.
    """
    while True:
        project_name = input(colored(
            "Flutter project name (use snake_case, no spaces): ",
            "light_yellow"
        )).strip()

        # Validate project name
        if not project_name:
            print(colored("Project name cannot be empty. Please try again.", "red"))
        elif not re.match(r"^[a-z0-9_]+$", project_name):
            print(colored(
                "Invalid project name. Use snake_case (e.g., my_new_app).",
                "red"
            ))
        else:
            break

    print('\n')

    # Get the desired architecture (TDD or MVC) using inquirer
    architecture_question = [
        inquirer.List(
            "architecture",
            message=colored("Select architecture:", "yellow", attrs=["bold"]),
            choices=["MVC", "TDD"],
            default="TDD"
        ),
    ]
    architecture = inquirer.prompt(architecture_question)["architecture"]

    # Get the target platforms using inquirer
    devices_question = [
        inquirer.Checkbox(
            "devices",
            message=colored(
                "Select target devices (space to select/unselect):",
                "light_cyan",
                attrs=['bold']
            ),
            choices=["android", "ios", "web", "windows", "macos", "linux"],
            default=["android", "ios", "web"]
        ),
    ]
    devices = inquirer.prompt(devices_question)["devices"]
    selected_device_str = ",".join(devices)

    print(f'\nArchitecture: {colored(architecture, "yellow", attrs=["bold"])}')
    print(f'Devices: {colored(selected_device_str, "yellow", attrs=["bold"])}\n')

    return project_name, selected_device_str, architecture


def main():
    """
    Main function to run the project creation process.
    """
    if not check_dependencies():
        print(colored(
            "\nSome dependencies are missing. Please install them to continue.",
            "red",
            attrs=['bold']
        ))
        sys.exit(1)

    print(colored(
        "\nAll required dependencies are installed. Let's create your project!",
        "light_green",
        attrs=["bold"]
    ))

    # Get user input for project configuration
    project_name, selected_devices, architecture = get_user_input()

    # Determine the base directory for the new project
    # This handles cross-platform home directory expansion
    base_dir = os.path.join(os.path.expanduser("~"), "Desktop")

    # Select the correct git repo URL and dependencies based on architecture
    if architecture == "TDD":
        repo_url = TDD_GIT_REPO_URL
        template_name = "bloc_tdd_arc"
        dependencies = TDD_DEPENDENCIES
    else:  # MVC
        repo_url = MVC_GIT_REPO_URL
        template_name = "getX_project_structure"
        dependencies = MVC_DEPENDENCIES

    try:
        # Step 1: Create a new Flutter project
        print(f"Creating Flutter project '{project_name}' in {base_dir}...")
        flutter_project_path = create_flutter_project(
            project_name,
            selected_devices,
            base_dir
        )
        print(colored(
            f"Successfully created project at {flutter_project_path}",
            "green"
        ))

        # Step 2: Clone the template and copy its 'lib' folder
        print("Cloning architectural template and replacing 'lib' folder...")
        clone_template_and_copy_lib(
            repo_url,
            flutter_project_path,
            template_name
        )

        # Step 3: Replace the old package name with the new one in all .dart files
        print("Updating package names in source files...")
        flutter_project_lib_path = os.path.join(flutter_project_path, "lib")
        replace_package_name_in_lib(
            flutter_project_lib_path,
            template_name,
            project_name
        )

        # Step 4: Add dependencies to the project
        print("Adding required dependencies...")
        add_dependencies(flutter_project_path, dependencies)

        print(colored(
            f"\n🎉 Project '{project_name}' with {architecture} architecture is ready!",
            "green",
            attrs=["bold"]
        ))

    except Exception as e:
        print(colored(f"\nAn error occurred: {e}", "red", attrs=['bold']))
        sys.exit(1)


if __name__ == "__main__":
    main()