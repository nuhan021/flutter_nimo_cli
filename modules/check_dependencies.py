# =============================================================================
# modules/check_dependencies.py
# -----------------------------------------------------------------------------
# This module provides functions to check if required system dependencies like
# Python and Flutter are installed and available in the system's PATH.
# It includes a visual spinner for a better user experience during checks.
# =============================================================================

import subprocess
import platform
import sys
import time
import itertools
import threading
from termcolor import colored


class SpinnerThread(threading.Thread):
    """
    A thread that runs a continuous spinning animation in the console.
    """
    def __init__(self, message="Checking..."):
        super().__init__()
        self.message = message
        self.event = threading.Event()
        self.spinner = itertools.cycle([
            colored('-', "light_blue"),
            colored('/', "light_blue"),
            colored('|', "light_blue"),
            colored('\\', "light_blue")
        ])

    def run(self):
        """
        The main loop for the spinner animation.
        """
        while not self.event.is_set():
            sys.stdout.write(f"\r{next(self.spinner)} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        # Clear the line and print a newline when the thread stops
        sys.stdout.write('\r' + ' ' * (len(self.message) + 3) + '\r')
        sys.stdout.flush()

    def stop(self):
        """
        Signals the thread to stop and waits for it to join.
        """
        self.event.set()
        self.join()


def is_command_installed(command: str) -> bool:
    """
    Checks if a given command is installed and in the system's PATH.
    Uses a spinner animation for visual feedback.

    Args:
        command: The command to check (e.g., "flutter", "python").

    Returns:
        True if the command is found, False otherwise.
    """
    spinner = SpinnerThread(f"Checking for '{command}'...")
    spinner.start()

    try:
        # The 'shell=True' is used for cross-platform compatibility
        # and to correctly find executables like 'py' on Windows.
        subprocess.run(
            [command, "--version"],
            check=True,
            capture_output=True,
            text=True,
            shell=True
        )
        spinner.stop()
        print(colored(f"✅ '{command}' is installed.", "light_magenta"))
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        spinner.stop()
        print(colored(f"❌ '{command}' is not installed or not in PATH.", "red"))
        return False


def check_dependencies() -> bool:
    """
    Checks for the main dependencies: Python and Flutter.

    This function handles platform-specific Python executable names.

    Returns:
        True if both Python and Flutter are installed, False otherwise.
    """
    print()
    python_installed = False
    system = platform.system()

    if system == "Windows":
        # On Windows, Python can be 'python' or 'py'
        if is_command_installed("python"):
            python_installed = True
        elif is_command_installed("py"):
            python_installed = True
    else:
        # On other systems (Linux, macOS), Python is typically 'python3'
        if is_command_installed("python3"):
            python_installed = True

    # If Python is not found, we don't need to check for Flutter
    if not python_installed:
        print(colored("Python is not installed. Please install Python to continue.", "red"))
        return False

    flutter_installed = is_command_installed("flutter")

    return python_installed and flutter_installed
